#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright 2020 NXP
#
# SPDX-License-Identifier: BSD-3-Clause

"""Boot Selection for SB file."""

from typing import List, Sequence

from spsdk.utils.crypto.abstract import BaseClass
from spsdk.utils.misc import DebugInfo
from .commands import parse_v1_command
from .headers import BootSectionHeaderV1, SecureBootFlagsV1
from ..commands import CmdBaseClass
from ..commands import CmdNop, CmdErase, CmdLoad, CmdFill, CmdJump, CmdCall, CmdReset, CmdMemEnable, CmdProg
from ..misc import SecBootBlckSize


class BootSectionV1(BaseClass):
    """Boot Section for SB file 1.x."""

    def __init__(self, section_id: int, flags: SecureBootFlagsV1 = SecureBootFlagsV1.NONE):
        """Initialize BootSectionV1.

        :param section_id: unique section ID, 32-bit int
        :param flags: see SecureBootFlagsV1
        """
        self._header = BootSectionHeaderV1(section_id, flags)
        self._commands: List[CmdBaseClass] = []

    def __str__(self) -> str:
        return self.info()

    @property
    def section_id(self) -> int:
        """Return unique ID of the section, 32 number."""
        return self._header.section_id

    @property
    def flags(self) -> SecureBootFlagsV1:
        """Return section flags."""
        return self._header.flags

    @property
    def bootable(self) -> bool:
        """Return whether section is bootable."""
        return self._header.bootable

    @property
    def rom_last_tag(self) -> bool:
        """ReturnROM_LAST_TAG flag.

        The last section header in an image always has its ROM_LAST_TAG flag set to help the ROM know at what point
        to stop searching.
        """
        return self._header.rom_last_tag

    @rom_last_tag.setter
    def rom_last_tag(self, value: bool) -> None:
        """Setter.

        :param value: ROM_LAST_TAG flag
        """
        self._header.rom_last_tag = value

    @property
    def cmd_size(self) -> int:
        """Return size of the binary representation of the commands."""
        return sum([cmd.raw_size for cmd in self._commands])

    @property
    def size(self) -> int:
        """Return size of the binary representation of the section in bytes."""
        result = self._header.raw_size + self.cmd_size
        return result

    def info(self) -> str:
        """Return string representation."""
        result = "[BootSection-V1]\n"
        result += f"ID: {self._header.section_id}\n"
        result += f"NumBlocks: {self._header.num_blocks}\n"
        result += self._header.info() + '\n'
        result += "[BootSection-commands]\n"
        for cmd in self._commands:
            result += cmd.info()
        return result

    @property
    def commands(self) -> Sequence[CmdBaseClass]:
        """Return sequence of all commands in the section."""
        return self._commands

    def append(self, cmd: CmdBaseClass) -> None:
        """Append command.

        :param cmd: to be added
        """
        assert isinstance(cmd, (CmdNop, CmdErase, CmdLoad, CmdFill, CmdJump, CmdCall, CmdReset, CmdMemEnable, CmdProg))
        self._commands.append(cmd)

    def update(self) -> None:
        """Update settings."""
        self._header.num_blocks = SecBootBlckSize.to_num_blocks(self.cmd_size)

    def export(self, dbg_info: DebugInfo = DebugInfo.disabled()) -> bytes:
        """Return binary representation of the class (serialization)."""
        self.update()
        dbg_info.append_section('Section')
        data = self._header.export()
        dbg_info.append_binary_data('Section-header', data)
        dbg_info.append_section('Commands')
        for cmd in self._commands:
            cmd_data = cmd.export(dbg_info)
            data += cmd_data
        return data

    @classmethod
    def parse(cls, data: bytes, offset: int = 0) -> 'BootSectionV1':
        """Deserialization from binary format.

        :param data: to be parsed
        :param offset: to start parsing
        :return: the parsed instance
        """
        header = BootSectionHeaderV1.parse(data, offset)
        result = BootSectionV1(0)
        result._header = header
        # commands
        cmd_base = offset + header.raw_size
        cmd_ofs = 0
        end_ofs = result._header.num_blocks * SecBootBlckSize.BLOCK_SIZE
        while cmd_ofs < end_ofs:
            cmd = parse_v1_command(data, cmd_base + cmd_ofs)
            result.append(cmd)
            cmd_ofs += cmd.raw_size
        return result
