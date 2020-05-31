import cv2
import numpy as np

class PerspectiveTransform():
	def __init__(self):
		self.image = None
		self.points = None
		
	def order_points(self):
		rect = np.zeros((4,2), dtype="float32")
		# top-left top-right bottom-right bottom-left
		for i in range(len(self.points)):
			rect[i] = self.points[i]
		return rect
	
	def perspective_transformation(self,image,points):
		self.image=image
		self.points=points
		# get ordered points and unpack them
		rect = self.order_points()
		(tl, tr, bl, br) = rect	 ## top-left top-right bottom-right bottom-left

		#print(rect)# compute width of new image
		
		# distance between topmost two points
		widthT = np.sqrt((tr[0]-tl[0])**2 + (tr[1]-tl[1])**2)
		# distance between bottommost two points
		widthB = np.sqrt((br[0]-bl[0])**2 + (br[1]-bl[1])**2)

		# compute height
		#distance between leftmost points
		heightL = np.sqrt((tl[0]-bl[0])**2 + (tl[1]-bl[1])**2)
		# distance between rightmost points
		heightR = np.sqrt((tr[0]-br[0])**2 + (tr[1]-br[1])**2)

		# find max height and width
		maxWidth = max(int(widthB), int(widthT))
		maxHeight = max(int(heightL), int(heightR))

		#print('width:'+str(maxWidth))
		#print('height:'+str(maxHeight))

		dst = np.float32([[0,0],
			[maxWidth-1,0],
			[maxWidth-1, maxHeight-1],
			[0,maxHeight-1]])

		# compute perspective transform matrix
		M = cv2.getPerspectiveTransform(rect, dst)
		warped = cv2.warpPerspective(self.image, M, (maxWidth, maxHeight))

		return warped
		
		
def main():

	img = cv2.imread('draw.jpg',1)
	pts = [(70,2),(554,3),(618,471),(13,474)]
	
	PT_obj = PerspectiveTransform()
	transformed_img = PT_obj.perspective_transformation(img,pts)
	
	cv2.imshow('unchanged image', transformed_img)
	k = cv2.waitKey(0)      # keyboard binding function
	if k == 27:  # wait for ESC key to exit
		cv2.destroyAllWindows()  # simply destroys all the windows we created
		
if __name__ == '__main__':
	main()
