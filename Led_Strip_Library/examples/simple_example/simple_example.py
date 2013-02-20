#!/usr/bin/python
 
# SIMPLE EXAMPLE :: EXAMPLE SKETCH
# 
# Example sketch for Raspberry Pi that scrolls the lights on and off on the
# LED bar. It uses the LED Strip Python library developed by the LAB at
# Rockwell Group for use with Adafruit's LPD8806 LED strips. 
# 
# Link to LED Strip: http://adafruit.com/products/306

from ledStrip import ledstrip
import time
import random 
import argparse

# Define app description and optional paramerters
parser = argparse.ArgumentParser(description='Example sketch that controls an LED strip via Spacesb. It uses the 	LED Strip Python library for Adafruit\'s LPD8806 LED strips.')

# Define the leds strip length optional parameter
parser.add_argument('-l', '--leds', '--pixels', 
					nargs=1, type=int, default=32,
					help='length of led strip in leds, or pixels')

# read all command line parameters
args = parser.parse_args()


# function that initializes all spacebrew and led strip object when script is run
def main():

	# initialize spi and leds objects
	spidev		= file("/dev/spidev0.0", "wb")  # ref to spi connection to the led bar
	leds 		= ledstrip.LEDStrip(pixels=args.leds, spi=spidev)

	pixel_edge = 0 	# current pixel whose state will be flipped
	turn_on = True  # holds whether pixel will be switched on or off

	print "Let's start chasing"

	while (True):
		# update the pixel at the edge of the animation
		if turn_on == True:
			leds.setPixelColorRGB(pixel=pixel_edge, red=127, green=127, blue=127)
		else:
			leds.setPixelColorRGB(pixel=pixel_edge, red=0, green=0, blue=0)
		# update all leds
		leds.show()

		# move the chase forward
		pixel_edge = (pixel_edge + 1) % leds.numPixels()
		# when pixel goes back to start of strip then switch from on to off, or off to on
		if pixel_edge == 0: turn_on = not turn_on 

		# delay for 20 milliseconds
		time.sleep(0.02)

if __name__ == "__main__":
	main()
