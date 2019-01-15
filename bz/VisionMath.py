from contour import Contour
from Constants import Constant as c
import math

printStat = False

class Math():

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
		





