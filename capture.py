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

def config_microsoft_cam():
	os.system("v4l2-ctl --set-ctrl=exposure_auto=1")
	os.system("v4l2-ctl --set-ctrl=exposure_absolute=5")
	os.system("v4l2-ctl --set-ctrl=brightness=30")
	os.system("v4l2-ctl --set-ctrl=saturation=200")
	os.system("v4l2-ctl --set-ctrl=contrast=1")
	os.system("v4l2-ctl --set-ctrl=white_balance_temperature_auto=0")
	os.system("v4l2-ctl --set-ctrl=white_balance_temperature=9000")

def init_network_tables():
	logging.basicConfig(level=logging.DEBUG)
	NetworkTables.enableVerboseLogging()
	NetworkTables.initialize(server='10.12.1.59')
		
	while (not NetworkTables.isConnected()):
		time.sleep(1)
		print("waiting")


def init_UDP_client():
	UDP_IP = "172.20.10.2"	
	#UDP_IP  = "10.12.1.59"
	UDP_PORT = 5005
	MESSAGE = "Hello world"
	MESSAGE = MESSAGE*4
	print("UDP target IP:" + UDP_IP)
	print ("UDP target port:" + UDP_PORT)
	print ("message:" + MESSAGE)
	
	sock = socket.socket(socket.AF_INET, #internet
					      socket.SOCK_DGRAM) #UDP
	sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

#ha --> horizontal aspect, va --> vertical aspect, dfov --> diagonal FOV
#These formulas are found on: vrguy.blogspot.com/2013/04/converting-diagonal-field-of-view-and.html
def find_fov(ha, va, dfov):
	da = math.sqrt(ha*ha + va*va)	
	hf = math.degrees(math.atan(math.tan(math.radians(dfov/2))*(ha/da))*2)
	return hf

#Horizontal FOV
#def find_distance(hf, cnt1, cnt2):
#	global printStat
#	#clean this up we dont want this to happen twice (once in find_target)
#	
#	Tpx=abs(contour.x2-contour.x1)+(contour.w1/2)+(contour.w2/2)
#	#print("Tpx =" + str(Tpx))
#	fovcm = (TWIDTH_CM * HRES)/Tpx
#	#print("fovcm = "+ str(fovcm))
#	distance = fovcm/(2*math.tan(math.radians(hf/2)))		
#	
#	if printStat: 
#		print("Object 1 Height = " + str(contour.h1) + "Width = " + str(contour.w1) + "X, Y = " + str(contour.x1) + ","  + str(contour.y1)) 
#		print("Object 2 Height = " + str(contour.h2) + "Width = " + str(contour.w2) + "X, Y = " + str(contour.x2) + ","  + str(contour.y2)) 
#		printStat = False
#
#	return distance

#def find_angle(hf, cnt1, cnt2):
#	global HRES
#	
#	Dpx = (HRES)/(2*math.tan(math.radians(hf/2)))
#	targetMidpoint = (contour.x1+contour.x2)/2		
#	offsetLength =  targetMidpoint - (HRES/2) 	
#	
#	offsetAngle = math.degrees(math.atan(offsetLength/Dpx))
#	
#	return offsetAngle


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




#Configuring the camera to look the way we want	
config_microsoft_cam()
#init_UDP_client()
#init_network_tables()
M_HFOV = find_fov(M_HA, M_VA, M_DFOV)
#print(M_HFOV)


pipeline = GripPipeline()
vision_math = Math()

#Video Capture stuff
cam = cv2.VideoCapture(0)
#Set Camera resoultion
cam.set(3, HRES)
cam.set(4, VRES)
cnt1 = Contour()
cnt2 = Contour()
count = 0
t_end = time.time() + 10
while time.time() <= t_end:
	count = count+1
	captureStartTime = cv2.getTickCount()
	s, im = cam.read() # captures image
	captureEndTime = cv2.getTickCount()
	captureTime = (captureEndTime - captureStartTime)/cv2.getTickFrequency()
	cv2.imshow("Test Picture", im) # displays captured image	
	processStartTime = cv2.getTickCount()
	pipeline.process(im) 
	processEndTime = cv2.getTickCount()
	processTime = (processEndTime - processStartTime)/cv2.getTickFrequency()
	find_target(cnt1, cnt2)
	distance, distanceRC = vision_math.find_distance(cnt1, cnt2, M_HFOV)
	angle, angleRC = vision_math.find_angle(cnt1, cnt2, M_HFOV)
	if printTime:
		print("Frame processing time:" +  str(processTime) + "\nFrame Capture Time:" + str(captureTime))
                                     	
	event = cv2.waitKey(25) & 0xFF
	if event == ord('c'):
		cv2.imwrite("./microsoft"+str(i)+".jpg", im)
		print("microsoft"+str(i))		
		i=i+1
	elif event == ord('p'):
		print(len(pipeline.find_contours_output))
		print
	elif event == ord('d'):
		if distanceRC == SUCCESS:		
			print("distance = " + str(distance))
	elif event == ord('s'):
		printStat = True
	elif event == ord('a'):
		if angleRC == SUCCESS:			
			print("angle = " + str(angle))
	elif event == ord('q'):
		break 
print(count/10)


cam.release()
cv2.destroyAllWindows()
