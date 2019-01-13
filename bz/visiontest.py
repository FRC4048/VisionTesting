import cv2	
import os
import numpy
import time
import math
import socket
import logging 
import argparse

from VisionMath import Math
from WebcamVideoStream import WebcamVideoStream
from FPS import FPS
from grip import GripPipeline
from contour import Contour
try:
	from networktables import NetworkTables
	from networktables.util import ntproperty
except:
	print 'Could not import NetworkTables'
from Constants import Constant as c
from Camera import Camera


# Target dimentions
TWIDTH_CM = 25

#file number
i = 1

printStat = False

def init_network_tables():
	logging.basicConfig(level=logging.DEBUG)
	#NetworkTables.enableVerboseLogging()
	NetworkTables.initialize(server='10.11.13.109')
	nt_timeout = time.time() + c.NT_TIMEOUT	
	while (not NetworkTables.isConnected() and time.time() < nt_timeout):
		time.sleep(1)
		print("waiting")
	if (not NetworkTables.isConnected()):
		print "Could not connect to network tables"	

def init_UDP_client():
	UDP_IP = "10.11.13.109"	
	UDP_PORT = 5005
	MESSAGE = "Hello world"
	MESSAGE = MESSAGE*4
	print("UDP target IP:" + str(UDP_IP))
	print ("UDP target port:" + str(UDP_PORT))
	print ("message:", MESSAGE)
	
	sock = socket.socket(socket.AF_INET, #internet
					      socket.SOCK_DGRAM) #UDP
	sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))


def find_target(cnt1, cnt2):
	rc = c.SUCCESS
	if len(pipeline.find_contours_output) < 2:
		rc = c.ERROR
	else:
		largest_contours = sorted(pipeline.find_contours_output, key=cv2.contourArea)[-2:]
		cnt1.cnt = largest_contours[0]
		cnt2.cnt = largest_contours[1]

		# make sure cnt1 is the left and cnt2 is the right
		if (cv2.minAreaRect(cnt1.cnt)[0][0] > cv2.minAreaRect(cnt2.cnt)[0][0]):
			cnt1.cnt = largest_contours[1]
			cnt2.cnt = largest_contours[0]

		minRect = cv2.minAreaRect(cnt1.cnt)
		x, y, w, h = cv2.boundingRect(cnt1.cnt)
		cnt1.setvars(minRect, w, h)
		
		minRect = cv2.minAreaRect(cnt2.cnt)
		x, y, w, h = cv2.boundingRect(cnt2.cnt)
		cnt2.setvars(minRect, w, h)
		
		print  cnt1.h, cnt2.h, cnt1.w, cnt2.w 
		# check bounding box angles 
		if (abs(cnt1.angle) < abs(cnt2.angle) ) or  (abs(cnt1.angle)  + abs(cnt2.angle)  > 110) or (abs(cnt1.angle)  + abs(cnt2.angle)  <70):
			rc = c.ERROR
		else:
			# compare h of both blobs
        		if (float(cnt1.h) / float(cnt2.h) > 1.2 or float(cnt1.h) / float(cnt2.h) < 0.8) or (float(cnt1.w) / float(cnt2.w) > 1.2 or float(cnt1.w) / float(cnt2.w) < 0.8):
				rc = c.ERROR

	if rc == c.ERROR:
		cnt1.reset()
		cnt2.reset()
	return rc


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("runtime", type=int, nargs='?', help="runtime in seconds", default=10)
	parser.add_argument("-d", "--debug", help="turn debug on", action="store_true")
	parser.add_argument("-n", "--network", help="use network tables", action="store_true")
	parser.add_argument("-i", "--image", help="display image", action="store_true")
	args = parser.parse_args()
	
	vision_math = Math()
	camera = Camera("Microsoft", c.M_HA, c.M_VA, c.M_DFOV)    # Microsoft camera
	#camera = Camera("mac", c.MAC_HA, c.MAC_VA, c.MAC_DFOV)    # mac internal camera
	camera.config()
	
	HRES = 320
	VRES = (camera.va * HRES)/camera.ha #360

	if args.network:
		init_network_tables()
		table = NetworkTables.getTable('SmartDashboard')	
	#init_UDP_client()	
	# code borrowed from Adrian
	# https://www.pyimagesearch.com/2015/12/21/increasing-webcam-fps-with-python-and-opencv/
	stream = WebcamVideoStream(src=0).start()
  	pipeline=GripPipeline()

	cnt1 = Contour()
 	cnt2 = Contour()	
	font = cv2.FONT_HERSHEY_SIMPLEX

	fps = FPS().start()
	
	t_end = time.time() + args.runtime
	while time.time() < t_end:
		frame = stream.read()
		if frame is not None:
			pipeline.process(frame)
			find_target(cnt1, cnt2)
			distance, distanceRC = vision_math.find_distance(cnt1, cnt2, camera.hfov)
			angle, angleRC = vision_math.find_angle(cnt1, cnt2, camera.hfov)
			if args.image:			
				cv2.circle(frame, (cnt1.x , cnt1.y), 5, (255, 0, 0), 2)
				cv2.circle(frame, (cnt2.x , cnt2.y), 5, (255, 0, 0), 2)
				middle = (abs(cnt1.x+cnt2.x)/2, abs(cnt1.y+cnt2.y)/2)
				if distanceRC == c.SUCCESS:
					cv2.putText(frame, 'D='+str(int(round(distance))), middle, font, 0.5 , (0, 0, 255), 1, cv2.LINE_4)
				if angleRC == c.SUCCESS:
					cv2.putText(frame, 'A='+str(int(round(angle))), (middle[0],middle[1]+30), font, 0.5 , (0, 0, 255), 1, cv2.LINE_4)

				cv2.imshow("Frame", frame)
			fps.update()
	     
   			event = cv2.waitKey(1) & 0xFF
			if event == ord('p'):
				print(len(pipeline.find_contours_output))
				print
			elif event == ord('d'):
				if distanceRC == c.SUCCESS:		
					print("distance = " + str(distance))
					#distanceNT = distance
					if args.network:
						table.putNumber('distance', distance)			
			elif event == ord('s'):
				printStat = True
			elif event == ord('a'):
				if angleRC == c.SUCCESS:			
					print("angle = " + str(angle))
			elif event == ord('q'):
				break 
	fps.stop()      
	cv2.destroyAllWindows()
	stream.stop()
	
	print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
	print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
