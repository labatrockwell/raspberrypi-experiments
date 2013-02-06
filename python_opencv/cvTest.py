#!/usr/bin/env python

import cv

WIDTH = 240
HEIGHT = 135


state = None
rectangle = None
tempRectangle = None

def mouseCallback(event, x, y, flags, param):
	if event == cv.CV_EVENT_LBUTTONDOWN:
		state = "DOWN"
		tempRectangle = (x, y, x, y)
	elif event == cv.CV_EVENT_LBUTTONUP:
		if state != "DOWN" :
			pass

		state = None

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


cv.NamedWindow("Camera", cv.CV_WINDOW_AUTOSIZE)
cv.NamedWindow("Accumulator", cv.CV_WINDOW_AUTOSIZE)
cv.NamedWindow("Difference", cv.CV_WINDOW_AUTOSIZE)
cv.NamedWindow("Threshold", cv.CV_WINDOW_AUTOSIZE)


cv.MoveWindow("Camera", 		0, 			0)
cv.MoveWindow("Accumulator", 	WIDTH + 10, 0)
cv.MoveWindow("Difference", 	0, 			HEIGHT + 50)
cv.MoveWindow("Threshold", 		WIDTH + 10, HEIGHT + 50)

cv.SetMouseCallback("Camera", mouseCallback, None)
cv.SetMouseCallback("Accumulator", mouseCallback, None)
cv.SetMouseCallback("Difference", mouseCallback, None)
cv.SetMouseCallback("Threshold", mouseCallback, None)

def repeat():
	global capture
	global WIDTH
	global HEIGHT
	global accumulator
	global grayBackground

	frame = cv.QueryFrame(capture)
	frame32f = None

	# handle depth conversion if necessary
	# just keep it all 32 bits
	if frame.depth == 32 :
		frame32f = frame
	else:
		frame32f = cv.CreateImage( (WIDTH, HEIGHT), cv.IPL_DEPTH_32F, 3 )
		# py ocv handles the bit conversion for us
		cv.ConvertScale(frame, frame32f)

	# convert to grayscale
	cv.CvtColor(frame32f, grayBackground32f, cv.CV_RGB2GRAY)
	# make the running average bg
	cv.RunningAvg(grayBackground32f, accumulator32f, 0.1)
	# do a absolute diff
	cv.AbsDiff(accumulator32f, grayBackground32f, difference32f)
	# finally threshold
	cv.Threshold(difference32f, threshold8u, 20, 255, cv.CV_THRESH_BINARY)

	cv.ConvertScale(accumulator32f, accumulatorShow8u)
	cv.ConvertScale(difference32f, differenceShow8u)

	cv.ShowImage("Camera", frame)
	cv.ShowImage("Accumulator", accumulatorShow8u)
	cv.ShowImage("Difference", differenceShow8u)
	cv.ShowImage("Threshold", threshold8u)


while True:
	c = cv.WaitKey(100)
	# 120 == 'x'
	if c == 120:
		break
	#time.sleep no work
	#time.sleep(int(sys.argv[1]))
	repeat()
	
cv.DestroyAllWindows()
del(capture)
