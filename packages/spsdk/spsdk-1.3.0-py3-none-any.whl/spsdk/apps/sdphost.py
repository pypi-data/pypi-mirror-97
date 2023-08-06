#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright 2020-2021 NXP
#
# SPDX-License-Identifier: BSD-3-Clause

"""Console script for SDP module aka SDPHost."""

import inspect
import json
import logging
import sys

import click
from click_option_group import MutuallyExclusiveOptionGroup, optgroup

from spsdk import __version__ as spsdk_version
from spsdk.apps.utils import INT, get_interface, format_raw_data, catch_spsdk_error
from spsdk.sdp import SDP
from spsdk.sdp.commands import ResponseValue


@click.group()
@optgroup.group('Interface configuration', cls=MutuallyExclusiveOptionGroup)
@optgroup.option('-p', '--port', help='Serial port')
@optgroup.option('-u', '--usb', help="""
USB device identifier. Following formats are supported:
<vid>, <vid:pid> or <vid,pid>, device/instance path, device name.
vid: hex or dec string; e.g. 0x0AB12, 43794.

vid/pid: hex or dec string; e.g. 0x0AB12:0x123, 1:3451

device name: use 'dscan' utility to list supported device names.

path - OS specific string.
Windows:
'device instance path' in device manager under Windows OS.

Linux specific:
Use 'Bus' and 'Device' ID observed using 'lsusb' in <bus>#<device>' form; e.g. '3#2'.

Mac specific:
Use device name and location ID from 'System report' in '<device_name> <location id>'
form. e.g. 'SE Blank RT Family @14100000'
""")
@click.option('-j', '--json', 'use_json', is_flag=True, help='Use JSON output')
@click.option('-v', '--verbose', 'log_level', flag_value=logging.INFO, help='Display more verbose output')
@click.option('-d', '--debug', 'log_level', flag_value=logging.DEBUG, help='Display debugging info')
@click.option('-t', '--timeout', metavar='<ms>', help='Set packet timeout in milliseconds', default=5000)
@click.version_option(spsdk_version, '--version')
@click.pass_context
def main(ctx: click.Context, port: str, usb: str, use_json: bool, log_level: int, timeout: int) -> int:
    """Utility for communication with ROM on i.MX targets."""
    logging.basicConfig(level=log_level or logging.WARNING)
    # if --help is provided anywhere on commandline, skip interface lookup and display help message
    if '--help ' in sys.argv:
        port, usb = None, None  # type: ignore
    ctx.obj = {
        'interface': get_interface(
            module='sdp', port=port, usb=usb, timeout=timeout
        ) if port or usb else None,
        'use_json': use_json
    }
    return 0


@main.command()
@click.pass_context
def error_status(ctx: click.Context) -> None:
    """Get error code of last operation."""
    with SDP(ctx.obj['interface']) as sdp:
        response = sdp.read_status()
    display_output(
        [response], sdp.response_value, ctx.obj['use_json'],
        extra_output=f"Response status = {decode_status_code(response)}."
    )


@main.command()
@click.argument('address', type=INT(), required=True)
@click.pass_context
def jump_address(ctx: click.Context, address: int) -> None:
    """Jump to entry point of image with IVT at specified address.

    \b
    ADDRESS - starting address of the image
    """
    with SDP(ctx.obj['interface']) as sdp:
        sdp.jump_and_run(address)
    display_output([], sdp.response_value)


@main.command()
@click.argument('address', type=INT(), required=True)
@click.argument('bin_file', metavar='FILE', type=click.File('rb'), required=True)
@click.argument('count', type=INT(), required=False)
@click.pass_context
def write_file(ctx: click.Context, address: int, bin_file: click.File, count: int) -> None:
    """Write file at address.

    \b
    ADDRESS - starting address of the image
    FILE    - binary file to write
    COUNT   - Count is size of data to write in bytes (default: whole file)
    """
    data = bin_file.read(count)  # type: ignore
    with SDP(ctx.obj['interface']) as sdp:
        sdp.write_file(address, data)
    display_output([], sdp.response_value)


@main.command()
@click.argument('address', type=INT(), required=True)
@click.argument('item_length', type=int, required=False, default=32, metavar='[FORMAT]')
@click.argument('count', type=int, required=False, default=1)
@click.argument('file', type=click.File('wb'), required=False)
@click.option('-h', '--use-hexdump', is_flag=True, default=False, help='Use hexdump format')
@click.pass_context
def read_register(ctx: click.Context, address: int, item_length: int, count: int,
                  file: click.File, use_hexdump: bool) -> None:
    """Read one or more registers.

    \b
    ADDRESS - starting address where to read
    FORMAT  - bits per item: valid values: 8, 16, 32; default 32
    COUNT   - items to read; default 1
    FILE    - write data into a file; write to stdout if not specified
    """
    with SDP(ctx.obj['interface']) as sdp:
        response = sdp.read_safe(address, count, item_length)
    if not response:
        click.echo(f"Error: invalid command or arguments 'read-register {address:#8X} {item_length} {count}'")
        sys.exit(1)
    if file:
        file.write(response)  # type: ignore
    else:
        click.echo(format_raw_data(response, use_hexdump=use_hexdump))
    display_output([], sdp.response_value, ctx.obj['use_json'])


def display_output(response: list, status_code: int, use_json: bool = False,
                   extra_output: str = None) -> None:
    """Printout the response.

    :param response: Response list to display
    :param status_code: Response status
    :param use_json: use JSON output format
    :param extra_output: Extra string to display
    """
    if use_json:
        data = {
            # get the name of a caller function and replace _ with -
            'command': inspect.stack()[1].function.replace('_', '-'),
            # this is just a visualization thing
            'response': response or [],
            'status': {
                'description': decode_status_code(status_code),
                'value': status_code
            }
        }
        print(json.dumps(data, indent=3))
    else:
        print(f'Status (HAB mode) = {decode_status_code(status_code)}.')
        if extra_output:
            print(extra_output)


def decode_status_code(status_code: int = None) -> str:
    """Return a stringified representation of status code.

    :param status_code: SDP status code
    :type status_code: int
    :return: stringified representation
    :rtype: str
    """
    if not status_code:
        return f"UNKNOWN ERROR"
    return f"{status_code} ({status_code:#x}) {ResponseValue.desc(status_code)}"


@catch_spsdk_error
def safe_main() -> None:
    """Call the main function."""
    sys.exit(main())  # pragma: no cover  # pylint: disable=no-value-for-parameter


if __name__ == "__main__":
    safe_main()  # pragma: no cover
