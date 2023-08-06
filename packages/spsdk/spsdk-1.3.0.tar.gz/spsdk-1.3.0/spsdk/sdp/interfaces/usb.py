#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright 2017-2018 Martin Olejar
# Copyright 2019-2021 NXP
#
# SPDX-License-Identifier: BSD-3-Clause
"""Module for USB communication with a terget using SDP protocol."""

import logging
import platform

from typing import Sequence, Tuple, Union

import hid

from spsdk.utils.usbfilter import USBDeviceFilter

from ..commands import CmdPacket, CmdResponse
from ..exceptions import SdpConnectionError
from .base import Interface

logger = logging.getLogger('SDP:USB')

# import os
# os.environ['PYUSB_DEBUG'] = 'debug'
# os.environ['PYUSB_LOG_FILENAME'] = 'usb.log'

HID_REPORT = {
    # name | id | length
    'CMD': (0x01, 1024, False),
    'DATA': (0x02, 1024, False),
    'HAB': (0x03, 4),
    'RET': (0x04, 64)
}

USB_DEVICES = {
    # NAME    | VID   | PID
    'MX6DQP': (0x15A2, 0x0054),
    'MX6SDL': (0x15A2, 0x0061),
    'MX6SL': (0x15A2, 0x0063),
    'MX6SX': (0x15A2, 0x0071),
    'MX6UL': (0x15A2, 0x007D),
    'MX6ULL': (0x15A2, 0x0080),
    'MX6SLL': (0x15A2, 0x0128),
    'MX7SD': (0x15A2, 0x0076),
    'MX7ULP': (0x1FC9, 0x0126),
    'VYBRID': (0x15A2, 0x006A),
    'MXRT20': (0x1FC9, 0x0130),
    'MXRT50': (0x1FC9, 0x0130),
    'MXRT60': (0x1FC9, 0x0135),
    'MX8MQ': (0x1FC9, 0x012B),
    'MX8QXP-A0': (0x1FC9, 0x007D),
    'MX8QM-A0': (0x1FC9, 0x0129),
    'MX8QXP': (0x1FC9, 0x012F),
    'MX8QM': (0x1FC9, 0x0129),
    'MX815': (0x1FC9, 0x013E),
    'MX865': (0x1FC9, 0x0146)
}


def scan_usb(device_name: str = None) -> Sequence[Interface]:
    """Scan connected USB devices. Return a list of all devices found.

    :param device_name: see USBDeviceFilter classes constructor for usb_id specification
    :return: list of matching RawHid devices
    """
    usb_filter = USBDeviceFilter(usb_id=device_name, nxp_device_names=USB_DEVICES)
    return RawHid.enumerate(usb_filter)


########################################################################################################################
# USB HID Interface Class
########################################################################################################################
class RawHid(Interface):
    """Base class for OS specific RAW HID Interface classes."""
    @property
    def name(self) -> str:
        """Get the name of the device.

        :return: Name of the device.
        """
        for name, value in USB_DEVICES.items():
            if value[0] == self.vid and value[1] == self.pid:
                return name
        return 'Unknown'

    @property
    def is_opened(self) -> bool:
        """Indicates whether device is open.

        :return: True if device is open, False othervise.
        """
        return self.device is not None and self._opened

    def __init__(self) -> None:
        """Initialize the USB interface object."""
        self._opened = False
        self.vid = 0
        self.pid = 0
        self.serial_number = ""
        self.vendor_name = ""
        self.product_name = ""
        self.interface_number = 0
        self.timeout = 2000
        self.path = ""
        self.device = None

    @staticmethod
    def _encode_report(report_id: int, report_size: int, data: bytes, offset: int = 0) -> Tuple[bytes, int]:
        """Encode the USB packet.

        :param report_id: ID of the report (see: HID_REPORT)
        :param report_size: Length of the report to send
        :param data: Data to send
        :param offset: offset within the 'data' bytes
        :return: Encoded bytes and length of the final report frame
        """
        data_len = min(len(data) - offset, report_size)
        raw_data = bytes([report_id])
        raw_data += data[offset: offset + data_len]
        raw_data += bytes([0x00] * (report_size - data_len))
        logger.debug(f"OUT[{len(raw_data)}]: {', '.join(f'{b:02X}' for b in raw_data)}")
        return raw_data, offset + data_len

    @staticmethod
    def _decode_report(raw_data: bytes) -> CmdResponse:
        """Decodes the data read on USB interface.

        :param raw_data: Data received
        :type raw_data: bytes
        :return: CmdResponse object
        """
        logger.debug(f"IN [{len(raw_data)}]: {', '.join(f'{b:02X}' for b in raw_data)}")
        return CmdResponse(raw_data[0] == HID_REPORT['HAB'][0], raw_data[1:])

    def info(self) -> str:
        """Return information about the USB interface."""
        return f"{self.product_name:s} (0x{self.vid:04X}, 0x{self.pid:04X})"

    def conf(self, config: dict) -> None:
        """Set HID report data.

        :param config: parameters dictionary
        """
        if 'hid_ep1' in config and 'pack_size' in config:
            HID_REPORT['CMD'] = (0x01, config['pack_size'], config['hid_ep1'])
            HID_REPORT['DATA'] = (0x02, config['pack_size'], config['hid_ep1'])

    def open(self) -> None:
        """Open the interface."""
        logger.debug("Open Interface")
        try:
            assert self.device
            self.device.open_path(self.path)
            self.device.set_nonblocking(False)
            # self.device.read(1021, 1000)
            self._opened = True
        except OSError:
            raise SdpConnectionError(
                f"Unable to open device VIP={self.vid} PID={self.pid} SN='{self.serial_number}'"
            )

    def close(self) -> None:
        """Close the interface."""
        logging.debug("Close Interface")
        try:
            assert self.device
            self.device.close()
            self._opened = False
        except OSError:
            raise SdpConnectionError(
                f"Unable to close device VIP={self.vid} PID={self.pid} SN='{self.serial_number}'"
            )

    def write(self, packet: Union[CmdPacket, bytes]) -> None:
        """Write data on the OUT endpoint associated to the HID interfaces.

        :param packet: Data to send
        :raises ValueError: Raises an error if packet type is incorrect
        :raises SdpConnectionError: Raises an error if device is openned for writing
        """
        if not self.is_opened:
            raise SdpConnectionError(f"Device is openned for writing")

        if isinstance(packet, CmdPacket):
            report_id, report_size, hid_ep1 = HID_REPORT['CMD']
            data = packet.to_bytes()
        elif isinstance(packet, (bytes, bytearray)):
            report_id, report_size, hid_ep1 = HID_REPORT['DATA']
            data = packet
        else:
            raise ValueError("Packet has to be either 'CmdPacket' or 'bytes'")

        assert self.device
        data_index = 0
        while data_index < len(data):
            raw_data, data_index = self._encode_report(report_id, report_size,
                                                       data, data_index)
            self.device.write(raw_data)

    def read(self, length: int = None) -> CmdResponse:
        """Read data on the IN endpoint associated to the HID interface.

        :return: Return CmdResponse object.
        :raises SdpConnectionError: Raises an error if device is openned for reading
        """
        if not self.is_opened:
            raise SdpConnectionError(f"Device is openned for reading")

        assert self.device
        raw_data = self.device.read(1024, self.timeout)
        if raw_data[0] == 0x04 and platform.system() == "Linux":
            raw_data += self.device.read(1024, self.timeout)
        return self._decode_report(bytes(raw_data))

    @staticmethod
    def enumerate(usb_device_filter: USBDeviceFilter) -> Sequence[Interface]:
        """Get list of all connected devices which matches device_id.

        :param usb_device_filter: USBDeviceFilter object
        :return: List of interfaces found
        """
        devices = []
        all_hid_devices = hid.enumerate()

        # iterate on all devices found
        for dev in all_hid_devices:
            if usb_device_filter.compare(dev) is True:
                new_device = RawHid()
                new_device.device = hid.device()
                new_device.vid = dev["vendor_id"]
                new_device.pid = dev["product_id"]
                new_device.vendor_name = dev['manufacturer_string']
                new_device.product_name = dev['product_string']
                new_device.interface_number = dev['interface_number']
                new_device.path = dev["path"]
                devices.append(new_device)

        return devices
