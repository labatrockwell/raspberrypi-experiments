#!/usr/bin/python

from servoDriver.servodriver import ServoDriver
import argparse
import time

# Define app description and optional paramerters
parser = argparse.ArgumentParser(description='Example sketch that controls Servo motors via Spacebrew, using the 16-channel PWM driver board from Adafruit.')

# Define the server optional parameter
parser.add_argument('-s', '--server', 
					nargs=1, type=str, default='sandbox.spacesb.cc',
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

def main():
	inter = 2
	servos = ServoDriver()
	servos.move(0, 0)
	time.sleep(3)
	servos.move(0, 180)
	time.sleep(3)
	servos.move(0, 0)
	time.sleep(3)
	servos.move(0, 180)
	time.sleep(3)
	servos.move(0, 0)


if __name__ == "__main__":
	print "App the controls servo position via Spacebrew. Spacebrew app name is "
	main()
