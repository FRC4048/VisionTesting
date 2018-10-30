import cv2
from grip import GripPipeline

class Contour():

	def __init__(self):

 		#cnt1, cnt2 = Contour.find_target()
		self.cnt = []

		self.x = 0
		self.y = 0 
		self.w =0 
		self.h = 0
	

	def reset(self):
		
		self.cnt = []

		self.x = 0
		self.y = 0 
		self.w =0 
		self.h = 0
	


    
    
