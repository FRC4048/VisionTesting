import cv2
from grip import GripPipeline

pipeline = GripPipeline()

class Contour():

    @staticmethod
    def find_target():
        #rc = 0
        cnt1 = 0
        cnt2 = 0
        if len(pipeline.find_contours_output) >= 2:
            #		    cnt1 = max(pipeline.find_contours_output, key = cv2.contourArea)
            #		    pipeline.find_contours_output.remove(cnt1)
            #		    cnt2 = max(pipeline.find_contours_output, key = cv2.contourArea)
            largest_contours = sorted(pipeline.find_contours_output, key=cv2.contourArea)[-2:]
            cnt1 = largest_contours[0]
            cnt2 = largest_contours[1]

            #if (float(Contour.h1) / float(Contour.h2) >= 0.8 and float(Contour.h1) / float(Contour.h2) <= 1.2) and (float(Contour.w1) / float(Contour.w2) >= 0.8 and float(Contour.w1) / float(Contour.w2) <= 1.2):
            #    rc = 1
        return cnt1, cnt2

        
    def __init__(self):

        cnt1, cnt2 = Contour.find_target()

        self.x1, self.y1, self.w1, self.h1 = cv2.boundingRect(cnt1)
        self.x2, self.y2, self.w2, self.h2 = cv2.boundingRect(cnt2)

    


    
    