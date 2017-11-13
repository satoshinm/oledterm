#!/usr/bin/env python
# -*- coding: utf-8 -*-
# based on:
# Copyright (c) 2014-17 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

import os
import time
import sys
from luma.core import cmdline
from luma.core.virtual import terminal
from PIL import ImageFont

VIRTUAL_TERMINAL_DEVICE = "/dev/vcsa"
ROWS = 9
COLS = 28

# based on demo_opts.py
from luma.core import cmdline, error
def get_device(actual_args=None):
    """
    Create device from command-line arguments and return it.
    """
    if actual_args is None:
        actual_args = sys.argv[1:]
    parser = cmdline.create_parser(description='luma.examples arguments')
    args = parser.parse_args(actual_args)

    if args.config:
        # load config from file
        config = cmdline.load_config(args.config)
        args = parser.parse_args(config + actual_args)

    # create device
    try:
        device = cmdline.create_device(args)
    except error.Error as e:
        parser.error(e)

    #print(display_settings(args))

    return device

# based on luma.examples terminal
def make_font(name, size):
    font_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'fonts', name))
    return ImageFont.truetype(font_path, size)


def main():
    if not os.access(VIRTUAL_TERMINAL_DEVICE, os.R_OK):
       print "Unable to access %s, try running as root?" % (VIRTUAL_TERMINAL_DEVICE,)
       raise SystemExit

    fontname = "tiny.ttf"
    size = 6

    font = make_font(fontname, size) if fontname else None
    term = terminal(device, font, animate=False)

    term.println("oledterm starting...")
    time.sleep(1)

    while True:
        data = file(VIRTUAL_TERMINAL_DEVICE).read()
        term.clear()
        term.println(data)
        term.flush()
        time.sleep(2)


if __name__ == "__main__":
    try:
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass
