import numpy as np
from cv2 import cv2
from matplotlib import pyplot as plt
from PIL import Image

import vision_definitions
from naoqi import ALProxy

ip = "127.0.0.1"
port = 9559

def takeImage():

	camProxy = ALProxy("ALVideoDevice", ip, port)
	resolution = vision_definitions.kVGA
	colorSpace = vision_definitions.kRGBColorSpace
	fps = 1

	# camProxy.set
	# print(camProxy.getParam(13))
	# camProxy.setParam(18, 0)
	camProxy.setParam(vision_definitions.kCameraSelectID, 0)
	camProxy.setParam(vision_definitions.kCameraContrastID, 0)
	# camProxy.setParam(vision_definitions.kCameraBrightnessID, 0)
	videoClient = camProxy.subscribe("python_client", resolution, colorSpace, fps)

	# Get a camera image.
	# image[6] contains the image data passed as an array of ASCII chars.
	naoImage = camProxy.getImageRemote(videoClient)

	camProxy.unsubscribe(videoClient)

	# Now we work with the image returned and save it as a PNG  using ImageDraw
	# package.

	# Get the image size and pixel array.
	imageWidth = naoImage[0]
	imageHeight = naoImage[1]
	print(imageWidth, imageHeight)
	array = naoImage[6]



	# Create a PIL Image from our pixel array.
	im = Image.frombytes("RGB", (imageWidth, imageHeight), array)

	filename = 'balls.png'

	# Save the image.
	im.save(filename, "PNG")
	

	process(filename)

def display_image(image):
	cv2.imshow('test', image)
	cv2.waitKey(0)


def get_color(img, x, y, r):
	height, width = img.shape[:2]
	roi_size = 20
	roi_values = img[(y-roi_size):(y+roi_size),(x-roi_size):(x+roi_size)]
	mean_blue = np.mean(roi_values[:,:,0])
	mean_green = np.mean(roi_values[:,:,1])
	mean_red = np.mean(roi_values[:,:,2])
	rgb = {"red":mean_red, "green":mean_green, "blue":mean_blue}
	return max(rgb, key=rgb.get)

def process(filename):
	print(filename)

	filename = 'old.png'
	image = cv2.imread(filename)
	# display_image(image)
	# display_image(image)

	# convert the image to greyscale
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# apply blur for noise reduction
	gray = cv2.medianBlur(gray, 7)
	# display_image(gray)

	# print(gray.shape)
	# rows = gray.shape[0]

	# # apply Hough gradient
	# circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 400)
	# circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows / 8, param1=200, param2=37, minRadius=1, maxRadius=300)
	

	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	img = cv2.medianBlur(gray, 17)
	# display_image(cimg)
	# detect circles in the image

	
	circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)

	balls = []
	print(circles)

	if circles is not None:
		circles = np.uint16(np.around(circles[0, :]).astype("int"))
		for (x, y, r) in circles:
			color = get_color(image, x, y, r)
			balls.append([x, y, r, color])
			center = (x, y)

			# marking detected circles
			cv2.circle(image, center, 1, (0, 100, 100), 2)
			cv2.circle(image, center, r, (255, 255, 255), 2)
	print(balls)
	print(len(balls))
	display_image(image)


takeImage()