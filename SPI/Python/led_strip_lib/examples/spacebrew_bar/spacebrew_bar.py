#!/usr/bin/python
 
# Light painting / POV demo for Raspberry Pi using
# Adafruit Digital Addressable RGB LED flex strip.
# ----> http://adafruit.com/products/306

from struct import *
#import time
from spacebrew import SpaceBrew 
import RPi.GPIO as GPIO, Image, time
import random 
from led_strip import LEDStrip

# Configurable values
brightness  = 0.0
color 		= [0, 0, 0]
rangeMax    = 1023.0
pixels	    = 32
spidev	    = file("/dev/spidev0.0", "wb")

leds = LEDStrip(pixels=pixels, spi=spidev)

def map(value, sourceMin, sourceMax, targetMin, targetMax):
    # Figure out how 'wide' each range is
    sourceSpan = sourceMax - sourceMin
    targetSpan = targetMax - targetMin
    valueScaled = float(value - sourceMin) / float(sourceSpan)
    return targetMin + (valueScaled * targetSpan)

def updateStrip():
	for i in range(32):
		if i < ( brightness / rangeMax * pixels ): 
			leds.setPixelColorRGB(pixel=i, red=color[0] + 127, green=color[1] + 127, blue=color[2] + 127)
		else:
			leds.setPixelColorRGB(pixel=i, red=127, green=127, blue=127)
	leds.show()
	time.sleep(0.001)

def updateLight(bright):
	brightness = bright
	updateStrip()

	# for i in range(32):
	# 	newVal = 128
	# 	if i < ( brightness / rangeMax * pixels ): 
	# 		newVal = 255                    
	# 	leds.setPixelColorRGB(pixel=i, red=newVal, green=newVal, blue=newVal)
	# leds.show()
	# time.sleep(0.001)

def updateRed(red):
	color[0] = map(red, 0, 1023, 0, 127)
	updateStrip()

def updateGreen(green):
	color[1] = map(green, 0, 1023, 0, 127)
	updateStrip()

def updateBlue(blue):
	color[2] = map(blue, 0, 1023, 0, 127)
	updateStrip()

brew1 = SpaceBrew(("Pithon DATA BAR " + str(random.randint(0,2000))),server="sandbox.spacebrew.cc")
brew1.addSubscriber("light", "range")

# We call "subscribe" to associate a function with a subscriber.
brew1.subscribe("light",updateLight)
brew1.start()

print "Running..."

