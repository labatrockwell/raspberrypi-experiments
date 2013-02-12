#!/usr/bin/env python

import cv
import platform
import numpy as np
import time
import sys
import argparse

from SbLink import SbLink

client = False


WIDTH = 240
HEIGHT = 135
arch = platform.architecture()
if arch[0] == '32bit' and arch[1] == 'ELF' :
	# assume rpi, drop the wide format support
	WIDTH = 160
	HEIGHT = 120

# since we only do a non-zero test, this is arbitrary
MAX_PIXEL_VAL = 255

state = None
rectangle = None
tempRectangle = None

parser = argparse.ArgumentParser(description='Python based Region of Interest ROI sensor, RPI tested!')
parser.add_argument('name', 
					type=str,
				    help='The name of this client/sensor that will show in spacebrew',
				    metavar='sensor01')

parser.add_argument('-c', '--client', 
					help="Configure script to operate as a client to adjust/monitor sensors rather than act as a sensor.",
					action='store_true')

parser.add_argument('-v', '--visual',
					help="Show all 4 sensor windows, sensor mode only",
					action='store_true')

args = parser.parse_args()

print args

sbLink = SbLink(thresholdCutoff   = 20, 
			    learnRate 		  = 0.1, 
				constantMessaging = False, 
			    percentageFill    = 0.2)


def mouseCallback(event, x, y, flags, param):
	global state
	global rectangle
	global tempRectangle
	
	if event == cv.CV_EVENT_LBUTTONDOWN:
		state = "DOWN"
		tempRectangle = [x, y, x, y]
		rectangle = None
		
	elif event == cv.CV_EVENT_LBUTTONUP:
		if state != "DOWN" :
			pass

		state = None
		rectangle = tempRectangle
		tempRectangle = None

	elif event == cv.CV_EVENT_MOUSEMOVE:
		if state == "DOWN" :
			tempRectangle[2] = x
			tempRectangle[3] = y
			

capture = cv.CaptureFromCAM(-1)

cv.SetCaptureProperty( capture, cv.CV_CAP_PROP_FRAME_WIDTH, WIDTH )
cv.SetCaptureProperty( capture, cv.CV_CAP_PROP_FRAME_HEIGHT, HEIGHT )

accumulator32f =    cv.CreateImage( (WIDTH, HEIGHT), cv.IPL_DEPTH_32F, 1 )
grayBackground32f = cv.CreateImage( (WIDTH, HEIGHT), cv.IPL_DEPTH_32F, 1 )
difference32f =     cv.CreateImage( (WIDTH, HEIGHT), cv.IPL_DEPTH_32F, 1 )

accumulatorShow8u = cv.CreateImage( (WIDTH, HEIGHT), cv.IPL_DEPTH_8U, 1 )
differenceShow8u =  cv.CreateImage( (WIDTH, HEIGHT), cv.IPL_DEPTH_8U, 1 )
threshold8u = 	 	cv.CreateImage( (WIDTH, HEIGHT), cv.IPL_DEPTH_8U, 1 )



def clientSetup():
	cv.NamedWindow("Camera", cv.CV_WINDOW_AUTOSIZE)
	cv.NamedWindow("Accumulator", cv.CV_WINDOW_AUTOSIZE)
	cv.NamedWindow("Difference", cv.CV_WINDOW_AUTOSIZE)
	cv.NamedWindow("Threshold", cv.CV_WINDOW_AUTOSIZE)

	cv.MoveWindow("Camera", 		0, 			0)
	cv.MoveWindow("Accumulator", 	WIDTH + 10, 0)
	cv.MoveWindow("Difference", 	0, 			HEIGHT + 50)
	cv.MoveWindow("Threshold", 		WIDTH + 10, HEIGHT + 50)

	cv.SetMouseCallback("Camera", mouseCallback, None)

def sensorSetup():
	cv.NamedWindow("Camera", cv.CV_WINDOW_AUTOSIZE)
	if args.visual:
		cv.NamedWindow("Accumulator", cv.CV_WINDOW_AUTOSIZE)
		cv.NamedWindow("Difference", cv.CV_WINDOW_AUTOSIZE)
		cv.NamedWindow("Threshold", cv.CV_WINDOW_AUTOSIZE)


	cv.MoveWindow("Camera", 		0, 			0)
	if args.visual:
		cv.MoveWindow("Accumulator", 	WIDTH + 10, 0)
		cv.MoveWindow("Difference", 	0, 			HEIGHT + 50)
		cv.MoveWindow("Threshold", 		WIDTH + 10, HEIGHT + 50)

	cv.SetMouseCallback("Camera", mouseCallback, None)

def clientRepeat():
	pass

def sensorRepeat():
	global accumulator
	global sbLink


	frame = cv.QueryFrame(capture)
	#print frame.depth
	frame32f = None

	# handle depth conversion if necessary
	# just keep it all 32 bits
	if frame.depth == 32 :
		frame32f = frame
	else:
		
		frame32f = cv.CreateImage( (WIDTH, HEIGHT), cv.IPL_DEPTH_32F, 3 )
		"""
		print frame.width, " ", frame.height
		print frame32f.width, " ", frame32f.height
		print frame.depth
		print frame32f.depth
		"""
		# py ocv handles the bit conversion for us
		cv.ConvertScale(frame, frame32f)

	# convert to grayscale
	cv.CvtColor(frame32f, grayBackground32f, cv.CV_RGB2GRAY)
	# make the running average bg
	cv.RunningAvg(grayBackground32f, accumulator32f, sbLink.learnRate)
	# do a absolute diff
	cv.AbsDiff(accumulator32f, grayBackground32f, difference32f)
	# finally threshold
	cv.Threshold(difference32f, threshold8u, sbLink.thresholdCutoff, MAX_PIXEL_VAL, cv.CV_THRESH_BINARY)

	cv.ConvertScale(accumulator32f, accumulatorShow8u)
	cv.ConvertScale(difference32f, differenceShow8u)

	# draw square
	if tempRectangle != None:
		pt1 = (tempRectangle[0], tempRectangle[1])
		pt2 = (tempRectangle[2], tempRectangle[3])
		cv.Rectangle(frame, pt1, pt2, (0,0,0), 1)
	elif rectangle != None:
		pt1 = (rectangle[0], rectangle[1])
		pt2 = (rectangle[2], rectangle[3])
		cv.Rectangle(frame, pt1, pt2, (0,0,0), 1)
	
	# If we have a rectangle let's do the test
	if rectangle != None:
		r = rectangle
		
		mask = np.zeros((threshold8u.width, threshold8u.height), np.uint8)
		print (r[1],r[3], r[0],r[2])
		print threshold8u.width, threshold8u.height
		print mask.shape
		#print mask.rows, mask.cols

		# switch x and y for cols
		mask[r[1]:r[3], r[0]:r[2]] = threshold8u[r[1]:r[3], r[0]:r[2]]

		pix = abs(r[0]-r[2]) * abs(r[1] - r[3])		
		hits = np.count_nonzero(mask)
		
		print "Percentage ", (float(hits) / float(pix))
		
		
	cv.ShowImage("Camera", frame)
	cv.ShowImage("Accumulator", accumulatorShow8u)
	cv.ShowImage("Difference", differenceShow8u)
	cv.ShowImage("Threshold", threshold8u)
	


clean = False

if args.client:
	clientSetup()
else:
	sensorSetup()

try:
	while True:
		c = cv.WaitKey(100)
		# 120 == 'x'
		if c == 120:
			break
		#time.sleep no work
		#time.sleep(int(sys.argv[1]))
		if args.client:
			clientRepeat()
		else:
			sensorRepeat()
	
	cv.DestroyAllWindows()
	del(capture)
	sbLink.stop()

	clean = True

except (KeyboardInterrupt, SystemExit) as e:
	print "Got keyboard interrupt"
	if not clean:
		cv.DestroyAllWindows()
		del(capture)
		sbLink.stop()
except Exception as e:
	if not clean:
		cv.DestroyAllWindows()
		del(capture)
		sbLink.stop()
	raise

