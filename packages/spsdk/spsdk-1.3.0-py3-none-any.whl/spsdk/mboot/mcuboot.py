#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright 2016-2018 Martin Olejar
# Copyright 2019-2021 NXP
#
# SPDX-License-Identifier: BSD-3-Clause

"""Module for communication with the bootloader."""

import logging
import time
from types import TracebackType
from typing import Any, Dict, List, Optional, Sequence, Union, Type

from .commands import (
    CmdResponse, CommandTag, KeyProvOperation, KeyProvUserKeyType,
    CmdPacket, GenericResponse, GenerateKeyBlobSelect
)
from .error_codes import StatusCode
from .exceptions import McuBootCommandError, McuBootConnectionError, SPSDKError, McuBootDataAbortError
from .interfaces import Interface
from .memories import ExtMemPropTags, ExtMemId
from .properties import PropertyTag, Version, parse_property_value

logger = logging.getLogger('MBOOT')


########################################################################################################################
# McuBoot Class
########################################################################################################################
class McuBoot:  # pylint: disable=too-many-public-methods
    """Class for communication with the bootloader."""

    @property
    def status_code(self) -> StatusCode:
        """:return: status code of the last operation."""
        return self._status_code

    @property
    def is_opened(self) -> bool:
        """:return: True if the device is open."""
        return self._device.is_opened

    def __init__(self, device: Interface, cmd_exception: bool = False) -> None:
        """Initialize the McuBoot object.

        :param device: The instance of communication interface class
        :param cmd_exception: True to throw McuBootCommandError on any error;
                False to set status code only
                Note: some operation might raise McuBootCommandError is all cases

        """
        self._cmd_exception = cmd_exception
        self._status_code = StatusCode.SUCCESS
        self._device = device
        self.reopen = False

    def __enter__(self) -> 'McuBoot':
        self.reopen = True
        self.open()
        return self

    def __exit__(self, exception_type: Type[BaseException] = None,
                 exception_value: BaseException = None, traceback: TracebackType = None) -> None:
        self.close()

    def _process_cmd(self, cmd_packet: CmdPacket) -> Any:
        """Process Command.

        :param cmd_packet: Command Packet
        :return: commad response derived from the CmdResponse
        :raises McuBootConnectionError: Timeout Error
        :raises McuBootCommandError: Error during command execution on the target
        """
        if not self._device.is_opened:
            logger.info('TX: Device not opened')
            raise McuBootConnectionError('Device not opened')

        logger.debug(f'TX-PACKET: {cmd_packet.info()}')

        try:
            self._device.write(cmd_packet)
            response = self._device.read()
        except TimeoutError:
            self._status_code = StatusCode.NO_RESPONSE
            logger.debug('RX-PACKET: No Response, Timeout Error !')
            raise McuBootConnectionError("No Response from Device")

        assert isinstance(response, CmdResponse)
        logger.debug(f'RX-PACKET: {response.info()}')
        self._status_code = response.status

        if self._cmd_exception and self._status_code != StatusCode.SUCCESS:
            raise McuBootCommandError(CommandTag.name(cmd_packet.header.tag), response.status)

        return response

    def _read_data(self, cmd_tag: int, length: int) -> bytes:
        """Read data from device.

        :param cmd_tag: Tag indicating the read command.
        :param length: Length of data to read
        :raises McuBootConnectionError: Timeout error or a problem opening the interface
        :raises McuBootCommandError: Error during command execution on the target
        :return: Data read from the device
        """
        data = b''

        if not self._device.is_opened:
            logger.info('RX: Device not opened')
            raise McuBootConnectionError('Device not opened')

        while True:
            try:
                response = self._device.read()
            except McuBootDataAbortError as e:
                logger.info(f'RX: {e}')
                response = self._device.read()
            except TimeoutError:
                self._status_code = StatusCode.NO_RESPONSE
                logger.debug('RX: No Response, Timeout Error !')
                raise McuBootConnectionError("No Response from Device")

            if isinstance(response, bytes):
                data += response

            elif isinstance(response, GenericResponse):
                logger.debug(f'RX-PACKET: {response.info()}')
                self._status_code = response.status
                if response.cmd_tag == cmd_tag:
                    break

        if len(data) < length or self.status_code != StatusCode.SUCCESS:
            status_info = StatusCode.get(self._status_code, f'0x{self._status_code:08X}')
            logger.debug(f"CMD: Received {len(data)} from {length} Bytes, {status_info}")
            if self._cmd_exception:
                raise McuBootCommandError(CommandTag.name(cmd_tag), response.status)
        else:
            logger.info(f"CMD: Successfully Received {len(data)} from {length} Bytes")

        return data[:length] if len(data) > length else data

    def _send_data(self, cmd_tag: int, data: List[bytes]) -> bool:
        """Send Data part of specific command.

        :param cmd_tag: Tag indicating the command
        :param data: List of data chunks to send
        :raises McuBootConnectionError: Timeout error
        :raises McuBootCommandError: Error during command execution on the target
        :return: True if the operation is successfull
        """
        if not self._device.is_opened:
            logger.info('TX: Device Disconnected')
            raise McuBootConnectionError('Device Disconnected !')

        total_sent = 0
        # this difference is applicable for load-image and program-aeskey commands
        expect_response = (cmd_tag != CommandTag.NO_COMMAND)
        try:
            for data_chunk in data:
                self._device.write(data_chunk)
                total_sent += len(data_chunk)
            if expect_response:
                response = self._device.read()
        except TimeoutError:
            self._status_code = StatusCode.NO_RESPONSE
            logger.debug('RX: No Response, Timeout Error !')
            raise McuBootConnectionError("No Response from Device")
        except SPSDKError as e:
            logger.info(f'RX: {e}')
            if expect_response:
                response = self._device.read()

        if expect_response:
            assert isinstance(response, CmdResponse)
            logger.debug(f'RX-PACKET: {response.info()}')
            self._status_code = response.status
            if response.status != StatusCode.SUCCESS:
                status_info = StatusCode.get(self._status_code, f'0x{self._status_code:08X}')
                logger.debug(f"CMD: Send Error, {status_info}")
                if self._cmd_exception:
                    raise McuBootCommandError(CommandTag.name(cmd_tag), response.status)
                return False

        logger.info(f"CMD: Successfully Send {total_sent} out of {sum(len(chunk) for chunk in data)} Bytes")
        return True

    def _split_data(self, data: bytes) -> List[bytes]:
        """Split data to send if necessary.

        :param data: Data to send
        :return: List of data splices
        """
        if not self._device.need_data_split:
            return [data]
        packet_size_property = self.get_property(prop_tag=PropertyTag.MAX_PACKET_SIZE)
        assert packet_size_property, "Unable to get MAX PACKET SIZE"
        max_packet_size = packet_size_property[0]
        logger.info(f"CMD: Max Packet Size = {max_packet_size}")
        return [
            data[i:i + max_packet_size] for i in range(0, len(data), max_packet_size)
        ]

    def open(self) -> None:
        """Connect to the device."""
        if not self._device.is_opened:
            logger.info(f"Connect: {self._device.info()}")
            self._device.open()

    def close(self) -> None:
        """Disconnect from the device."""
        self._device.close()

    def get_property_list(self) -> list:
        """Get a list of available properties.

        :return: List of available properties.
        :raises McuBootCommandError: Failure to read properties list
        """
        property_list: List[Any] = []
        for tag in PropertyTag.tags():
            try:
                values = self.get_property(tag)
            except McuBootCommandError:
                continue

            if values:
                property_list.append(parse_property_value(tag, values))

        self._status_code = StatusCode.SUCCESS
        if not property_list:
            self._status_code = StatusCode.FAIL
            if self._cmd_exception:
                raise McuBootCommandError('GetPropertyList', self.status_code)

        return property_list

    def _get_internal_flash(self) -> dict:
        """Get information about the internal flash.

        - key: index
        - value: dictionary
            - key: 'address' / 'size' / 'sector_size'
            - value: number??
        :return: info about internal flash for memory map
        """
        index = 0
        mdata: dict = {}
        start_address = 0
        while True:
            try:
                values = self.get_property(PropertyTag.FLASH_START_ADDRESS, index)
                if not values:
                    break
                if index == 0:
                    start_address = values[0]
                elif start_address == values[0]:
                    break
                mdata[index] = {}
                mdata[index]['address'] = values[0]
                values = self.get_property(PropertyTag.FLASH_SIZE, index)
                if not values:
                    break
                mdata[index]['size'] = values[0]
                values = self.get_property(PropertyTag.FLASH_SECTOR_SIZE, index)
                if not values:
                    break
                mdata[index]['sector_size'] = values[0]
                index += 1
            except McuBootCommandError:
                break

        return mdata

    def _get_internal_ram(self) -> dict:
        """Get information about the internal RAM.

        - key: index
        - value: dictionary
            - key: 'address' / 'size'
            - value: number??
        :return: info about internal RAM
        """
        index = 0
        mdata: Dict[int, Dict[str, int]] = {}
        start_address = 0
        while True:
            try:
                values = self.get_property(PropertyTag.RAM_START_ADDRESS, index)
                if not values:
                    break
                if index == 0:
                    start_address = values[0]
                elif start_address == values[0]:
                    break
                mdata[index] = {}
                mdata[index]['address'] = values[0]
                values = self.get_property(PropertyTag.RAM_SIZE, index)
                if not values:
                    break
                mdata[index]['size'] = values[0]
                index += 1
            except McuBootCommandError:
                break

        return mdata

    def _get_ext_memories(self) -> list:
        """Get information about the external memories.

        List contains dictionary with info about memory:
        - mem_id
        - mem_name
        - address (optional)
        - size (optional)
        - page_size (optional)
        - sector_size (optional)
        - block_size (optional)
        :return: list of external memories supported by the device
        """
        ext_mem_list: List[Dict[str, Union[int, str]]] = []
        ext_mem_ids: Sequence[int] = ExtMemId.tags()
        try:
            values = self.get_property(PropertyTag.CURRENT_VERSION)
        except McuBootCommandError:
            values = None

        if not values and self._status_code == StatusCode.UNKNOWN_PROPERTY:
            self._status_code = StatusCode.SUCCESS
            return ext_mem_list

        assert values

        if Version(values[0]) <= Version("2.0.0"):
            # old versions mboot support only Quad SPI memory
            ext_mem_ids = [ExtMemId.QUAD_SPI0]

        for mem_id in ext_mem_ids:
            mem_attrs: Dict[str, Union[int, str]] = {}

            try:
                values = self.get_property(PropertyTag.EXTERNAL_MEMORY_ATTRIBUTES, mem_id)
            except McuBootCommandError:
                values = None

            if not values:  # pragma: no cover  # corner-cases are currently untestable without HW
                if self._status_code == StatusCode.UNKNOWN_PROPERTY:
                    break

                if self._status_code in [
                        StatusCode.INVALID_ARGUMENT,
                        StatusCode.QSPI_NOT_CONFIGURED, StatusCode.MEMORY_NOT_CONFIGURED
                ]:
                    continue

                assert self._status_code != StatusCode.SUCCESS  # Other Error
                break

            # memory ID and name
            mem_attrs['mem_id'] = mem_id
            mem_attrs['mem_name'] = ExtMemId.name(mem_id)
            # parse memory attributes
            if values[0] & ExtMemPropTags.START_ADDRESS:
                mem_attrs['address'] = values[1]
            if values[0] & ExtMemPropTags.SIZE_IN_KBYTES:
                mem_attrs['size'] = values[2] * 1024
            if values[0] & ExtMemPropTags.PAGE_SIZE:
                mem_attrs['page_size'] = values[3]
            if values[0] & ExtMemPropTags.SECTOR_SIZE:
                mem_attrs['sector_size'] = values[4]
            if values[0] & ExtMemPropTags.BLOCK_SIZE:
                mem_attrs['block_size'] = values[5]
            # store attributes
            ext_mem_list.append(mem_attrs)

        return ext_mem_list

    def get_memory_list(self) -> dict:
        """Get list of embedded memories.

        :return: dict, with the following keys: internal_flash (optional) - dictionary,
                internal_ram (optional) - dictionary, external_mems (optional) - list
        :raises McuBootCommandError: Error reading the memory list
        """
        memory_list: Dict[str, Any] = {}
        # Internal FLASH
        mdata = self._get_internal_flash()
        if mdata:
            memory_list['internal_flash'] = mdata

        # Internal RAM
        mdata = self._get_internal_ram()
        if mdata:
            memory_list['internal_ram'] = mdata

        # External Memories
        ext_mem_list = self._get_ext_memories()
        if ext_mem_list:
            memory_list['external_mems'] = ext_mem_list

        self._status_code = StatusCode.SUCCESS
        if not memory_list:
            self._status_code = StatusCode.FAIL
            if self._cmd_exception:
                raise McuBootCommandError('GetMemoryList', self.status_code)

        return memory_list

    def flash_erase_all(self, mem_id: int = 0) -> bool:
        """Erase complete flash memory without recovering flash security section.

        :param mem_id: Memory ID
        :return: False in case of any problem; True otherwise
        """
        logger.info(f"CMD: FlashEraseAll(mem_id={mem_id})")
        cmd_packet = CmdPacket(CommandTag.FLASH_ERASE_ALL, 0, mem_id)
        response = self._process_cmd(cmd_packet)
        return response.status == StatusCode.SUCCESS

    def flash_erase_region(self, address: int, length: int, mem_id: int = 0) -> bool:
        """Erase specified range of flash.

        :param address: Start address
        :param length: Count of bytes
        :param mem_id: Memory ID
        :return: False in case of any problem; True otherwise
        """
        logger.info(f"CMD: FlashEraseRegion(address=0x{address:08X}, length={length}, mem_id={mem_id})")
        cmd_packet = CmdPacket(CommandTag.FLASH_ERASE_REGION, 0, address, length, mem_id)
        return self._process_cmd(cmd_packet).status == StatusCode.SUCCESS

    def read_memory(self, address: int, length: int, mem_id: int = 0) -> Optional[bytes]:
        """Read data from MCU memory.

        :param address: Start address
        :param length: Count of bytes
        :param mem_id: Memory ID
        :return: Data read from the memory; None in case of a failure
        """
        logger.info(f"CMD: ReadMemory(address=0x{address:08X}, length={length}, mem_id={mem_id})")
        cmd_packet = CmdPacket(CommandTag.READ_MEMORY, 0, address, length, mem_id)
        cmd_response = self._process_cmd(cmd_packet)
        if cmd_response.status == StatusCode.SUCCESS:
            return self._read_data(CommandTag.READ_MEMORY, cmd_response.length)
        return None

    def write_memory(self, address: int, data: bytes, mem_id: int = 0) -> bool:
        """Write data into MCU memory.

        :param address: Start address
        :param data: List of bytes
        :param mem_id: Memory ID, see ExtMemId; additionally use `0` for internal memory
        :return: False in case of any problem; True otherwise
        """
        logger.info(f"CMD: WriteMemory(address=0x{address:08X}, length={len(data)}, mem_id={mem_id})")
        data_chunks = self._split_data(data=data)
        cmd_packet = CmdPacket(CommandTag.WRITE_MEMORY, 1, address, len(data), mem_id)
        if self._process_cmd(cmd_packet).status == StatusCode.SUCCESS:
            return self._send_data(CommandTag.WRITE_MEMORY, data_chunks)
        return False

    def fill_memory(self, address: int, length: int, pattern: int = 0xFFFFFFFF) -> bool:
        """Fill MCU memory with specified pattern.

        :param address: Start address (must be word aligned)
        :param length: Count of words (must be word aligned)
        :param pattern: Count of wrote bytes
        :return: False in case of any problem; True otherwise
        """
        logger.info(f"CMD: FillMemory(address=0x{address:08X}, length={length}, pattern=0x{pattern:08X})")
        cmd_packet = CmdPacket(CommandTag.FILL_MEMORY, 0, address, length, pattern)
        return self._process_cmd(cmd_packet).status == StatusCode.SUCCESS

    def flash_security_disable(self, backdoor_key: bytes) -> bool:
        """Disable flash security by using of backdoor key.

        :param backdoor_key: The key value as array of 8 bytes
        :return: False in case of any problem; True otherwise
        :raises ValueError: If the backdoor_key is not 8 bytes long
        """
        if len(backdoor_key) != 8:
            raise ValueError('Backdoor key must by 8 bytes long')
        logger.info(f"CMD: FlashSecurityDisable(backdoor_key={backdoor_key!r})")
        cmd_packet = CmdPacket(CommandTag.FLASH_SECURITY_DISABLE, 0, data=backdoor_key)
        return self._process_cmd(cmd_packet).status == StatusCode.SUCCESS

    def get_property(self, prop_tag: PropertyTag, index: int = 0) -> Optional[List[int]]:
        """Get specified property value.

        :param prop_tag: Property TAG (see Properties Enum)
        :param index: External memory ID or internal memory region index (depends on property type)
        :return: list integers representing the property; None in case no response from device
        """
        logger.info(f"CMD: GetProperty({PropertyTag.name(prop_tag, 'UNKNOWN')!r}, index={index!r})")
        cmd_packet = CmdPacket(CommandTag.GET_PROPERTY, 0, prop_tag, index)
        cmd_response = self._process_cmd(cmd_packet)
        return cmd_response.values if cmd_response.status == StatusCode.SUCCESS else None

    def set_property(self, prop_tag: PropertyTag, value: int) -> bool:
        """Set value of specified property.

        :param  prop_tag: Property TAG (see Property enumerator)
        :param  value: The value of selected property
        :return: False in case of any problem; True otherwise
        """
        logger.info(f"CMD: SetProperty({PropertyTag.name(prop_tag)}, value=0x{value:08X})")
        cmd_packet = CmdPacket(CommandTag.SET_PROPERTY, 0, prop_tag, value)
        cmd_response = self._process_cmd(cmd_packet)
        return cmd_response.status == StatusCode.SUCCESS

    def receive_sb_file(self, data: bytes) -> bool:
        """Receive SB file.

        :param  data: SB file data
        :return: False in case of any problem; True otherwise
        """
        logger.info(f"CMD: ReceiveSBfile(data_length={len(data)})")
        data_chunks = self._split_data(data=data)
        cmd_packet = CmdPacket(CommandTag.RECEIVE_SB_FILE, 1, len(data))
        cmd_response = self._process_cmd(cmd_packet)
        if cmd_response.status == StatusCode.SUCCESS:
            return self._send_data(CommandTag.RECEIVE_SB_FILE, data_chunks)
        return False

    def execute(self, address: int, argument: int, sp: int) -> bool:    # pylint: disable=invalid-name
        """Execute program on a given address using the stack pointer.

        :param address: Jump address (must be word aligned)
        :param argument: Function arguments address
        :param sp: Stack pointer address
        :return: False in case of any problem; True otherwise
        """
        logger.info(f"CMD: Execute(address=0x{address:08X}, argument=0x{argument:08X}, SP=0x{sp:08X})")
        cmd_packet = CmdPacket(CommandTag.EXECUTE, 0, address, argument, sp)
        return self._process_cmd(cmd_packet).status == StatusCode.SUCCESS

    def call(self, address: int, argument: int) -> bool:
        """Fill MCU memory with specified pattern.

        :param address: Call address (must be word aligned)
        :param argument: Function arguments address
        :return: False in case of any problem; True otherwise
        """
        logger.info(f"CMD: Call(address=0x{address:08X}, argument=0x{argument:08X})")
        cmd_packet = CmdPacket(CommandTag.CALL, 0, address, argument)
        return self._process_cmd(cmd_packet).status == StatusCode.SUCCESS

    def reset(self, timeout: int = 2000, reopen: bool = True) -> bool:
        """Reset MCU and reconnect if enabled.

        :param timeout: The maximal waiting time in [ms] for reopen connection
        :param reopen: True for reopen connection after HW reset else False
        :return: False in case of any problem; True otherwise
        :raises ValueError: if reopen is not supported
        :raises McuBootConnectionError: Failure to reopen the device
        """
        logger.info('CMD: Reset MCU')
        cmd_packet = CmdPacket(CommandTag.RESET, 0)
        ret_val = False
        if self._process_cmd(cmd_packet).status == StatusCode.SUCCESS:
            self._device.close()
            ret_val = True
            if reopen:
                if not self.reopen:
                    raise ValueError('reopen is not supported')
                time.sleep(timeout / 1000)
                try:
                    self._device.open()
                except SPSDKError:
                    ret_val = False
                    if self._cmd_exception:
                        raise McuBootConnectionError('reopen failed')
        return ret_val

    def flash_erase_all_unsecure(self) -> bool:
        """Erase complete flash memory and recover flash security section.

        :return: False in case of any problem; True otherwise
        """
        logger.info('CMD: FlashEraseAllUnsecure')
        cmd_packet = CmdPacket(CommandTag.FLASH_ERASE_ALL_UNSECURE, 0)
        return self._process_cmd(cmd_packet).status == StatusCode.SUCCESS

    def efuse_read_once(self, index: int) -> Optional[int]:
        """Read from MCU flash program once region.

        :param index: Start index
        :return: read value (32-bit int); None if operation failed
        """
        logger.info(f"CMD: FlashReadOnce(index={index})")
        cmd_packet = CmdPacket(CommandTag.FLASH_READ_ONCE, 0, index, 4)
        cmd_response = self._process_cmd(cmd_packet)
        return cmd_response.values[0] if cmd_response.status == StatusCode.SUCCESS else None

    def efuse_program_once(self, index: int, value: int) -> bool:
        """Write into MCU once program region (OCOTP).

        :param index: Start index
        :param value: Int value (4 bytes long)
        :return: False in case of any problem; True otherwise
        """
        logger.info(f"CMD: FlashProgramOnce(index={index}, value=0x{value:X})")
        cmd_packet = CmdPacket(CommandTag.FLASH_PROGRAM_ONCE, 0, index, 4, value)
        return self._process_cmd(cmd_packet).status == StatusCode.SUCCESS

    def flash_read_once(self, index: int, count: int = 4) -> Optional[bytes]:
        """Read from MCU flash program once region (max 8 bytes).

        :param index: Start index
        :param count: Count of bytes
        :return: Data read; None in case of an failure
        """
        assert count in (4, 8)
        logger.info(f"CMD: FlashReadOnce(index={index}, bytes={count})")
        cmd_packet = CmdPacket(CommandTag.FLASH_READ_ONCE, 0, index, count)
        cmd_response = self._process_cmd(cmd_packet)
        return cmd_response.data if cmd_response.status == StatusCode.SUCCESS else None

    def flash_program_once(self, index: int, data: bytes) -> bool:
        """Write into MCU flash program once region (max 8 bytes).

        :param index: Start index
        :param data: Input data aligned to 4 or 8 bytes
        :return: False in case of any problem; True otherwise
        """
        assert len(data) in (4, 8)
        logger.info(f"CMD: FlashProgramOnce(index={index!r}, data={data!r})")
        cmd_packet = CmdPacket(CommandTag.FLASH_PROGRAM_ONCE, 0, index, len(data), data=data)
        return self._process_cmd(cmd_packet).status == StatusCode.SUCCESS

    def flash_read_resource(self, address: int, length: int, option: int = 1) -> Optional[bytes]:
        """Read resource of flash module.

        :param address: Start address
        :param length: Number of bytes
        :param option:
        :return: Data from the resource; None in case of an failure
        """
        logger.info(f"CMD: FlashReadResource(address=0x{address:08X}, length={length}, option={option})")
        cmd_packet = CmdPacket(CommandTag.FLASH_READ_RESOURCE, 0, address, length, option)
        cmd_response = self._process_cmd(cmd_packet)
        if cmd_response.status == StatusCode.SUCCESS:
            return self._read_data(CommandTag.FLASH_READ_RESOURCE, cmd_response.length)
        return None

    def configure_memory(self, address: int, mem_id: int) -> bool:
        """Configure memory.

        :param address: The address in memory where are locating configuration data
        :param mem_id: Memory ID
        :return: False in case of any problem; True otherwise
        """
        logger.info(f"CMD: ConfigureMemory({mem_id}, address=0x{address:08X})")
        cmd_packet = CmdPacket(CommandTag.CONFIGURE_MEMORY, 0, mem_id, address)
        return self._process_cmd(cmd_packet).status == StatusCode.SUCCESS

    def reliable_update(self, address: int) -> bool:
        """Reliable Update.

        :param address: Address where new the firmware is stored
        :return: False in case of any problem; True otherwise
        """
        logger.info(f"CMD: ReliableUpdate(address=0x{address:08X})")
        cmd_packet = CmdPacket(CommandTag.RELIABLE_UPDATE, 0, address)
        return self._process_cmd(cmd_packet).status == StatusCode.SUCCESS

    def generate_key_blob(
            self, dek_data: bytes, key_sel: int = GenerateKeyBlobSelect.OPTMK, count: int = 72
        ) -> Optional[bytes]:
        """Generate Key Blob.

        :param dek_data: Data Encryption Key as bytes
        :param key_sel: select the BKEK used to wrap the BK (default: OPTMK/FUSES)
        :param count: Key blob count (default: 72 - AES128bit)
        :return: Key blob; None in case of an failure
        """
        logger.info(f"CMD: GenerateKeyBlob(dek_len={len(dek_data)}, key_sel={key_sel}, count={count})")
        data_chunks = self._split_data(data=dek_data)
        cmd_response = self._process_cmd(CmdPacket(CommandTag.GENERATE_KEY_BLOB, 1, key_sel, len(dek_data), 0))
        if cmd_response.status != StatusCode.SUCCESS:
            return None
        if not self._send_data(CommandTag.GENERATE_KEY_BLOB, data_chunks):
            return None
        cmd_response = self._process_cmd(CmdPacket(CommandTag.GENERATE_KEY_BLOB, 0, key_sel, count, 1))
        if cmd_response.status == StatusCode.SUCCESS:
            return self._read_data(CommandTag.GENERATE_KEY_BLOB, cmd_response.length)
        return None

    def kp_enroll(self) -> bool:
        """Key provisioning: Enroll Command (start PUF).

        :return: False in case of any problem; True otherwise
        """
        logger.info("CMD: [KeyProvisioning] Enroll")
        cmd_packet = CmdPacket(CommandTag.KEY_PROVISIONING, 0, KeyProvOperation.ENROLL)
        return self._process_cmd(cmd_packet).status == StatusCode.SUCCESS

    def kp_set_intrinsic_key(self, key_type: int, key_size: int) -> bool:
        """Key provisioning: Generate Intrinsic Key.

        :param key_type: Type of the key
        :param key_size: Size of the key
        :return: False in case of any problem; True otherwise
        """
        logger.info(f"CMD: [KeyProvisioning] SetIntrinsicKey(type={key_type}, key_size={key_size})")
        cmd_packet = CmdPacket(CommandTag.KEY_PROVISIONING, 0, KeyProvOperation.SET_INTRINSIC_KEY, key_type, key_size)
        return self._process_cmd(cmd_packet).status == StatusCode.SUCCESS

    def kp_write_nonvolatile(self, mem_id: int = 0) -> bool:
        """Key provisioning: Write the key to a nonvolatile memory.

        :param mem_id: The memory ID (default: 0)
        :return: False in case of any problem; True otherwise
        """
        logger.info(f"CMD: [KeyProvisioning] WriteNonVolatileMemory(mem_id={mem_id})")
        cmd_packet = CmdPacket(CommandTag.KEY_PROVISIONING, 0, KeyProvOperation.WRITE_NON_VOLATILE, mem_id)
        return self._process_cmd(cmd_packet).status == StatusCode.SUCCESS

    def kp_read_nonvolatile(self, mem_id: int = 0) -> bool:
        """Key provisioning: Load the key from a nonvolatile memory to bootloader.

        :param mem_id: The memory ID (default: 0)
        :return: False in case of any problem; True otherwise
        """
        logger.info(f"CMD: [KeyProvisioning] ReadNonVolatileMemory(mem_id={mem_id})")
        cmd_packet = CmdPacket(CommandTag.KEY_PROVISIONING, 0, KeyProvOperation.READ_NON_VOLATILE, mem_id)
        return self._process_cmd(cmd_packet).status == StatusCode.SUCCESS

    def kp_set_user_key(self, key_type: KeyProvUserKeyType, key_data: bytes) -> bool:
        """Key provisioning: Send the user key specified by <key_type> to bootloader.

        :param key_type: type of the user key, see enumeration for details
        :param key_data: binary content of the user key
        :return: False in case of any problem; True otherwise
        """
        logger.info(f"CMD: [KeyProvisioning] SetUserKey(key_type={KeyProvUserKeyType.name(key_type)}, "
                    f"key_len={len(key_data)})")
        data_chunks = self._split_data(data=key_data)
        cmd_packet = CmdPacket(CommandTag.KEY_PROVISIONING, 1, KeyProvOperation.SET_USER_KEY, key_type, len(key_data))
        cmd_response = self._process_cmd(cmd_packet)
        if cmd_response.status == StatusCode.SUCCESS:
            return self._send_data(CommandTag.KEY_PROVISIONING, data_chunks)
        return False

    def kp_write_key_store(self, key_data: bytes) -> bool:
        """Key provisioning: Write key data into key store area.

        :param key_data: key store binary content to be written to processor
        :return: result of the operation; True means success
        """
        logger.info(f"CMD: [KeyProvisioning] WriteKeyStore(key_len={len(key_data)})")
        data_chunks = self._split_data(data=key_data)
        cmd_packet = CmdPacket(CommandTag.KEY_PROVISIONING, 1, KeyProvOperation.WRITE_KEY_STORE, 0, len(key_data))
        cmd_response = self._process_cmd(cmd_packet)
        if cmd_response.status == StatusCode.SUCCESS:
            return self._send_data(CommandTag.KEY_PROVISIONING, data_chunks)
        return False

    def kp_read_key_store(self) -> Optional[bytes]:
        """Key provisioning: Read key data from key store area."""
        logger.info(f"CMD: [KeyProvisioning] ReadKeyStore")
        cmd_packet = CmdPacket(CommandTag.KEY_PROVISIONING, 0, KeyProvOperation.READ_KEY_STORE)
        cmd_response = self._process_cmd(cmd_packet)
        if cmd_response.status == StatusCode.SUCCESS:
            return self._read_data(CommandTag.KEY_PROVISIONING, cmd_response.length)
        return None

    def load_image(self, data: bytes) -> bool:
        """Load a boot image to the device.

        :param data: boot image
        :return: False in case of any problem; True otherwise
        """
        logger.info(f"CMD: LoadImage(length={len(data)})")
        data_chunks = self._split_data(data)
        # there's no command in this case
        self._status_code = StatusCode.SUCCESS
        return self._send_data(CommandTag.NO_COMMAND, data_chunks)
