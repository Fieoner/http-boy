#!/usr/bin/env python

import sys
sys.path.append('PyBoy/Source')
import os
import traceback
import glob
from PyBoy.WindowEvent import WindowEvent
from PyBoy import PyBoy
from PIL import Image
from PyBoy.GameWindow import SdlGameWindow as Window

class Emulator:

    def __init__(self):
        bootROM = None
        ROMdir = "ROM/"
        scale = 2
        try:
            # Check if the ROM is given through argv
            if len(sys.argv) > 1:
                filename = sys.argv[1]
            else:
                filename = self.getROM(ROMdir)

            # Start PyBoy and run loop
            self.pyboy = PyBoy(Window(scale=scale), filename, bootROM)


        except Exception:
            traceback.print_exc()
    

    def getROM(self, ROMdir):
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

    def ticks(self, n):
        for i in range(0, n):
            self.pyboy.tick()
       

    def gamestart(self):
        print("> Game starting...")
        cartridge = self.pyboy.mb.cartridge.filename.split('/')[-1:][0]
        print("> Loading {0}".format(cartridge))
        # ticks(pyboy, 100)
        # pyboy.mb.buttonEvent([WindowEvent.LoadState])
        self.pyboy.mb.loadState("STATES/{0}.state".format(cartridge))
        self.pyboy.tick()
        self.pyboy.sendInput([WindowEvent.PressButtonA])
        self.pyboy.tick()
        self.pyboy.sendInput([WindowEvent.ReleaseButtonA])
        self.ticks(250)

    def savegame(self):
        list_of_files = glob.glob("STATES/*.state")
        list_of_files.sort()
        cartridge = self.pyboy.mb.cartridge.filename.split('/')[-1:][0]
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
        self.pyboy.mb.saveState("STATES/"+savefile)

    def resumegame(self):
        list_of_files = glob.glob("STATES/*.state")
        list_of_filenames = map(lambda fullpath: fullpath.split('/')[-1:][0],
                                list_of_files)
        list_of_filenames.sort()
        cartridge = self.pyboy.mb.cartridge.filename.split('/')[-1:][0]
        counter = "00000"
        savefile = cartridge + counter + ".state"
        if savefile not in list_of_filenames:
            self.gamestart()
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
        self.pyboy.mb.loadState("STATES/"+savefile)



    def presskey(self, key):
        keys = {"up":[[WindowEvent.PressArrowUp],[WindowEvent.ReleaseArrowUp]],
        "down":[[WindowEvent.PressArrowDown],[WindowEvent.ReleaseArrowDown]],
        "left":[[WindowEvent.PressArrowLeft],[WindowEvent.ReleaseArrowLeft]],
        "right":[[WindowEvent.PressArrowRight],[WindowEvent.ReleaseArrowRight]],
        "a":[[WindowEvent.PressButtonA],[WindowEvent.ReleaseButtonA]],
        "b":[[WindowEvent.PressButtonB],[WindowEvent.ReleaseButtonB]],
        "start":[[WindowEvent.PressButtonStart],[WindowEvent.ReleaseButtonStart]],
        "select":[[WindowEvent.PressButtonSelect],[WindowEvent.ReleaseButtonSelect]]}
        self.pyboy.sendInput(keys[key][0])
        self.ticks(10)
        self.pyboy.sendInput(keys[key][1])
        self.ticks(200)
        self.savegame()


    def getScreenshot(self):
        screenshot = self.pyboy.window.getScreenBuffer()
        im = Image.new('RGBA', (288, 320))
        pixellist = []
        for line in screenshot:
            for pixel in line:
                pixelstring = str(hex(pixel))
                if len(pixelstring) < 8:
                    pixelstring = "0x" + ('0'*(8-len(pixelstring))) + pixelstring[2:]
                r = int(pixelstring[2:4], 16)
                g = int(pixelstring[4:6], 16)
                b = int(pixelstring[6:8], 16)
                pixellist.append((r, g, b))
        im.putdata(pixellist)
        transposed = im.transpose(Image.TRANSPOSE)
        return transposed

    def read(self, address):
        return self.pyboy.getMemoryValue(address)

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
