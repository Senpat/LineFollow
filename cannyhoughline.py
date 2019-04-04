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
STRAIGHTTHRESH = 5

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
	edges = cv2.dilate(edges,None,iterations=1)
	#img, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	#cv2.drawContours(frame, contours, -1, (0,255,0), 3)

	lines = cv2.HoughLinesP(edges,1,np.pi/180,200,minLineLength = 100)



	if(not lines is None):
		'''find highest and lowest lines'''
		maxy = -1
		maxline = -1
		miny = 10000
		minline = -1

		for L in lines:
			for x1,y1,x2,y2 in L:
				if(max(y1,y2) > maxy):
					maxy = max(y1,y2)
					maxline = (x1,y1,x2,y2)
				if(min(y1,y2) < miny):
					miny = min(y1,y2)
					minline = (x1,y1,x2,y2)

		if(maxline != -1):
			cv2.line(frame,(maxline[0],maxline[1]),(maxline[2],maxline[3]),(0,0,0),4)
		if(minline != -1):
			cv2.line(frame,(minline[0],minline[1]),(minline[2],minline[3]),(0,0,0),4)


		#calculates slope and uses that to determine left or right

		#slope based on maxline
		slope = 99999
		if(abs(maxline[0]-maxline[2]) < STRAIGHTTHRESH):
			print("GO STRAIGHT")
		else:
			slope = (maxline[1]-maxline[3])/(maxline[0]-maxline[2])
			if(slope < 0):
				print("GO RIGHT")
			else:
				print("GO LEFT")

		#calculate angle
		if(slope != 99999):

			angle = round(abs(math.degrees(math.atan(1/slope))),2)
			print(str(angle) + u"\u00b0")
		'''
		print(len(lines))
		for L in lines:
			for x1,y1,x2,y2 in L:
				cv2.line(frame,(x1,y1),(x2,y2),(0,0,0),4)
		'''


	cv2.imshow("edges",edges)
	cv2.imshow("frame",frame)
	#cv2.imshow("blur",blur)
	#cv2.imshow("thresh",thresh)
	

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
