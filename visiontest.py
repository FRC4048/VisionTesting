from WebcamVideoStream import WebcamVideoStream
from FPS import FPS
import cv2	
import os
from VisionMath import Math
import numpy
import time
import math
import socket
from grip import GripPipeline
from contour import Contour
from networktables import NetworkTables
from networktables.util import ntproperty
from Constants import Constant as c
import logging 

#Aspect ratio (microsoft)
M_HA = 16
M_VA = 9
M_DFOV = 68.5

HRES = 640
VRES = (M_VA * HRES)/M_HA #360
#Target dimentions
TWIDTH_CM = 25

#return codes
ERROR = -1
SUCCESS = 0

#file number
i = 1

printTime = False
printStat = False
optionNetwork = False
optionImage = True

def init_network_tables():
	logging.basicConfig(level=logging.DEBUG)
	#NetworkTables.enableVerboseLogging()
	NetworkTables.initialize(server='10.11.13.109')
		
	while (not NetworkTables.isConnected()):
		time.sleep(1)
		print("waiting")


def init_UDP_client():
	UDP_IP = "10.11.13.109"	
	#UDP_IP  = "10.12.1.59"
	UDP_PORT = 5005
	MESSAGE = "Hello world"
	MESSAGE = MESSAGE*4
	print("UDP target IP:" + str(UDP_IP))
	print ("UDP target port:" + str(UDP_PORT))
	print ("message:", MESSAGE)
	
	sock = socket.socket(socket.AF_INET, #internet
					      socket.SOCK_DGRAM) #UDP
	sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))


def config_microsoft_cam():
	os.system("v4l2-ctl --set-ctrl=exposure_auto=1")
	os.system("v4l2-ctl --set-ctrl=exposure_absolute=5")
	os.system("v4l2-ctl --set-ctrl=brightness=30")
	os.system("v4l2-ctl --set-ctrl=saturation=200")
	os.system("v4l2-ctl --set-ctrl=contrast=1")
	os.system("v4l2-ctl --set-ctrl=white_balance_temperature_auto=0")
	os.system("v4l2-ctl --set-ctrl=white_balance_temperature=9000")

#ha --> horizontal aspect, va --> vertical aspect, dfov --> diagonal FOV
#These formulas are found on: vrguy.blogspot.com/2013/04/converting-diagonal-field-of-view-and.html
def find_fov(ha, va, dfov):
	da = math.sqrt(ha*ha + va*va)	
	hf = math.degrees(math.atan(math.tan(math.radians(dfov/2))*(ha/da))*2)
	return hf

def find_target(cnt1, cnt2):
        rc = ERROR
        if len(pipeline.find_contours_output) >= 2:
            #		    cnt1 = max(pipeline.find_contours_output, key = cv2.contourArea)
            #		    pipeline.find_contours_output.remove(cnt1)
            #		    cnt2 = max(pipeline.find_contours_output, key = cv2.contourArea)
            	largest_contours = sorted(pipeline.find_contours_output, key=cv2.contourArea)[-2:]
		cnt1.cnt = largest_contours[0]
		cnt2.cnt = largest_contours[1]
		cnt1.x, cnt1.y, cnt1.w, cnt1.h = cv2.boundingRect(cnt1.cnt)
		cnt2.x, cnt2.y, cnt2.w, cnt2.h = cv2.boundingRect(cnt2.cnt)

            	if (float(cnt1.h) / float(cnt2.h) >= 0.8 and float(cnt1.h) / float(cnt2.h) <= 1.2) and (float(cnt1.w) / float(cnt2.w) >= 0.8 and float(cnt1.w) / float(cnt2.w) <= 1.2):
            		rc = SUCCESS
	if rc == ERROR:
		cnt1.reset()
		cnt2.reset()
	return rc



if __name__ == "__main__":
	vision_math = Math()
	runtime = 10
	M_HFOV = find_fov(M_HA, M_VA, M_DFOV)
	config_microsoft_cam()
	if optionNetwork:
		init_network_tables()
		table = NetworkTables.getTable('SmartDashboard')	
	#init_UDP_client()	
	# code borrowed from Adrian
	# https://www.pyimagesearch.com/2015/12/21/increasing-webcam-fps-with-python-and-opencv/
	cam = WebcamVideoStream(src=0).start()
  	pipeline=GripPipeline()

	cnt1 = Contour()
 	cnt2 = Contour()	
	font = cv2.FONT_HERSHEY_SIMPLEX


	fps = FPS().start()
	
	t_end = time.time() + runtime
	while time.time() < t_end:
		frame = cam.read()
		if frame is not None:
			pipeline.process(frame)
			find_target(cnt1, cnt2)
			distance, distanceRC = vision_math.find_distance(cnt1, cnt2, M_HFOV)
			angle, angleRC = vision_math.find_angle(cnt1, cnt2, M_HFOV)
			if optionImage:			
				#frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5) 
				cv2.rectangle(frame, (cnt1.x, cnt1.y), (cnt1.x + cnt1.w, cnt1.y + cnt1.h), (255, 0, 0), 2)
				cv2.rectangle(frame, (cnt2.x, cnt2.y), (cnt2.x + cnt2.w, cnt2.y + cnt2.h), (255, 0, 0), 2)
				middle = (abs(cnt1.x+cnt2.x)/2, abs(cnt1.y+cnt2.y)/2)
				if distanceRC == SUCCESS:
					cv2.putText(frame, 'D='+str(int(round(distance))), middle, font, 0.5 , (0, 0, 255), 1, cv2.LINE_4)
				if angleRC == SUCCESS:
					cv2.putText(frame, 'A='+str(int(round(angle))), (middle[0],middle[1]+30), font, 0.5 , (0, 0, 255), 1, cv2.LINE_4)

				cv2.imshow("Frame", frame)
			fps.update()
	     
   			event = cv2.waitKey(1) & 0xFF
			if event == ord('p'):
				print(len(pipeline.find_contours_output))
				print
			elif event == ord('d'):
				if distanceRC == SUCCESS:		
					print("distance = " + str(distance))
					#distanceNT = distance
					if optionNetwork:
						table.putNumber('distance', distance)			
			elif event == ord('s'):
				printStat = True
			elif event == ord('a'):
				if angleRC == SUCCESS:			
					print("angle = " + str(angle))
			elif event == ord('q'):
				break 
	fps.stop()      
	cv2.destroyAllWindows()
	cam.stop()
   	
	
	print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
	print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
