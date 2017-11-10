#DONT PUT THE RPI TO AUTO SLEEP/AUTO SCREEN OFF ETC ETC ETC
import config

import picamera
from subprocess import Popen
from twython import Twython
# from PIL import Image
from time import sleep
from gpiozero import Button

# disable all power saving features
Popen(["xset", "s", "off"])
Popen(["xset", "-dpms"])
Popen(["xset", "s", "noblank"])

#5...4...3...2...1...
def countdown(sec):
	sec = str(sec)
	print(sec)
	
	sleep(1)

camera = picamera.PiCamera()

twitter = Twython(config.CONSUMER_KEY, config.CONSUMER_SECRET, config.ACCESS, config.ACCESS_SECRET)

#background
bg = Popen(["feh", "-x", "./img/bg.png"])

print(bg)

res = (1024, 768)

window = (int(1280/2 - 1024/2), int(1024/2 - 768/2)) + res

camera.start_preview(fullscreen=False, window=window)

while True:
	
	#checking Button.value == True in a loop is too stressful for rpi	
	Button(config.BUTTON).wait_for_press()
	#feh --fullscreen --slideshow-delay 1
	#feh -g 400x300 img.img
	countdownBG = Popen(["feh", "--fullscreen", "--slideshow-delay", "1", "./img/"])
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
	
	countdownBG.kill()
	camera.capture(("temp.jpg"), resize=(1440, 1080)) #TODO: check resize whether affect image quality
	camera.stop_preview()
	
	imagePreview = Popen(["feh", "-g", "1024x768+128+128", "-x", "temp.jpg"])#TODO: open in middle
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
	imagePreview.terminate()

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
