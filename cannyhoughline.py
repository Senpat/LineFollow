##detects line using canny then houghline 3/28/19

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

def dis(x1,y1,x2,y2):
	return math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2))

def vidprocess(frame):
	# resize the frame, convert it to grayscale, and blur it
	frame = imutils.resize(frame, width=500)


	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(gray,(21,21,),4)

	ret,thresh = cv2.threshold(blur,GTHRESH,255,0)
	thresh = cv2.bitwise_not(thresh)

	edges = cv2.Canny(thresh,100,200)

	#img, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	#cv2.drawContours(frame, contours, -1, (0,255,0), 3)

	lines = cv2.HoughLinesP(edges,1,np.pi/180,200,minLineLength = 100)



	if(not lines is None):
		'''find longest 2 lines'''
		'''
		maxline1 = -1
		maxline2 = -1
		maxdis1 = -1
		maxdis2 = -1

		for L in lines:
			for x1,y1,x2,y2 in L:
				curdis = dis(x1,y1,x2,y2)
				if(curdis > maxdis1):
					maxdis2 = maxdis1
					maxdis1 = curdis
					maxline2 = maxline1
					maxline1 = (x1,y1,x2,y2)
				elif(curdis > maxdis2):
					maxdis2 = curdis
					maxline2 = (x1,y1,x2,y2)

		if(maxline1 != -1):
			cv2.line(frame,(maxline1[0],maxline1[1]),(maxline1[2],maxline1[3]),(0,0,0),4)
		if(maxline2 != -1):
			cv2.line(frame,(maxline2[0],maxline2[1]),(maxline2[2],maxline2[3]),(0,0,0),4)
		'''

		for L in lines:
			for x1,y1,x2,y2 in L:
				cv2.line(frame,(x1,y1),(x2,y2),(0,0,0),4)



	cv2.imshow("frame",frame)
	#cv2.imshow("blur",blur)
	#cv2.imshow("thresh",thresh)
	cv2.imshow("edges",edges)

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
