import cv2	
import os
import math
from grip import GripPipeline

#Aspect ratio (microsoft)
M_HA = 16
M_VA = 9
M_DFOV = 68.5

HRES = 640
VRES = 360

#Target dimentions
TWIDTH_CM = 25

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
def find_distance(hf):
	
	x1,y1,w1,h1 = cv2.boundingRect(pipeline.find_contours_output[0])
	x2,y2,w2,h2 = cv2.boundingRect(pipeline.find_contours_output[1])
	
	Tpx=abs(x2-x1)+(w1/2)+(w2/2)
	#print("Tpx =" + str(Tpx))
	fovcm = (TWIDTH_CM * HRES)/Tpx
	#print("fovcm = "+ str(fovcm))
	distance = fovcm/(2*math.tan(math.radians(hf/2)))		
	print("distance = " + str(distance))
	
	return distance



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
	event = cv2.waitKey(25) & 0xFF
	if event == ord('c'):
		cv2.imwrite("./microsoft"+str(i)+".jpg", im)
		print("microsoft"+str(i))		
		i=i+1
	elif event == ord('p'):
		print(len(pipeline.find_contours_output))
		print
	elif event == ord('d') and len(pipeline.find_contours_output) == 2:
		find_distance(M_HFOV)
	elif event == ord('q'):
		break 

cam.release()
cv2.destroyAllWindows()
