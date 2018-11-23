import math
from Constants import Constant as c

class Camera():
	def __init__(self, model, ha, va, dfov):
		self.model = model
		self.ha = ha       # horizontal aspect
		self.va = va       # vertical aspect
		self.dfov = dfov   # diagonal field of view

		#These formulas are found on: vrguy.blogspot.com/2013/04/converting-diagonal-field-of-view-and.html
		da = math.sqrt(self.ha*self.ha + self.va*self.va)	
		self.hfov = math.degrees(math.atan(math.tan(math.radians(self.dfov/2))*(self.ha/da))*2)		

	def config(self):
		if self.model == "Microsoft":
			os.system("v4l2-ctl --set-ctrl=exposure_auto=1")
			os.system("v4l2-ctl --set-ctrl=exposure_absolute=5")
			os.system("v4l2-ctl --set-ctrl=brightness=30")
			os.system("v4l2-ctl --set-ctrl=saturation=200")
			os.system("v4l2-ctl --set-ctrl=contrast=1")
			os.system("v4l2-ctl --set-ctrl=white_balance_temperature_auto=0")
			os.system("v4l2-ctl --set-ctrl=white_balance_temperature=9000")	
		else:
			print "Unknown camera (" + self.model + ")"
		
		
		
		
		
		
		