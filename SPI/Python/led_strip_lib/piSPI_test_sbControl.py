#!/usr/bin/python
 
# Light painting / POV demo for Raspberry Pi using
# Adafruit Digital Addressable RGB LED flex strip.
# ----> http://adafruit.com/products/306

from struct import *
import time
from spacebrew import SpaceBrew 
import RPi.GPIO as GPIO, Image, time
import random 
from led_strip import LEDStrip


# Configurable values
# filename  = "test.png"
dev         = "/dev/spidev0.0"
brightness  = 0.0
rangeMax    = 1023.0
pixels      = 32
spidev    = file(dev, "wb")

# 
brew1 = SpaceBrew(("Pithon DATA BAR " + str(random.randint(0,2000))),server="sandbox.spacebrew.cc")
brew1.addPublisher("pub", "range")
brew1.addSubscriber("light", "range")

leds = LEDStrip(pixels=pixels, spi=spidev)

# Here's a simple example of a function that recieves a value.
#def example(value):
#	print "Got", value
#	updateLight(value)
# We call "subscribe" to associate a function with a subscriber.
#brew1.subscribe("light",updateLight)
#brew1.start()
#column = bytearray(height * 3 + 1)
 
# Then it's a trivial matter of writing each column to the SPI port.
#print "Displaying..."

def updateLight(bright):
	#print "set brightness ", bright
        #print "       leds on  ", ( bright / rangeMax * height) 

	print "fucking range: ", range(pixels)

	for i in range(32):
		print "updating pixel number ", i, " from ", pixels
		newVal = 128
		if i < ( bright / rangeMax * pixels ): 
			newVal = 255                    

		leds.setPixelColorRGB(pixel=i, red=newVal, green=newVal, blue=newVal)

		# y3 = y * 3
		# column[y3] = newVal
		# column[y3 + 1] = newVal
		# column[y3 + 2] = newVal

	print "show pixels"
	leds.show()
	# spidev.write(column)
	# spidev.flush()
	time.sleep(0.001)

# We call "subscribe" to associate a function with a subscriber.
brew1.subscribe("light",updateLight)

brew1.start()

#column = bytearray(height * 3 + 1)

# Then it's a trivial matter of writing each column to the SPI port.
print "Displaying..."

