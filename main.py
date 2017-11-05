import config
import picamera
import sys
from twython import Twython
from PIL import Image
from time import sleep
from gpiozero import Button

#camera = picamera.PiCamera()

# img = Image.open("foo.jpg")

# overlol = camera.add_overlay(img.tobytes(), size=img.size)
#overlol.layer = 3
#alpha = 0 is transparent, and vice versa
#overlol.alpha = 0

twitter = Twython(config.CONSUMER_KEY, config.CONSUMER_SECRET, config.ACCESS, config.ACCESS_SECRET)

while True:

	#camera.start_preview(fullscreen=false, window=(x y height width))
	#camera.capture("bar.jpg")
	#camera.stop_preview()
	#photo = open("bar.jpg", "rb")
	Button(config.BUTTON).wait_for_press()

	try:
		twitter.update_status_with_media(media=photo, status="Testing, testing. Anyone can see me?")
		#TODO: Upload complete picture
		# feh -x filename
		sleep(5)
	except:
		#TODO: Upload Failed & check out the twitter acc. picture 
		sleep(5)
		pass
