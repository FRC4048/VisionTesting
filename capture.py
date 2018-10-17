import cv2	
import os
import math
import numpy
from grip import GripPipeline

#Aspect ratio (microsoft)
M_HA = 16
M_VA = 9
M_DFOV = 68.5

HRES = 640
VRES = 360

#Target dimentions
TWIDTH_CM = 25

#return codes
ERROR = -1
SUCCESS = 0

#file number
i = 1

def config_microsoft_cam():
	#os.system("v4l2-ctl -v --set-fmt-video=width=1920,height=1080")
	#os.system("v4l2-ctl --set-fmt-video=width=1920,height=1080,pixelformat=YUYV")

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

#Horizontal FOV
def find_distance(hf, cnt1, cnt2):
	#clean this up we dont want this to happen twice (once in find_target)
	x1,y1,w1,h1 = cv2.boundingRect(cnt1)
	x2,y2,w2,h2 = cv2.boundingRect(cnt2)

	Tpx=abs(x2-x1)+(w1/2)+(w2/2)
	#print("Tpx =" + str(Tpx))
	fovcm = (TWIDTH_CM * HRES)/Tpx
	#print("fovcm = "+ str(fovcm))
	distance = fovcm/(2*math.tan(math.radians(hf/2)))		
	print("distance = " + str(distance))
	
	return distance

#may change this
def find_target():
	rc = ERROR
	cnt1 = 0
	cnt2 = 0
	if len(pipeline.find_contours_output) >= 2:
#		cnt1 = max(pipeline.find_contours_output, key = cv2.contourArea)
#		pipeline.find_contours_output.remove(cnt1)
#		cnt2 = max(pipeline.find_contours_output, key = cv2.contourArea)
		largest_contours = sorted(pipeline.find_contours_output, key=cv2.contourArea) [-2:]		
		cnt1 = largest_contours[0]
		cnt2 = largest_contours[1]

		x1,y1,w1,h1 = cv2.boundingRect(cnt1)
		x2,y2,w2,h2 = cv2.boundingRect(cnt2)
		#print("width = " + str(float(w1)/float(w2)) + " Height = " + str(float(h1)/float(h2)))
		if (float(h1)/float(h2) >= 0.8 and float(h1)/float(h2) <= 1.2) and (float(w1)/float(w2) >= 0.8 and float(w1)/float(w2) <= 1.2):
			rc = SUCCESS
	return cnt1, cnt2, rc

#Configuring the camera to look the way we want	
config_microsoft_cam()
M_HFOV = find_fov(M_HA, M_VA, M_DFOV)
print(M_HFOV)


pipeline = GripPipeline()

#Video Capture stuff
cam = cv2.VideoCapture(0)
#Set Camera resoultion
cam.set(3, HRES)
cam.set(4, VRES)
while(True):
	s, im = cam.read() # captures image
	cv2.imshow("Test Picture", im) # displays captured image	
	pipeline.process(im) 
	cnt1, cnt2, rc = find_target()
	event = cv2.waitKey(25) & 0xFF
	if event == ord('c'):
		cv2.imwrite("./microsoft"+str(i)+".jpg", im)
		print("microsoft"+str(i))		
		i=i+1
	elif event == ord('p'):
		print(len(pipeline.find_contours_output))
		print
	elif event == ord('d') and rc == SUCCESS:
		find_distance(M_HFOV, cnt1, cnt2)
	elif event == ord('q'):
		break 

cam.release()
cv2.destroyAllWindows()
