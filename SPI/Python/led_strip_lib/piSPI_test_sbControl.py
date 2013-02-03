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
rangeMax    = 1023.0
pixels	    = 32
spidev	    = file("/dev/spidev0.0", "wb")

leds = LEDStrip(pixels=pixels, spi=spidev)

def updateLight(bright):
	for i in range(32):
		newVal = 128
		if i < ( bright / rangeMax * pixels ): 
			newVal = 255                    
		leds.setPixelColorRGB(pixel=i, red=newVal, green=newVal, blue=newVal)

	leds.show()
	time.sleep(0.001)


brew1 = SpaceBrew(("Pithon DATA BAR " + str(random.randint(0,2000))),server="sandbox.spacebrew.cc")
brew1.addSubscriber("light", "range")

# We call "subscribe" to associate a function with a subscriber.
brew1.subscribe("light",updateLight)
brew1.start()

print "Running..."

