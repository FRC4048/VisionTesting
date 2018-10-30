from contour import Contour
import math
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

printStat = False

class Math():

	@staticmethod
	def find_distance(cnt1, cnt2, hf):
		if cnt1.x == 0 or cnt2.x == 0:
			return 0, ERROR  
		global printStat

		Tpx=abs(cnt2.x-cnt1.x)+(cnt1.w/2)+(cnt2.w/2)
		#print("Tpx =" + str(Tpx))
		fovcm = (TWIDTH_CM * HRES)/Tpx
		#print("fovcm = "+ str(fovcm))
		distance = fovcm/(2*math.tan(math.radians(hf/2)))
	
		if printStat:
			print("Object 1 Height = " + str(cnt1.h) + "Width = " + str(cnt1.w) + "X, Y = " + str(cnt1.x) + ","  + str(cnt2.y))
			print("Object 2 Height = " + str(cnt2.h) + "Width = " + str(cnt2.w) + "X, Y = " + str(cnt2.x) + ","  + str(cnt2.y))
			printStat = False
		return distance, SUCCESS


	@staticmethod
	def find_angle(cnt1, cnt2, hf):
		global HRES
		if cnt1.x == 0 or cnt2.x == 0:
			return 0, ERROR  
		Dpx = (HRES)/(2*math.tan(math.radians(hf/2)))
		targetMidpoint = (cnt1.x+cnt2.x)/2
		offsetLength =  targetMidpoint - (HRES/2)

		offsetAngle = math.degrees(math.atan(offsetLength/Dpx))
	
		return offsetAngle, SUCCESS

