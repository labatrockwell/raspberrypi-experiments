#!/usr/bin/env python

import cv
import time
import sys


cv.NamedWindow("Win", cv.CV_WINDOW_AUTOSIZE)

capture = cv.CaptureFromCAM(-1)

cv.SetCaptureProperty( capture, cv.CV_CAP_PROP_FRAME_WIDTH, 240 )
cv.SetCaptureProperty( capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 135 )


def repeat():
	global capture
	
	frame = cv.QueryFrame(capture)
	cv.ShowImage("Win", frame)


while True:
	c = cv.WaitKey(1)
	if( c != -1 ):
		break
	#time.sleep no work
	#time.sleep(int(sys.argv[1]))
	repeat()
	
cv.DestroyAllWindows()
del(capture)
