#DONT PUT THE RPI TO AUTO SLEEP/AUTO SCREEN OFF ETC ETC ETC
import config

import picamera
from subprocess import Popen
from twython import Twython
# from PIL import Image
from time import sleep
from gpiozero import Button, LED

# disable all power saving features
# restart to clear the settings
Popen(["xset", "s", "off"])
Popen(["xset", "-dpms"])
Popen(["xset", "s", "noblank"])

led1 = LED(config.LED_1)
led2 = LED(config.LED_2)

#5...4...3...2...1...
def countdown(sec):
	sec = int(sec)
	if sec > 5:
		led1.blink(on_time=0.25, off_time=0.25, n=4)
		led2.blink(on_time=0.25, off_time=0.25, n=4)
		sleep(1)
	elif sec >= 3:
		led1.blink(on_time=0.2, off_time=0.05, n=6)
		led2.blink(on_time=0.2, off_time=0.05, n=6)
		sleep(1)
	elif sec < 2:
		led1.blink(on_time=0.1, off_time=0.01, n=10)
		led2.blink(on_time=0.1, off_time=0.01, n=10)
		sleep(1)

def startCountdown(startSec):
	try:
		startSec = int(startSec)
	except:
		print("INPUT AN INTEGER")
	
	while startSec > 0:
		countdown(startSec)
		startSec -= 1

camera = picamera.PiCamera()

twitter = Twython(config.CONSUMER_KEY, config.CONSUMER_SECRET, config.ACCESS, config.ACCESS_SECRET)

#background
bg = Popen(["feh", "--fullscreen", "./bg-final.png"])

print(bg)

res = (1024, 768)

window = (int(1280/2 - 1024/2), int(1024/2 - 768/2)) + res

camera.start_preview(fullscreen=False, window=window)

while True:
	
	led1.on()
	led2.on()
	led1.blink()
	sleep(1)
	led2.blink()
	#checking Button.value == True in a loop is too stressful for rpi	
	Button(config.BUTTON).wait_for_press()
	#feh --fullscreen --slideshow-delay 1
	#feh -g 400x300 img.img
	countdownBG = Popen(["feh", "--fullscreen", "--slideshow-delay", "1", "./bg"])
	
	startCountdown(10)
	
	countdownBG.kill()
	camera.capture(("temp.jpg"), resize=(1440, 1080))
	camera.stop_preview()
	
	imagePreview = Popen(["feh", "-g", "1024x768+128+128", "-x", "temp.jpg"])
	sleep(2)
	photo = open("temp.jpg", "rb")
		
	try:
		twitter.update_status_with_media(media=photo, status="Testing, testing. Anyone can see me?")
		imagePreview.terminate()
		complete = Popen(["feh", "--fullscreen", "complete.png")]
		sleep(7)
		complete.terminate()
	except:
		failed = Popen(["feh", "--fullscreen", "failed.png")]
		sleep(7)
		failed.terminate()
		pass
		
	camera.start_preview(fullscreen=False, window=window)
	#imagePreview.terminate()

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
