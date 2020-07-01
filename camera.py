import numpy as np
from cv2 import cv2
from PIL import Image

import vision_definitions
from naoqi import ALProxy

ip = "127.0.0.1"
port = 9559


def takeImage(filename):

	camProxy = ALProxy("ALVideoDevice", ip, port)
	resolution = vision_definitions.kVGA  # VGA
	colorSpace = vision_definitions.kRGBColorSpace  # RGB
	fps = 1
	videoClient = camProxy.subscribe("python_client", resolution, colorSpace, fps)
	naoImage = camProxy.getImageRemote(videoClient)
	camProxy.unsubscribe(videoClient)

	# filename = 'balls.png'
	# Get the image size and pixel array.
	width = naoImage[0]
	height = naoImage[1]
	array = naoImage[6]

	im = Image.frombytes("RGB", (width, height), array)
	im.save(filename, "PNG")

takeImage('test.png')