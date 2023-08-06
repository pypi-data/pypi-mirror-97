#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright 2020-2021 NXP
#
# SPDX-License-Identifier: BSD-3-Clause

"""SerialProxy serves as patch replacement for serial.Serial class."""

import logging
from typing import Dict, Type   # pylint: disable=unused-import  # Type is necessary for Mypy

logger = logging.getLogger("SerialProxy")


class SerialProxy:
    """SerialProxy is used to simulate communication with serial device.

    It can be used as mock.patch for serial.Serial class.
    @patch(<your.package>.Serial, SerialProxy.init_proxy(pre_recorded_responses))
    """

    responses: Dict[bytes, bytes] = dict()

    @classmethod
    def init_proxy(cls, data: Dict[bytes, bytes]) -> 'Type[SerialProxy]':
        """Initialized response dictionary of write and read bytes.

        :param data: Dictionary of write and read bytes
        :return: SerialProxy class with configured data
        """
        cls.responses = data
        return cls

    def __init__(self, port: str, timeout: int, baudrate: int):
        """Basic initialization for serial.Serial class.

        __init__ signature must accommodate instantiation of serial.Serial

        :param port: Serial port name
        :param timeout: timeout (does nothing)
        :param baudrate: Serial port speed (does nothing)
        """
        self.port = port
        self.timeout = timeout
        self.baudrate = baudrate
        self.is_open = False
        self.buffer = bytes()

    def open(self) -> None:
        """Simulates opening a serial port."""
        self.is_open = True

    def close(self) -> None:
        """Simulates closing a serial port."""
        self.is_open = False

    def write(self, data: bytes) -> None:
        """Simulates a write, currently just pick up response from responses.

        :param data: Bytes to write, key in responses
        """
        logger.debug(f"I got: {data!r}")
        self.buffer = self.responses[data]
        logger.debug(f"setting buffer to: '{self.buffer!r}'")

    def read(self, length: int) -> bytes:
        """Read portion of pre-configured data.

        :param length: Amount of data to read from buffer
        :return: Data read
        """
        segment = self.buffer[:length]
        self.buffer = self.buffer[length:]
        logger.debug(f"I responded with: '{segment!r}'")
        return segment

    def info(self) -> str:
        """Text information about the interface."""
        return self.__class__.__name__

    def reset_input_buffer(self) -> None:
        """Simulates reseting input buffer."""

    def reset_output_buffer(self) -> None:
        """Simulates reseting output buffer."""

    def flush(self) -> None:
        """Simulates flushing input buffer."""


class SimpleReadSerialProxy(SerialProxy):
    """SimpleReadSerialProxy is used to simulate communication with serial device.

    It simplifies reading method.
    @patch(<your.package>.Serial, SerialProxy.init_proxy(pre_recorded_responses))
    """

    FULL_BUFFER = bytes()

    @classmethod
    def init_data_proxy(cls, data: bytes) -> 'Type[SimpleReadSerialProxy]':
        """Initialized response dictionary of write and read bytes.

        :param data: Dictionary of write and read bytes
        :return: SerialProxy class with configured data
        """
        cls.FULL_BUFFER = data
        return cls

    def __init__(self, port: str, timeout: int, baudrate: int):
        """Basic initialization for serial.Serial class.

        __init__ signature must accommodate instantiation of serial.Serial

        :param port: Serial port name
        :param timeout: timeout (does nothing)
        :param baudrate: Serial port speed (does nothing)
        """
        super().__init__(port=port, timeout=timeout, baudrate=baudrate)
        self.buffer = self.FULL_BUFFER

    def write(self, data: bytes) -> None:
        """Simulates a write method, but it does nothing.

        :param data: Bytes to write, key in responses
        """
        pass
