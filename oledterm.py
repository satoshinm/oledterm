#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-17 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
Simple println capabilities.
"""

import os
import time
import sys
from luma.core import cmdline
from luma.core.virtual import terminal
from PIL import ImageFont

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
    while True:
        #for fontname, size in [(None, None), ("tiny.ttf", 6), ("ProggyTiny.ttf", 16), ("creep.bdf", 16), ("miscfs_.ttf", 12), ("FreePixel.ttf", 12)]:
        for fontname, size in [("tiny.ttf", 6), ("ProggyTiny.ttf", 16), ("creep.bdf", 16), ("miscfs_.ttf", 12), ("FreePixel.ttf", 12)]:
            font = make_font(fontname, size) if fontname else None
            term = terminal(device, font)

            term.println("Terminal mode demo")
            term.println("------------------")
            term.println("Uses any font to output text using a number of different print methods.")
            term.println()
            time.sleep(2)
            term.println("The '{0}' font supports a terminal size of {1}x{2} characters.".format(fontname, term.width, term.height))
            term.println()
            time.sleep(2)
            term.println("An animation effect is defaulted to give the appearance of spooling to a teletype device.")
            term.println()
            time.sleep(2)

            term.println("".join(chr(i) for i in range(32, 127)))
            time.sleep(2)

            term.clear()
            for i in range(30):
                term.println("Line {0:03d}".format(i))

            term.animate = False
            time.sleep(2)
            term.clear()

            term.println("Progress bar")
            term.println("------------")
            for mill in range(0, 10001, 25):
                term.puts("\rPercent: {0:0.1f} %".format(mill / 100.0))
                term.flush()

            time.sleep(2)
            term.clear()
            term.puts("Backspace test.")
            term.flush()
            time.sleep(2)
            for _ in range(17):
                term.backspace()
                time.sleep(0.2)

            time.sleep(2)
            term.clear()
            term.animate = True
            term.println("Tabs test")
            term.println("|...|...|...|...|...|")
            term.println("1\t2\t4\t11")
            term.println("992\t43\t9\t12")
            term.println("\t3\t99\t1")
            term.flush()
            time.sleep(2)


if __name__ == "__main__":
    try:
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass
