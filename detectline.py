##detects line 3/5/19

import sys
import argparse
import warnings
import datetime
#import dropbox
import imutils
import json
import time
import cv2
import numpy as np
import math
import glob

from picamera import PiCamera
from picamera.array import PiRGBArray

GTHRESH = 127

def vidprocess(frame):
	# resize the frame, convert it to grayscale, and blur it
	frame = imutils.resize(frame, width=500)

	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(gray,(21,21,),4)

	ret,thresh = cv2.threshold(blur,GTHRESH,255,0)

	img, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	cv2.drawContours(frame, contours, -1, (0,255,0), 3)

	cv2.imshow("frame",frame)
	cv2.imshow("blur",blur)
	cv2.imshow("thresh",thresh)

	cv2.waitKey(1) & 0xFF
	rawCapture.truncate(0)

	return True



if __name__ == "__main__":

	camera = PiCamera()
	camera.framerate = 32
	rawCapture = PiRGBArray(camera)

	'''
	cap = cv2.VideoCapture(0)

	while(True):
		ret,frame = cap.read()
		vidprocess(frame)
	'''

	time.sleep(0.1)

	for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		# grab the raw NumPy array representing the image and initialize
		# the timestamp and occupied/unoccupied text
		frame = f.array
		vidprocess(frame)
		#rawCapture.truncate(0)

	cap.release()
	cv2.destroyAllWindows()
