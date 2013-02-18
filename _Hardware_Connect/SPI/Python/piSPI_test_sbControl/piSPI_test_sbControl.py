#!/usr/bin/python
 
# Light painting / POV demo for Raspberry Pi using
# Adafruit Digital Addressable RGB LED flex strip.
# ----> http://adafruit.com/products/306

from struct import *
import time
from spacebrew import SpaceBrew 
import RPi.GPIO as GPIO, Image, time
import random 


# Configurable values
# filename  = "test.png"
dev		 = "/dev/spidev0.1"
brightness  = 0.0
rangeMax	= 1023.0
height	  = 32

spidev	= file(dev, "wb")

# 
brew1 = SpaceBrew(("Pithon DATA BAR " + str(random.randint(0,2000))),server="sandbox.spacebrew.cc")
brew1.addPublisher("pub", "range")
brew1.addSubscriber("light", "range")

# Here's a simple example of a function that recieves a value.
def example(value):
	print "Got", value
	updateLight(value)

# We call "subscribe" to associate a function with a subscriber.
brew1.subscribe("light",example)

brew1.start()
 
column = bytearray(height * 3 + 1)
 
# Then it's a trivial matter of writing each column to the SPI port.
print "Displaying..."

def updateLight(bright):
	print "set brightness ", bright
	print "	   leds on  ", ( bright / rangeMax * height) 

	for y in range(height):
		y3 = y * 3
		newVal = 128
		if y < ( bright / rangeMax * height):
			newVal = 255					

		column[y3] = newVal
				column[y3 + 1] = newVal
				column[y3 + 2] = newVal

	spidev.write(column)
	spidev.flush()
	time.sleep(0.001)
