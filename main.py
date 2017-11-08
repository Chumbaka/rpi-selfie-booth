import config

import picamera
from subprocess import Popen
from twython import Twython
# from PIL import Image
from time import sleep
from gpiozero import Button

camera = picamera.PiCamera()

#overlay in picamera is still not working as expected. not using it
#Image (Image.open & etc) is from the PIL Library
# img = Image.open("foo.jpg")
# over = camera.add_overlay(img.tobytes(), size=img.size)
#picamera preview defaults at layer 2
# over.layer = 3
#alpha = 0 is transparent, and vice versa
# over.alpha = 0

twitter = Twython(config.CONSUMER_KEY, config.CONSUMER_SECRET, config.ACCESS, config.ACCESS_SECRET)

#STEM background

bg = Popen(["feh", "-x", "bg.jpg"])

print(bg)

camera.start_preview(fullscreen=False, window=(20, 20, 1080, 1080))
animation = Popen(["animate", "k2ybPvSfRQuK.gif"])

while True:
	
	if(Button(config.KILLBUTTON).is_pressed == True):
		break
	
	elif(Button(config.BUTTON).is_pressed == True):
		#5
		#4
		#3
		#2
		#1
		
		camera.capture("temp.jpg")
		camera.stop_preview()
		imagePreview = Popen(["feh", "-x", "temp.jpg"])
		sleep(5)
		#photo = open("bar.jpg", "rb")
		
		try:
			#twitter.update_status_with_media(media=photo, status="Testing, testing. Anyone can see me?")
			#TODO: Upload complete picture
			# feh -x filename
			sleep(5)
		except:
			#TODO: Upload Failed & check out the twitter acc. picture 
			sleep(5)
			pass
		
		camera.start_preview()

camera.stop_preview()
bg.terminate()
