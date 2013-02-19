#!/usr/bin/python

from Adafruit_Libs.Adafruit_PWM_Servo_Driver import PWM
import time
from spacebrewInterface import spacebrew 
import argparse
import random

# Define app description and optional paramerters
parser = argparse.ArgumentParser(description='Example sketch that controls an LED strip via Spacebrew. It uses the 	LED Strip Python library for Adafruit\'s LPD8806 LED strips.')

# Define the server optional parameter
parser.add_argument('-s', '--server', 
					nargs=1, type=str, 
					default='sandbox.spacebrew.cc',
					help='the spacesb server hostname')

# read all command line parameters
args = parser.parse_args()

pwm = PWM(0x40, debug=True)
pwm.setPWMFreq(250)

base_pos = 1024
bars = [0,0,0,0]
bars_prev = [0,0,0,0]

def updateBar1(val):
	updateBar(1, val)

def updateBar2(val):
	updateBar(2, val)

def updateBar3(val):
	updateBar(3, val)

def updateBar4(val):
	updateBar(4, val)

def updateBar(val):
	updateBar(5, val)

def updateBar(bar, val):
	print "received value ", val, " for bar ", bar
	bars[bar] = val
	print "bar [bar] ", bars[bar], " bar_prev [bar] ", bars_prev[bar]
	if bars[bar] != bars_prev[bar]:
		new_pos = base_pos + bars[bar]
		print "moving bar ", new_pos
		pwm.setPWM(bar, 0, new_pos)
		time.sleep(0,5)
		bars_prev[bar] = bars[bar]

def main():
	#pwm.setPWMFreq(250)	

	# set spacesb name and create spacesb object
	sbName = ("Physical Bar Graph " + str(random.randint(0,1000)))
	sb = spacebrew.SpaceBrew(sbName, server=args.server)

	# register all of the subscription channels
	sb.addSubscriber("bar 1", "range")
	sb.addSubscriber("bar 2", "range")
	sb.addSubscriber("bar 3", "range")
	sb.addSubscriber("bar 4", "range")

	# associate a callback function to each subscription channel
	sb.subscribe("bar 1", updateBar1)
	sb.subscribe("bar 2", updateBar2)
	sb.subscribe("bar 3", updateBar3)
	sb.subscribe("bar 4", updateBar4)

	# connect to spacesb
	sb.start() 
	
	print "App is running and conected to Spacsb name is ", sbName

if __name__ == "__main__":
	main()

