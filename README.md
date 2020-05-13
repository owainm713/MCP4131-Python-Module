# MCP4131-Python-Module
Python 3.x  module for use with MCP4131 digital potentiometer. 

This requires the py-spidev and python-dev modules for the SPI connection. I used an MCP4131
10kOhm digital pot connected to a Raspberry Pi 3 for development of this module.

Connections to the MCP4131 from the Pi are as follows

- Pi MOSI to 560 ohm resistor to MCP SDI/SDO
- Pi MISO to MCP SDI/SDO
- Pi SCLK to MCP SCK
- Pi CE1 to MCP CS
- Pi 3.3V to MCP Vdd
- Pi Gnd to MCP Gnd/Vss

For testing I used a Fluke7 3 Series II multimeter measuring ohms placed across the MCP P0B
and MCP P0W terminals

Current functions include:
- set_wiper_value(wiperValue = 0x40, wiper = 0):=
- read_wiper_value(wiper = 0)
- increment_wiper(increment = 1, wiper = 0)
- decrement_wiper(decrement = 1, wiper = 0)
- set_wiper_controls(pA = 1, pW = 1, pB= 1, shutdown = 1, wiper = 0)
- read_wiper_controls()

For information on how the chip works check out the datasheet

Note: 
For the increment and decrement commands I did not use the 8 bit increment/decrement 
commands found in the data sheet. They never worked for me, on the Pi or on an Arduino UNO.
I used a 2 step version instead where I read the current wiper value first and then increment/decrement
that by the specified amount and write that value back to the wiper value register. 