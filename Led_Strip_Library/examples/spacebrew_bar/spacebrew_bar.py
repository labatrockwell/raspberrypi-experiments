#!/usr/bin/python
 
# Light painting / POV demo for Raspberry Pi using
# Adafruit Digital Addressable RGB LED flex strip.
# ----> http://adafruit.com/products/306

from struct import *
from spacebrew import SpaceBrew 
from LAB_Led_Strip import LEDStrip
import RPi.GPIO as GPIO, Image, time
import random 

# Configurable values
brightness  = 0.0 		   # current brightness state (used to determine how many leds should be on)
color 	    = [127, 127, 127]	   # RGB color used for all pixels
rangeMax    = 1023.0		   # maximum incoming range values
pixels	    = 32		   # number of pixels 
spidev	    = file("/dev/spidev0.0", "wb")  # link to spi connection to the led bar

# create an instance of LEDStrip object - pass number of pixels and link to spi connection
leds = LEDStrip(pixels=pixels, spi=spidev)

def map(value, sourceMin, sourceMax, targetMin, targetMax):
	sourceSpan = sourceMax - sourceMin
	targetSpan = targetMax - targetMin
	valueScaled = float(value - sourceMin) / float(sourceSpan)
	updatedVal = targetMin + (valueScaled * targetSpan)
	return int(updatedVal)

def updateStrip():
	global brightness
	global color
	for i in range(32):
		if i < ( brightness / rangeMax * pixels ): 
			leds.setPixelColorRGB(pixel=i, red=color[0], green=color[1], blue=color[2])
		else:
			leds.setPixelColorRGB(pixel=i, red=128, green=128, blue=128)

	leds.show()
	time.sleep(0.001)

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

# set spacebrew name and create spacebrew object
brewName = ("Pithon DATA BAR " + str(random.randint(0,2000)))
brew1 = SpaceBrew(brewName, server="sandbox.spacebrew.cc")

# register all of the subscription channels
brew1.addSubscriber("light", "range")
brew1.addSubscriber("color_red", "range")
brew1.addSubscriber("color_green", "range")
brew1.addSubscriber("color_blue", "range")

# associate a callback function to each subscription channel
brew1.subscribe("light", updateLight)
brew1.subscribe("color_red", updateRed)
brew1.subscribe("color_green", updateGreen)
brew1.subscribe("color_blue", updateBlue)

# connect to spacebrew
brew1.start() 

print "App is running"
print "Spacbrew name is ", brewName
