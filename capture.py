import cv2	
import os
from grip import GripPipeline


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


def find_distance():
	x1,y1,w1,h1 = cv2.boundingRect(pipeline.find_contours_output[0])
	x2,y2,w2,h2 = cv2.boundingRect(pipeline.find_contours_output[1])
	
	Tpx=abs(x2-x1)+(w1/2)+(w2/2)
	
	distance=17204/Tpx
	print(distance)	




#Configuring the camera to look the way we want	
config_microsoft_cam()
pipeline = GripPipeline()

#Video Capture stuff
cam = cv2.VideoCapture(0)
#Set Camera resoultion
cam.set(3, 640)
cam.set(4, 480)
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
		find_distance()
	elif event == ord('q'):
		break 

cam.release()
cv2.destroyAllWindows()
