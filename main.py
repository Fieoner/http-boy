#!/usr/bin/env python

import sys
sys.path.append('PyBoy/Source')
import os
import traceback
from PyBoy.WindowEvent import WindowEvent
from PyBoy import PyBoy
from PyBoy.GameWindow import SdlGameWindow as Window

def getROM(ROMdir):
    # Give a list of ROMs to start
    found_files = filter(lambda f: f.lower().endswith(
        ".gb") or f.lower().endswith(".gbc"), os.listdir(ROMdir))
    for i, f in enumerate(found_files):
        print ("%s\t%s" % (i + 1, f))
    filename = raw_input("Write the name or number of the Pokemon Blue ROM file:\n")

    try:
        filename = ROMdir + found_files[int(filename) - 1]
    except:
        filename = ROMdir + filename

    return filename


def main():
    bootROM = None
    ROMdir = "ROM/"
    scale = 2
    try:
        # Check if the ROM is given through argv
        if len(sys.argv) > 1:
            filename = sys.argv[1]
        else:
            filename = getROM(ROMdir)

        # Start PyBoy and run loop
        pyboy = PyBoy(Window(scale=scale), filename, bootROM)
        frame = 0
        view = pyboy.getTileView(False)
        while not pyboy.tick():
            print("frame: " + str(frame))

            frame += 1
        pyboy.stop()

    except KeyboardInterrupt:
        print ("Interrupted by keyboard")
    except Exception as ex:
        traceback.print_exc()

if __name__ == '__main__':
    main()
