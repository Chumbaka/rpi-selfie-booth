import editThis
import picamera
from twython import Twython
from PIL import Image
from time import sleep
from gpiozero import Button

button = Button(2)

#camera = picamera.PiCamera()
#camera.start_preview()

# img = Image.open("foo.jpg")

# overlol = camera.add_overlay(img.tobytes(), size=img.size)

twitter = Twython(editThis.CONSUMER_KEY, editThis.CONSUMER_SECRET, editThis.ACCESS, editThis.ACCESS_SECRET)

button.wait_for_press()
print("finally")

#camera.capture("bar.jpg")
#camera.stop_preview()
#photo = open("bar.jpg", "rb")

# twitter.update_status_with_media(media=photo, status="Testing, testing. Anyone can see me?")



