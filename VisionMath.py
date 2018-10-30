from contour import Contour
import math
M_HA = 16
M_VA = 9
M_DFOV = 68.5

HRES = 640
VRES = (M_VA * HRES)/M_HA #360
#Target dimentions
TWIDTH_CM = 25

printStat = False

class Math():

	@staticmethod
	def find_distance(hf):
		contour1 = Contour()
		contour2 = Contour()
		global printStat

		Tpx=abs(contour2.x2-contour1.x1)+(contour1.w1/2)+(contour2.w2/2)
		#print("Tpx =" + str(Tpx))
		fovcm = (TWIDTH_CM * HRES)/Tpx
		#print("fovcm = "+ str(fovcm))
		distance = fovcm/(2*math.tan(math.radians(hf/2)))
	
		if printStat:
			print("Object 1 Height = " + str(contour1.h1) + "Width = " + str(contour1.w1) + "X, Y = " + str(contour1.x1) + ","  + str(contour1.y1))
			print("Object 2 Height = " + str(contour1.h2) + "Width = " + str(contour2.w2) + "X, Y = " + str(contour2.x2) + ","  + str(contour2.y2))
			printStat = False
		return distance


	@staticmethod
	def find_angle(hf):
		contour1 = Contour()
		contour2 = Contour()
		global HRES
		
		Dpx = (HRES)/(2*math.tan(math.radians(hf/2)))
		targetMidpoint = (contour1.x1+contour2.x2)/2
		offsetLength =  targetMidpoint - (HRES/2)

		offsetAngle = math.degrees(math.atan(offsetLength/Dpx))
	
		return offsetAngle

