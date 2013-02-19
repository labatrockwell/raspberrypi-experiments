#!/usr/bin/python
 
# SPACEBREW BAR :: EXAMPLE SKETCH
# Example sketch for Raspberry Pi that controls an LED strip via Spacesb. 
# It uses the LED Strip Python library for Adafruit's LPD8806 LED strips. 
# 
# Link to LED Strip: http://adafruit.com/products/306

from spacebrewInterface import spacebrew 
from ledStrip import ledstrip
import RPi.GPIO as GPIO
import time
import random 
import argparse

# Define app description and optional paramerters
parser = argparse.ArgumentParser(description='Example sketch that controls an LED strip via Spacesb. It uses the 	LED Strip Python library for Adafruit\'s LPD8806 LED strips.')

# Define the server optional parameter
parser.add_argument('-s', '--server', 
					nargs=1, type=str, 
					default='sandbox.spacebrew.cc',
					help='the spacesb server hostname')

# Define the leds strip length optional parameter
parser.add_argument('-l', '--leds', '--pixels', 
					nargs=1, type=int, default=32,
					help='length of led strip in leds, or pixels')

# read all command line parameters
args = parser.parse_args()

# initialize variables
brightness  	= 0.0 				# current brightness state (used to determine how many leds should be on)
color 		= [127, 127, 127]	# RGB color used for all pixels
rangeMax	= 1023.0 			# maximum incoming range values
pixels		= args.leds			# number of pixels 
spidev		= file("/dev/spidev0.0", "wb")  # link to spi connection to the led bar
leds 		= {}
sb		= {}

def map(value, sourceMin, sourceMax, targetMin, targetMax):
	sourceSpan = sourceMax - sourceMin
	targetSpan = targetMax - targetMin
	valueScaled = float(value - sourceMin) / float(sourceSpan)
	updatedVal = targetMin + (valueScaled * targetSpan)
	return int(updatedVal)

def updateStrip():
	global brightness, color, rangeMax, pixels, leds
	cur_bright = (brightness / rangeMax * pixels)
	for i in range(32):
		if i < cur_bright: 
			leds.setPixelColorRGB(pixel=i, red=color[0], green=color[1], blue=color[2])
		else:
			leds.setPixelColorRGB(pixel=i, red=128, green=128, blue=128)
	leds.show()
	#time.sleep(0.001)

def updateLight(bright):
	global brightness
	brightness = bright
	updateStrip()

def updateRed(red):
	global color
	color[0] = map(red, 0, rangeMax, 0, 127) + 128
	updateStrip()

def updateGreen(green):
	global color
	color[1] = map(green, 0, rangeMax, 0, 127) + 128
	updateStrip()

def updateBlue(blue):
	global color
	color[2] = map(blue, 0, rangeMax, 0, 127) + 128
	updateStrip()

def main():
	global leds, sb

	# create an instance of LEDStrip object - pass number of pixels and link to spi connection
	leds = ledstrip.LEDStrip(pixels=pixels, spi=spidev)

	# set spacesb name and create spacesb object
	sbName = ("Data Bar " + str(random.randint(0,2000)))
	sb = spacebrew.SpaceBrew(sbName, server=args.server)

	# register all of the subscription channels
	sb.addSubscriber("light", "range")
        sb.addSubscriber("color_red", "range")
	sb.addSubscriber("color_green", "range")
	sb.addSubscriber("color_blue", "range")

	# associate a callback function to each subscription channel
	sb.subscribe("light", updateLight)
	sb.subscribe("color_red", updateRed)
	sb.subscribe("color_green", updateGreen)
	sb.subscribe("color_blue", updateBlue)

	# connect to spacesb
	sb.start() 

	print "App is running and conected to Spacebrew name is ", sbName

if __name__ == "__main__":
	main()
