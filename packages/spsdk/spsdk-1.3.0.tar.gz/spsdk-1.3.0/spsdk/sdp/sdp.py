#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright 2017-2018 Martin Olejar
# Copyright 2019-2020 NXP
#
# SPDX-License-Identifier: BSD-3-Clause

"""Module implementing the SDP communication protocol."""

import logging
from typing import Optional, Tuple, Mapping

from .commands import CommandTag, CmdPacket, ResponseValue
from .error_codes import StatusCode
from .exceptions import SdpCommandError, SdpConnectionError
from .interfaces import Interface

logger = logging.getLogger('SDP')


########################################################################################################################
# Serial Downloader Protocol (SDP) Class
########################################################################################################################
class SDP:
    """Serial Downloader Protocol."""

    @property
    def status_code(self) -> StatusCode:
        """Get status code of the last operation."""
        return self._status_code

    @property
    def response_value(self) -> int:
        """Get the response value from last operation."""
        return self._response_value

    @property
    def is_opened(self) -> bool:
        """Indicates whether the underlying interface is open.

        :return: True if device is open, False if it's closed
        """
        return self._device.is_opened

    def __init__(self, device: Interface, cmd_exception: bool = False) -> None:
        """Initialize the SDP object.

        :param device: Interface to a device
        :param cmd_exception: True if commands should raise in exception, defaults to False
        """
        self._response_value = 0
        self._cmd_exception = cmd_exception
        self._status_code = StatusCode.SUCCESS
        self._device = device

    def __enter__(self) -> 'SDP':
        self.open()
        return self

    def __exit__(self, *args: Tuple, **kwargs: Mapping) -> None:
        self.close()

    def open(self) -> None:
        """Connect to i.MX device."""
        if not self._device.is_opened:
            logger.info(f"Connect: {self._device.info()}")
            self._device.open()

    def close(self) -> None:
        """Disconnect i.MX device."""
        self._device.close()

    def _process_cmd(self, cmd_packet: CmdPacket) -> bool:
        """Process Command Packet.

        :param cmd_packet: Command packet object
        :return: True if success else False.
        :raises SdpCommandError: If command failed and the 'cmd_exception' is set to True
        :raises SdpConnectionError: Timeout or Connection error
        """
        if not self.is_opened:
            logger.info('RX-CMD: Device Disconnected')
            raise SdpConnectionError('Device Disconnected !')

        logger.debug(f'TX-PACKET: {cmd_packet.info()}')
        self._status_code = StatusCode.SUCCESS

        try:
            self._device.write(cmd_packet)
            response = self._device.read()
        except Exception as e:
            logger.debug(e)
            logger.info('RX-CMD: Timeout Error')
            raise SdpConnectionError('Timeout Error')

        logger.info(f'RX-PACKET: {response.info()}')
        if response.hab:
            self._response_value = response.value
            if response.value != ResponseValue.UNLOCKED:
                self._status_code = StatusCode.HAB_IS_LOCKED

        return True

    def _read_status(self) -> int:
        """Read status value.

        :return: Status code
        :raises SdpConnectionError: Timeout
        """
        try:
            response = self._device.read()
            logger.info(f'RX-PACKET: {response.info()}')
        except:
            logger.info('RX-CMD: Timeout Error')
            raise SdpConnectionError('Timeout Error')

        return response.value

    def _read_data(self, length: int) -> Optional[bytes]:
        """Read data from device.

        :param length: Count of bytes
        :return: bytes read if the read operation is successfull else None
        :raises SdpCommandError: If command failed and the 'cmd_exception' is set to True
        :raises SdpConnectionError: Timeout or Connection error
        """
        MAX_LENGTH = 64
        data = b''
        remaining = length - len(data)
        while remaining > 0:
            try:
                self._device.expect_status = False
                response = self._device.read(min(remaining, MAX_LENGTH))
            except:
                logger.info('RX-CMD: Timeout Error')
                raise SdpConnectionError('Timeout Error')

            if not response.hab:
                data += response.raw_data
            else:
                logger.debug(f'RX-DATA: {response.info()}')
                self._response_value = response.value
                if response.value == ResponseValue.LOCKED:
                    self._status_code = StatusCode.HAB_IS_LOCKED
            remaining = length - len(data)
        return data[:length] if len(data) > length else data

    def _send_data(self, cmd_packet: CmdPacket, data: bytes) -> bool:
        """Send data to target.

        :param cmd_packet: Command packet object
        :param data: array with data to send
        :return: True if the write operation is successfull
        :raises SdpCommandError: If command failed and the 'cmd_exception' is set to True
        :raises SdpConnectionError: Timeout or Connection error
        """
        if not self.is_opened:
            logger.info('TX-DATA: Device Disconnected')
            raise SdpConnectionError('Device Disconnected !')

        logger.debug(f'TX-PACKET: {cmd_packet.info()}')
        self._status_code = StatusCode.SUCCESS
        ret_val = True

        try:
            # Send Command
            self._device.write(cmd_packet)

            # Send Data
            self._device.write(data)

            # Read HAB state (locked / unlocked)
            response = self._device.read()
            logger.debug(f'RX-DATA: {response.info()}')
            self._response_value = response.value
            # TODO: Is this condition necessary?
            if response.value != ResponseValue.UNLOCKED:
                self._status_code = StatusCode.HAB_IS_LOCKED

            # Read Command Status
            response = self._device.read()
            logger.debug(f'RX-DATA: {response.info()}')
            if cmd_packet.tag == CommandTag.WRITE_DCD and response.value != ResponseValue.WRITE_DATA_OK:
                self._status_code = StatusCode.WRITE_DCD_FAILURE
                ret_val = False
            elif cmd_packet.tag == CommandTag.WRITE_CSF and response.value != ResponseValue.WRITE_DATA_OK:
                self._status_code = StatusCode.WRITE_CSF_FAILURE
                ret_val = False
            elif cmd_packet.tag == CommandTag.WRITE_FILE and response.value != ResponseValue.WRITE_FILE_OK:
                self._status_code = StatusCode.WRITE_IMAGE_FAILURE
                ret_val = False

        except:
            logger.info('RX-CMD: Timeout Error')
            raise SdpConnectionError('Timeout Error')

        if not ret_val and self._cmd_exception:
            raise SdpCommandError('SendData', self.status_code)

        return ret_val

    def read(self, address: int, length: int, data_format: int = 32) -> Optional[bytes]:
        """Read value from reg/mem at specified address.

        :param address: Start address of first register
        :param length: Count of bytes
        :param data_format: Register access format 8, 16, 32 bits
        :return: Return bytes if success else None.
        """
        logger.info(f"TX-CMD: Read(address=0x{address:08X}, length={length}, format={data_format})")
        cmd_packet = CmdPacket(CommandTag.READ_REGISTER, address, data_format, length)
        if self._process_cmd(cmd_packet):
            return self._read_data(length)
        return None

    def read_safe(self, address: int, length: int, data_format: int = 32) -> Optional[bytes]:
        """Read value from reg/mem at specified address.

        This method is safe, because is validating input arguments and prevents fault execution.

        :param address: Start address of first register
        :param length: Count of bytes
        :param data_format: Register access format 8, 16, 32 bits
        :return: Return bytes if success else None.
        :raises ValueError: If the address is not properly aligned
        """
        # Check if start address value is aligned
        if (address % (data_format // 8)) > 0:
            raise ValueError(f"Address 0x{address:08X} not aligned to {data_format} bits")
        # Align count value if doesn't
        align = length % (data_format // 8)
        if align > 0:
            length += (data_format // 8) - align

        return self.read(address, length, data_format)

    def write(self, address: int, value: int, count: int = 4, data_format: int = 32) -> bool:
        """Write value into reg/mem at specified address.

        :param address: Start address of first register
        :param value: Register value
        :param count: Count of bytes (max 4)
        :param data_format: Register access format 8, 16, 32 bits
        :return: Return True if success else False.
        :raises SdpCommandError: If command failed and the 'cmd_exception' is set to True
        """
        logger.info(f"TX-CMD: Write(address=0x{address:08X}, value=0x{value:08X}, count={count}, format={data_format})")
        cmd_packet = CmdPacket(CommandTag.WRITE_REGISTER, address, data_format, count, value)
        if not self._process_cmd(cmd_packet):
            return False
        status = self._read_status()
        if status != ResponseValue.WRITE_DATA_OK:
            self._status_code = StatusCode.WRITE_REGISTER_FAILURE
            if self._cmd_exception:
                raise SdpCommandError('WriteRegister', self.status_code)
            return False
        return True

    def write_safe(self, address: int, value: int, count: int = 4, data_format: int = 32) -> bool:
        """Write value into reg/mem at specified address.

        This method is safe, because is validating input arguments and prevents fault execution.

        :param address: Start address of first register
        :param value: Register value
        :param count: Count of bytes (max 4)
        :param data_format: Register access format 8, 16, 32 bits
        :return: Return True if success else False.
        :raises ValueError: If the address is not properly aligned
        """
        # Check if start address value is aligned
        if (address % (data_format // 8)) > 0:
            raise ValueError(f"Address 0x{address:08X} not aligned to {data_format} bits")
        # Align count value if doesn't
        align = count % (data_format // 8)
        if align > 0:
            count += (data_format // 8) - align
        if count > 4:
            count = 4

        return self.write(address, value, count, data_format)

    def write_csf(self, address: int, data: bytes) -> bool:
        """Write CSF Data at specified address.

        :param address: Start Address
        :param data: The CSF data in binary format
        :return: Return True if success else False.
        """
        logger.info(f"TX-CMD: WriteCSF(address=0x{address:08X}, length={len(data)})")
        cmd_packet = CmdPacket(CommandTag.WRITE_CSF, address, 0, len(data))
        return self._send_data(cmd_packet, data)

    def write_dcd(self, address: int, data: bytes) -> bool:
        """Write DCD values at specified address.

        :param address: Start Address
        :param data: The DCD data in binary format
        :return: Return True if success else False.
        """
        logger.info(f"TX-CMD: WriteDCD(address=0x{address:08X}, length={len(data)})")
        cmd_packet = CmdPacket(CommandTag.WRITE_DCD, address, 0, len(data))
        return self._send_data(cmd_packet, data)

    def write_file(self, address: int, data: bytes) -> bool:
        """Write File/Data at specified address.

        :param address: Start Address
        :param data: The boot image data in binary format
        :return: Return True if success else False.
        """
        logger.info(f"TX-CMD: WriteFile(address=0x{address:08X}, length={len(data)})")
        cmd_packet = CmdPacket(CommandTag.WRITE_FILE, address, 0, len(data))
        return self._send_data(cmd_packet, data)

    def skip_dcd(self) -> bool:
        """Skip DCD blob from loaded file.

        :return: Return True if success else False.
        :raises SdpCommandError: If command failed and the 'cmd_exception' is set to True
        """
        logger.info('TX-CMD: Skip DCD')
        cmd_packet = CmdPacket(CommandTag.SKIP_DCD_HEADER, 0, 0, 0)
        if not self._process_cmd(cmd_packet):
            return False
        status = self._read_status()
        if status != ResponseValue.SKIP_DCD_HEADER_OK:
            self._status_code = StatusCode.SKIP_DCD_HEADER_FAILURE
            if self._cmd_exception:
                raise SdpCommandError('SkipDcdHeader', self.status_code)
            return False
        return True

    def jump_and_run(self, address: int) -> bool:
        """Jump to specified address and run code from there.

        :param address: Destination address
        :return: Return True if success else False.
        """
        logger.info(f"TX-CMD: Jump To Address: 0x{address:08X}")
        cmd_packet = CmdPacket(CommandTag.JUMP_ADDRESS, address, 0, 0)
        return self._process_cmd(cmd_packet)

    def read_status(self) -> Optional[int]:
        """Read Error Status.

        :return: Return status value if success else None
        """
        logger.info('TX-CMD: ReadStatus')
        if self._process_cmd(CmdPacket(CommandTag.ERROR_STATUS, 0, 0, 0)):
            return self._read_status()
        return None
