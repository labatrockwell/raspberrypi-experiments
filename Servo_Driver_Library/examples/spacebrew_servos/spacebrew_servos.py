#!/usr/bin/python
 
# SPACEBREW SERVOS :: EXAMPLE SKETCH
# Example sketch for Raspberry Pi that controls two servos via Spacebrew. 
# It uses the 16-Channel PWM Driver from Adafruit. 
# 
# Link to LED Strip: http://adafruit.com/products/306

from spacebrewInterface import spacebrew 
from servoDriver.servodriver import ServoDriver
import time
import random 
import argparse

# Define app description and optional paramerters
parser = argparse.ArgumentParser(description='Example sketch that controls a Servo motors using the 16-channel PWM driver board from Adafruit.')

# Define the server optional parameter
parser.add_argument('-s', '--server', 
					nargs=1, type=str, 
					default='sandbox.spacebrew.cc',
					help='the spacesb server hostname')

# Define the leds strip length optional parameter
parser.add_argument('-b', '--begin', 
					nargs=1, type=int, default=140,
					help='length of pulse in nanoseconds when servo is at beginning pos, 0 degrees')

# Define the leds strip length optional parameter
parser.add_argument('-e', '--end', 
					nargs=1, type=int, default=650,
					help='length of pulse in nanoseconds when servo is at end pos, 180 degrees')

parser.add_argument('-a', '--address', 
					nargs=1, type=int, default=0x40,
					help='i2c address of the 16-channel PWM driver')

# read all command line parameters
args = parser.parse_args()

# initialize variables
servos		= {}							# ref to spacebrew object
rotating = False

# function that maps value to a new range
def map(value, sourceMin, sourceMax, targetMin, targetMax):
	sourceSpan = sourceMax - sourceMin
	targetSpan = targetMax - targetMin
	valueScaled = float(value - sourceMin) / float(sourceSpan)
	updatedVal = targetMin + (valueScaled * targetSpan)
	return int(updatedVal)

# handles data from "light" spacebrew channel
def rotate(on):
	global servos, rotating
	if rotating == True:
		print "stop"
		servos.move(0, 0)
		rotating = False
	else:
		print "start"
		servos.move(0, 100)
		rotating = True

def position(pos):
	global servos
	print "got new position ", pos
	pos = map(pos, 0, 1024, 0, 180)
	pos -= 90
	servos.move(1, pos)

# function that initializes all spacebrew and led strip object when script is run
def main():
	# identify global variables that we will access in this function
	global servos, sb

	# create an instance of LEDStrip object - pass number of pixels and link to spi connection
	servos = ServoDriver()
	servos.continous(0)
	servos.calibrateCont(0, 8150)

	# set spacesb name and create spacesb object
	sbName = ("Servo Control " + str(random.randint(0,2000)))
	sb = spacebrew.SpaceBrew(sbName, server=args.server)

	# register all of the subscription channels
	sb.addSubscriber("rotate", "boolean")
	sb.addSubscriber("position", "range")

	# associate a callback function to each subscription channel
	sb.subscribe("rotate", rotate)
	sb.subscribe("position", position)

	# connect to spacesb
	sb.start() 

	print "App is running and conected to Spacebrew name is ", sbName

if __name__ == "__main__":
	main()
