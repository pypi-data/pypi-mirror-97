#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright 2020-2021 NXP
#
# SPDX-License-Identifier: BSD-3-Clause

"""NXP USB Device Scanner."""

import sys

from typing import IO

import click

import spsdk.utils.nxpdevscan as nxpdevscan

from spsdk.apps.utils import catch_spsdk_error


@click.command()
@click.option('-e', '--extend-vids', multiple=True, default=[], help="VID in hex to extend search.")
@click.option('-o', '--out', default='-', type=click.File('w'))
def main(extend_vids: str, out: IO[str]) -> None:
    """Utility listing all connected NXP USB and UART devices."""
    additional_vids = [int(vid, 16) for vid in extend_vids]

    nxp_devices = nxpdevscan.search_nxp_usb_devices(additional_vids)
    if out.name == '<stdout>':
        click.echo(8*"-" + " Connected NXP USB Devices " + 8*"-" + "\n", out)
    for nxp_dev in nxp_devices:
        click.echo(nxp_dev.info(), out)
        click.echo('', out)

    nxp_devices = nxpdevscan.search_nxp_uart_devices()
    if out.name == '<stdout>':
        click.echo(8*"-" + " Connected NXP UART Devices " + 8*"-" + "\n", out)
    for nxp_dev in nxp_devices:
        click.echo(nxp_dev.info(), out)
        click.echo('', out)

@catch_spsdk_error
def safe_main() -> None:
    """Call the main function."""
    sys.exit(main())  # pragma: no cover  # pylint: disable=no-value-for-parameter


if __name__ == "__main__":
    safe_main()  # pragma: no cover
