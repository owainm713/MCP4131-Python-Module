#!/usr/bin/env python3
"""MCP4131example, example program to use with a MCP4131.py module

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

import MCP4131
import time

dPOT = MCP4131.MCP4131(0,1)

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


for i in range(0,5):
    dPOT.increment_wiper()
    print(dPOT.read_wiper_value(0))
    time.sleep(2)

for i in range(0,5):
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
