#!/usr/bin/env python
# -*- coding: utf-8 -*-
# based on:
# Copyright (c) 2014-17 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

import os
import time
import sys
import subprocess
from luma.core import cmdline
from luma.core.virtual import terminal
from PIL import ImageFont

VIRTUAL_TERMINAL_DEVICE = "/dev/vcsa"
ROWS = 9
COLS = 31

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
    time.sleep(0.1)
    term.clear()
    for i in range(0, ROWS):
        term.puts(str(i) * COLS)
    term.flush()
    #time.sleep(1)

    while True:
        # Get terminal text; despite man page, `screendump` differs from reading vcs dev
        #data = file(VIRTUAL_TERMINAL_DEVICE).read()
        data = subprocess.check_output(["screendump"])
	print [data]

        # Try to avoid flashing - don't clear screen, only overwrite
        #term.clear()
        term._cx, term._cy = (0, 0)

        # puts() flushes on newline(), so reimplement it ourselves
        #term.puts(data)

        # character x position, can't seem to use term._cx / term._cw (width) since cw=6 but term.font.getsize('-')0] is 4??
        # TODO: even this isn't foolproof, spaces are smaller :(
        x = 0

        def padToNextLine():
            #print "cx / cw = ", (term._cx / term._cw), "cx=",term._cx, "cw=",term._cw
            #print term.font.getsize("_")[0]
            #print "COLS - cx/cw = " , (COLS - term._cx / term._cw)
            #term.puts("0123456789abc"[(term._cy / term._ch)] * (COLS - term._cx / term._cw))
            #term.puts("0123456789abc"[(term._cy / term._ch)] * (COLS - x))
            term.puts("_" * (COLS - x))

        for char in data:
            if char == '\r':
                #padToNextLine()
                term.carriage_return()
                x = 0
            elif char == '\n':
                #term.newline()
                # no scroll, no flush
                padToNextLine()
                term.carriage_return()
                x = 0
                term._cy += term._ch
            elif char == '\b':
                term.backspace()
                x =- 1
            elif char == '\t':
                #term.tab()
                # reimplemented to count tab width
                soft_tabs = term.tabstop - ((term._cx // term._cw) % term.tabstop)
                self.puts(" " * soft_tabs)
                x += len(soft_tabs)
            else:
                term.putch(char)
                x += 1
        #padToNextLine()

        term.flush()
        time.sleep(0.01)
        #print "refresh"
        #print data


if __name__ == "__main__":
    os.system("stty --file=/dev/console rows %d" % (ROWS,))
    os.system("stty --file=/dev/console cols %d" % (COLS,))
    try:
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass
