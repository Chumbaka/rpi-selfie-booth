import config

import picamera
from subprocess import Popen
from twython import Twython
# from PIL import Image
from time import sleep
from gpiozero import Button

#5...4...3...2...1...
def countdown(sec):
	sec = str(sec)
	print(sec)
	# sec = Popen(["feh", "-x", sec + ".jpg"])
	sleep(1)
	# sec.terminate()

camera = picamera.PiCamera()

twitter = Twython(config.CONSUMER_KEY, config.CONSUMER_SECRET, config.ACCESS, config.ACCESS_SECRET)

#background
bg = Popen(["feh", "-x", "bg.jpg"])

print(bg)

res = (800, 600)

window = (int(1024/2 - 800/2), int(768/2 - 600/2)) + res

camera.start_preview(fullscreen=False, window=window)

while True:
	
	if(Button(config.KILLBUTTON).is_pressed == True):
		break
	
	elif(Button(config.BUTTON).is_pressed == True):
		#5
		countdown(5)
		#4
		countdown(4)
		#3
		countdown(3)
		#2
		countdown(2)
		#1
		countdown(1)
		
		camera.capture("temp.jpg", resize=(1440, 1080)) #TODO: check resize whether affect image quality
		camera.stop_preview()
		
		imagePreview = Popen(["feh", "-x", "temp.jpg"]) #TODO: move to middle
		sleep(3)
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
		
		camera.start_preview(fullscreen=False, window=window)

camera.stop_preview()
bg.terminate()


#overlay in picamera is still not working as expected. not using it
#Image (Image.open & etc) is from the PIL Library

# img = Image.open("foo.jpg")
# over = camera.add_overlay(img.tobytes(), size=img.size)

#picamera preview defaults at layer 2

# over.layer = 3

#alpha = 0 is transparent, and vice versa

# over.alpha = 0