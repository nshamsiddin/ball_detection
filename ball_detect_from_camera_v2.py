import numpy as np
from cv2 import cv2
from matplotlib import pyplot as plt
from PIL import Image

import vision_definitions as vd
from naoqi import ALProxy

ip = '127.0.0.1'
port = 9559

filter_bounds = {
	'red' : [(0, 28, 82), (17, 255, 255)],
	'blue' : [(112, 65, 72), (157, 255, 255)],
}

camera_specs = {
	0: {'focal_legth' : 569, 'angle_x' : 60.97, 'angle_y' : 47.64, 'res' : vd.kVGA, 'fps' : 1, 'height' : 54},
	1: {'focal_legth' : 415, 'angle_x' : 60.97, 'angle_y' : 47.64, 'res' : vd.k16VGA, 'fps' : 1, 'height' : 48},
}


GAUSS_PARAMS = {
	'ksize'  :(9, 9),
	'sigmaX' : 3
}

HOUGH_PARAMS = {
	'dp': 1,
	'minDist': 10,
	'param1': 100,
	'param2': 30,
	'minRadius' : 0,
	'maxRadius' : 0
}



def takeImage(camera = 0):

	camProxy = ALProxy("ALVideoDevice", ip, port)
	res = camera_specs[camera]['res']  # VGA
	fps = camera_specs[camera]['fps']
	colorSpace = vd.kRGBColorSpace  # RGB
	camProxy.setParam(vd.kCameraSelectID, camera)
	videoClient = camProxy.subscribe("python", res, colorSpace, fps)
	naoImage = camProxy.getImageRemote(videoClient)
	camProxy.unsubscribe(videoClient)

	filename = 'balls.png'
	# Get the image size and pixel array.
	width = naoImage[0]
	height = naoImage[1]
	array = naoImage[6]

	im = Image.frombytes("RGB", (width, height), array)
	im.save(filename, "PNG")
	process(filename, camera)


def display_image(image):
	cv2.imshow('test', image)
	cv2.waitKey(0)

def find_position(x, y, r, camera):
	# focal length calculated with F = (PxD)/W where
	# W - actual width of an object (diameter of a ball)
	# D - distance to the object
	# P - width of the object in the image
	W = 20
	F = 0
	if camera == 0:
		F = 569 # calculated focal length for camera #0
	if camera == 1:
		F = 415 # calculated focal length for camera #1
	# from formula above we can find distance D = (WxF)/P
	D = (W * F) / (2 * r)
	print(W, F, r, D)

	# from NAO specs
	position = 0

	return position, D

def get_balls(image, color, bounds, camera):

	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	bright = cv2.inRange(hsv, bounds[0], bounds[1])
	blur = cv2.GaussianBlur(bright, **GAUSS_PARAMS)
	


	# detected_circles = cv2.HoughCircles(blurred_mask, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)
	detected_circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, **HOUGH_PARAMS)
	balls = []

	if detected_circles is not None:
		for circle in detected_circles[0, :]:
			x = circle[0]
			y = circle[1]
			r = circle[2]
			
			# locate detected balls
			position, distance = find_position(x, y, r, camera)
			circled_orig = cv2.circle(image, (x, y), r, (0, 255, 0), thickness=1)

			font = cv2.FONT_HERSHEY_SIMPLEX
			# x = x - 10
			print(x, y)
			cv2.putText(circled_orig, str(format(distance, '.2f')), (x,y), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

			balls.append((x, y, r, color))
		
		display_image(circled_orig)

	return balls


def process(filename, camera):
	print(filename)

	image = cv2.imread(filename)

	# red balls
	red = get_balls(image, 'red', filter_bounds['red'], camera)
	print(red)

	# blue balls
	blue = get_balls(image, 'blue', filter_bounds['blue'], camera)
	print(blue)

	# blye balls
	# blue = get_balls(image, 0, 0, 0, 0)


takeImage(0)