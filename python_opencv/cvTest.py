#!/usr/bin/env python

import cv2
import time

cv2.namedWindow("Win")

img = cv2.imread("logo.png")

cv2.imshow("Win", img)

def repeat():
	time.sleep(1)

while True:
	repeat()

"""
vc = cv2.VideoCapture(-1)
rval, frame = vc.read()

def repeat():
	global vc
	global frame

	cv2.imshow("win", frame)
	rval, frame = vc.read()

while True:
	repeat()	
"""