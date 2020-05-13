#!/usr/bin/env python3
"""MCP4131, module for use with a MCP4131 digital potentiometer

created May 12, 2020 OM
modified May 12, 2020 OM"""

"""
Copyright 2020 Owain Martin

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import time, spidev

class MCP4131:

    def __init__(self, spiPort = 0, spiCS = 0):

        self.spi=spidev.SpiDev()
        self.spi.open(spiPort,spiCS)
        self.spi.mode = 0b00
        self.spi.max_speed_hz = 4000000       

        return

    def set_wiper_value(self, wiperValue = 0x40, wiper = 0):
        """set_wiper_value, function to set the value of the given wiper
        to value between 0 and 128"""

        # for 16 bit/2 byte commands format is
        # AD3, AD2, AD1, AD0, C1, C0, D9-D0
        # write to wiper 0 register 0h
        # MCP4131 has 7 bit wiper register with 128
        # different values (0x00 to 0x80)
        # for write commands C1, C0 = 0,0

        wiperValue = int(wiperValue)

        byte1 = (wiper<<4) + (0b00<<2) + 0b00    

        if wiperValue >= 128:
            byte2 = 128        
        elif wiperValue < 0:
            byte2 = 0
        else:
            byte2 = wiperValue

        #print(wiperValue, hex(byte1), hex(byte2)) # for testing

        dataTransfer = self.spi.xfer2([byte1, byte2])    

        return

    def read_wiper_value(self, wiper = 0):
        """read_wiper, function to read the current wiper
        value"""

        # for read commands with SDO/SDI multiplexed
        # D7-D0 need to be set to all 1s so
        # SD0/MISO data can be read properly
        # for read commands C1, C0 = 1,1

        byte1 = (wiper<<4) + (0b11<<2) + 0b00
        byte2 = 0xFF

        #print(hex(byte1), hex(byte2))

        dataTransfer = self.spi.xfer2([byte1, byte2])   

        return dataTransfer[1]

    def increment_wiper(self, increment = 1, wiper = 0):
        """increment_wiper, function to increment the
        current wiper value by the increment amount passed,
        default of 1"""

        currentWiperValue = self.read_wiper_value(wiper)

        newWiperValue = currentWiperValue + increment

        self.set_wiper_value(newWiperValue, wiper)

        return

    def decrement_wiper(self, decrement = 1, wiper = 0):
        """decrement_wiper, function to decrement the
        current wiper value by the decrement amount passed,
        default of 1"""

        currentWiperValue = self.read_wiper_value(wiper)

        newWiperValue = currentWiperValue - decrement

        self.set_wiper_value(newWiperValue, wiper)

        return

    def set_wiper_controls(self, pA = 1, pW = 1, pB= 1, shutdown = 1, wiper = 0):
        """set_wiper_controls, function to set the controls bits in the
        TCON register(0x4h) for the given wiper"""

        byte1 = 0x40

        # read current TCON value in
        dataTransfer = self.spi.xfer2([0x4C, 0xFF])
        byte2 = dataTransfer[1]    

        if wiper == 0:        
            byte2 = byte2 & 0xF0
            byte2 = byte2 | ((shutdown<<3) + (pA<<2) + (pW<<1) + pB)

        else:        
            byte2 = byte2 & 0x0F
            byte2 = byte2 | ((shutdown<<7) + (pA<<6) + (pW<<5) + (pB<<4))
        
        #print(hex(byte2))

        # write value to TCON register
        dataTransfer = self.spi.xfer2([byte1, byte2])    

        return

    def read_wiper_controls(self):
        """read_wiper_controls, function to read the wiper control bits
        in the TCON register (0x4h)"""

        # read current TCON value in
        dataTransfer = self.spi.xfer2([0x4C, 0xFF])

        return dataTransfer[1]

if __name__ == "__main__":

    dPOT = MCP4131(0,1)

    dPOT.set_wiper_value()
    print(dPOT.read_wiper_value())
    time.sleep(3)
    dPOT.set_wiper_value(128)
    print(dPOT.read_wiper_value())
    time.sleep(3)
    dPOT.set_wiper_value(0)
    print(dPOT.read_wiper_value())
    time.sleep(3)
    dPOT.set_wiper_value(65)
    print(dPOT.read_wiper_value(0))
    time.sleep(3)

    
    for i in range(0,10):
        dPOT.increment_wiper()
        print(dPOT.read_wiper_value(0))
        time.sleep(2)

    for i in range(0,10):
        dPOT.decrement_wiper(5)
        print(dPOT.read_wiper_value(0))
        time.sleep(2)
    

    print(hex(dPOT.read_wiper_controls()))
    dPOT.set_wiper_controls(0,1,0)
    print(hex(dPOT.read_wiper_controls()))
    dPOT.set_wiper_controls(pW = 0, wiper = 1) # No visible effect on an MCP4131 as there is only 1 resistor network
    print(hex(dPOT.read_wiper_controls()))
    time.sleep(2)
    dPOT.set_wiper_controls(1,1,1,1,0)
    dPOT.set_wiper_controls(1,1,1,1,1)
    print(hex(dPOT.read_wiper_controls()))
        
