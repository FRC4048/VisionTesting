from Constants import Constant
from VisionMath import Math
from Camera import Camera

c = Constant()
vision_math = Math()
camera = Camera("Microsoft", c.M_HA, c.M_VA, c.M_DFOV)

print "HFOV: ", camera.hfov
print "VFOV: ", camera.vfov

print "Midpoint: "
vision_math.find_tx_ty_math(160, 90, camera.hfov, camera.vfov)
print ""
print "Top-left point: "
vision_math.find_tx_ty_math(0, 0, camera.hfov, camera.vfov)
print ""
print "Bottom-right point: "
vision_math.find_tx_ty_math(320, 180, camera.hfov, camera.vfov)
print ""
print "Bottom-left point: "
vision_math.find_tx_ty_math(0, 180, camera.hfov, camera.vfov)
print""
print "Top-right point: "
vision_math.find_tx_ty_math(320, 0, camera.hfov, camera.vfov)
print ""
print "Middle-left: "
vision_math.find_tx_ty_math(80, 90, camera.hfov, camera.vfov)
print ""
print "Middle-top: "
vision_math.find_tx_ty_math(160, 45, camera.hfov, camera.vfov)
