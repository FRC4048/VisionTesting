from threading import Thread
from Constants import Constant as c
import cv2
 
class WebcamVideoStream:
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
	self.stream.set(3, c.HRES)
	self.stream.set(4, c.VRES)        
	self.stopped = False
      
      		
    def start(self):
        # start the thread to read frames from the video stream
        self.t = Thread(target=self.update, args=())
	self.t.start()
	
        return self


# This is the thread that will be running to get images
    def update(self):
        while True:
            if self.stopped:
                return
            (self.grabbed, self.frame) = self.stream.read()
 
    def read(self):
        # return the frame most recently read
        if self.grabbed:
           return self.frame
        else:
           return None
 
    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
	self.t.join()


	
