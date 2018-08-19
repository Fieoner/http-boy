#!/usr/bin/env python

import sys
sys.path.append('PyBoy/Source')
import os
import traceback
import glob
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

def ticks(pyboy, n):
    for i in range(0, n):
        pyboy.tick()

def init_emulator():
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
        return PyBoy(Window(scale=scale), filename, bootROM)


    except Exception as ex:
        traceback.print_exc()

def gamestart(pyboy):
    print("> Game starting...")
    cartridge = pyboy.mb.cartridge.filename.split('/')[-1:][0]
    print("> Loading {0}".format(cartridge))
    # ticks(pyboy, 100)
    # pyboy.mb.buttonEvent([WindowEvent.LoadState])
    pyboy.mb.loadState("STATES/{0}.gb.state".format(cartridge))
    pyboy.tick()
    pyboy.sendInput([WindowEvent.PressButtonA])
    pyboy.tick()
    pyboy.sendInput([WindowEvent.ReleaseButtonA])
    ticks(pyboy, 250)

def savegame(pyboy):
    list_of_files = glob.glob("STATES/*.state")
    list_of_files.sort()
    cartridge = pyboy.mb.cartridge.filename.split('/')[-1:][0]
    counter = "00000"
    savefile = cartridge + counter + ".state"
    for file in list_of_files:
        actualname = file.split('/')[-1:][0]
        if savefile == actualname:
            intcounter = int(counter)
            intcounter += 1
            counter = str(intcounter)
            if len(counter) < 5:
                counter = "0"*(5-len(counter)) + counter
            savefile = cartridge + counter + ".state"
    pyboy.mb.saveState("STATES/"+savefile)

def resumegame(pyboy):
    list_of_files = glob.glob("STATES/*.state")
    list_of_filenames = map(lambda fullpath: fullpath.split('/')[-1:][0],
                            list_of_files)
    list_of_filenames.sort()
    cartridge = pyboy.mb.cartridge.filename.split('/')[-1:][0]
    counter = "00000"
    savefile = cartridge + counter + ".state"
    if savefile not in list_of_filenames:
        gamestart(pyboy)
        return
    for file in list_of_filenames:
        if savefile == file:
            intcounter = int(counter)
            intcounter += 1
            counter = str(intcounter)
            if len(counter) < 5:
                counter = "0"*(5-len(counter)) + counter
            savefile = cartridge + counter + ".state"
    counter = str(int(counter)-1)
    counter = "0"*(5-len(counter)) + counter
    savefile = cartridge + counter + ".state"
    print(savefile)
    pyboy.mb.loadState("STATES/"+savefile)



def presskey(pyboy, key):
    keys = {"up":[[WindowEvent.PressArrowUp],[WindowEvent.ReleaseArrowUp]],
    "down":[[WindowEvent.PressArrowDown],[WindowEvent.ReleaseArrowDown]],
    "left":[[WindowEvent.PressArrowLeft],[WindowEvent.ReleaseArrowLeft]],
    "right":[[WindowEvent.PressArrowRight],[WindowEvent.ReleaseArrowRight]],
    "a":[[WindowEvent.PressButtonA],[WindowEvent.ReleaseButtonA]],
    "b":[[WindowEvent.PressButtonB],[WindowEvent.ReleaseButtonB]],
    "start":[[WindowEvent.PressButtonStart],[WindowEvent.ReleaseButtonStart]],
    "select":[[WindowEvent.PressButtonSelect],[WindowEvent.ReleaseButtonSelect]]}
    pyboy.sendInput(keys[key][0])
    ticks(pyboy, 10)
    pyboy.sendInput(keys[key][1])
    ticks(pyboy, 200)
    savegame(pyboy)

# def main():
#     bootROM = None
#     ROMdir = "ROM/"
#     scale = 2
#     try:
#         # Check if the ROM is given through argv
#         if len(sys.argv) > 1:
#             filename = sys.argv[1]
#         else:
#             filename = getROM(ROMdir)
#
#         # Start PyBoy and run loop
#         pyboy = PyBoy(Window(scale=scale), filename, bootROM)
#         frame = 0
#         view = pyboy.getTileView(False)
#         while not pyboy.tick():
#             print("frame: " + str(frame))
#
#             frame += 1
#         pyboy.stop()
#
#     except KeyboardInterrupt:
#         print ("Interrupted by keyboard")
#     except Exception as ex:
#         traceback.print_exc()
