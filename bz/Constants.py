class Constant():
	#Aspect ratio (microsoft)
	M_HA = 16
	M_VA = 9
	M_DFOV = 68.5
	
	# Aspect ratio (mac internal camera)
	MAC_HA = 10
	MAC_VA = 10
	MAC_DFOV = 80  ### this is just a guess....
	

	HRES = 320
	VRES = (M_VA * HRES)/M_HA #360

	# Network tables constants
	NT_TIMEOUT = 10

	#return codes
	ERROR = -1
	SUCCESS = 0

	#file number
	i = 1	
			
