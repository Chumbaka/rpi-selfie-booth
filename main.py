import config
import picamera
from twython import Twython
from PIL import Image
from time import sleep
from gpiozero import Button

button = Button(config.BUTTON)

#camera = picamera.PiCamera()

# img = Image.open("foo.jpg")

# overlol = camera.add_overlay(img.tobytes(), size=img.size)

twitter = Twython(config.CONSUMER_KEY, config.CONSUMER_SECRET, config.ACCESS, config.ACCESS_SECRET)

while True:

	#camera.start_preview()
	#camera.capture("bar.jpg")
	#camera.stop_preview()
	#photo = open("bar.jpg", "rb")

	try:
		twitter.update_status_with_media(media=photo, status="Testing, testing. Anyone can see me?")
		#TODO: Upload complete picture
		sleep(5)
	except:
		#TODO: Upload Failed & check out the twitter acc. picture 
		sleep(5)
		pass