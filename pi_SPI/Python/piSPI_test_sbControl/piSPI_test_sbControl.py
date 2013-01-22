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
dev         = "/dev/spidev0.0"
brightness  = 0.0
rangeMax    = 1023.0
height      = 32

spidev    = file(dev, "wb")

# 
brew1 = SpaceBrew(("Pithon DATA BAR " + str(random.randint(0,2000))),server="sandbox.spacebrew.cc")
brew1.addPublisher("pub", "range")
brew1.addSubscriber("light", "range")

# Here's a simple example of a function that recieves a value.
def example(value):
	print "Got", value
	updateLight(value)
#    ser.write(pack('B',value/4))

# We call "subscribe" to associate a function with a subscriber.
brew1.subscribe("light",example)

brew1.start()
 
# Open SPI device, load image in RGB format and get dimensions:
#spidev    = file(dev, "wb")
#print "Loading..."
# img       = Image.open(filename).convert("RGB")
# pixels    = img.load()
# width     = img.size[0]
#height    = img.size[1]
#print "%dx%d pixels" % img.size
# To do: add resize here if image is not desired height
 
# Calculate gamma correction table.  This includes
# LPD8806-specific conversion (7-bit color w/high bit set).
#gamma = bytearray(256)
#for i in range(256):
#	gamma[i] = 0x80 | int(pow(float(i) / 255.0, 2.5) * 127.0 + 0.5)
 
# Create list of bytearrays, one for each column of image.
# R, G, B byte per pixel, plus extra '0' byte at end for latch.
#print "Allocating..."
#column = [0 for x in range(width)]
#for x in range(width):
#	column[x] = bytearray(height * 3 + 1)
column = bytearray(height * 3 + 1)
 
# Convert 8-bit RGB image into column-wise GRB bytearray list.
#print "Converting..."
#for x in range(width):
#for y in range(height):
#	if (y < (bright/range * height):
#		column[y] = 255
#	else:
#		column[y] = 0
		
#	print "R: ", column[x][y3], " G: ", column[x][y3 + 1], " B: ", column[x][y3 + 2]
 
# Then it's a trivial matter of writing each column to the SPI port.
print "Displaying..."
#while True:
#	brightness = random.random() * rangeMax	

def updateLight(bright):
	print "set brightness ", bright
        print "       leds on  ", ( bright / rangeMax * height) 

	for y in range(height):
		y3 = y * 3
		newVal = 128
		if y < ( bright / rangeMax * height):
			newVal = 255                    

		column[y3] = newVal
                column[y3 + 1] = newVal
                column[y3 + 2] = newVal
#		print "pixel val ",  column[y]


#	for x in range(width):
	spidev.write(column)
	spidev.flush()
	time.sleep(0.001)
#	for y in range(32):
#		y3 = y * 3
#		print "display: ", column[x][y3], column[x][y3+1], column[x][y3 + 2]

#	time.sleep(1)
