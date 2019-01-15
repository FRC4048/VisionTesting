from contour import Contour
from Constants import Constant as c
import math

#Target dimentions
TWIDTH_CM = 25

#return codes
ERROR = -1
SUCCESS = 0

printStat = False

class Math():

	@staticmethod
	def find_distance(cnt1, cnt2, hf):
		if cnt1.x == 0 or cnt2.x == 0:
			return 0, ERROR  
		global printStat

		Tpx=abs(cnt2.x-cnt1.x)+(cnt1.w/2)+(cnt2.w/2)
		#print("Tpx =" + str(Tpx))
		fovcm = (TWIDTH_CM * c.HRES)/Tpx
		#print("fovcm = "+ str(fovcm))
		distance = fovcm/(2*math.tan(math.radians(hf/2)))
	
		if printStat:
			print("Object 1 Height = " + str(cnt1.h) + "Width = " + str(cnt1.w) + "X, Y = " + str(cnt1.x) + ","  + str(cnt2.y))
			print("Object 2 Height = " + str(cnt2.h) + "Width = " + str(cnt2.w) + "X, Y = " + str(cnt2.x) + ","  + str(cnt2.y))
			printStat = False
		return distance, SUCCESS


	@staticmethod
	def find_angle(cnt1, cnt2, hf):
		if cnt1.x == 0 or cnt2.x == 0:
			return 0, ERROR  
		Dpx = (c.HRES)/(2*math.tan(math.radians(hf/2)))
		targetMidpoint = (cnt1.x+cnt2.x)/2
		offsetLength =  targetMidpoint - (c.HRES/2)

		offsetAngle = math.degrees(math.atan(offsetLength/Dpx))
	
		return offsetAngle, SUCCESS


	@staticmethod
	def find_tx_ty(cnt1, cnt2, hf, vf):
		middlex = (cnt1.x + cnt2.x)/2
		middley = (cnt1.y + cnt2.y)/2
		offsetx = middlex - c.HRES/2
		offsety = middley - c.VRES/2
		return (hf/c.HRES) * offsetx, (vf/c.VRES) * offsety * -1
	
	@staticmethod
	def find_tx_ty_math(middlex, middley, hf, vf):
		offsetx = middlex - c.HRES/2
		offsety = middley - c.VRES/2
		print "X: ", (hf/c.HRES) * offsetx, "  Y: ", (vf/c.VRES) * offsety * -1
		





