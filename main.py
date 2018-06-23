#DONT PUT THE RPI TO AUTO SLEEP/AUTO SCREEN OFF ETC ETC ETC
import config

import picamera
from time import sleep
from subprocess import Popen
from subprocess import PIPE
from twython import Twython
# from PIL import Image
from gpiozero import Button, LED


#5...4...3...2...1...
#TODO move out LED part so it is not hard-coded
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


# disable all power saving features
# restart to clear these settings
Popen(["xset", "s", "off"])
Popen(["xset", "-dpms"])
Popen(["xset", "s", "noblank"])

led1 = LED(config.LED_1)
led2 = LED(config.LED_2)

#run xrandr | grep '*' and obtain the resolution
xrandr = Popen(["xrandr"], stdout=PIPE)
grep = Popen(["grep", '*'], stdin=xrandr.stdout, stdout=PIPE)
xrandr.stdout.close()
res = str(grep.communicate()[0])
res = res.split("x")

res[0] = res.split("'") #using b' as a point of spliting

width = int(res[0][1].strip())
height = int(res[1].split(" ")[0])

res = (width, height)

camera = picamera.PiCamera()

twitter = Twython(config.CONSUMER_KEY, config.CONSUMER_SECRET, config.ACCESS, config.ACCESS_SECRET)

#background
bg = Popen(["feh", "--fullscreen", "./bg-final.png"])

print(bg)

#TODO configure the webcam to be in the middle according to the resolution
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

	#TODO open uploading image after preview
	photo = open("temp.jpg", "rb")
		
	try:
		twitter.update_status_with_media(media=photo, status="Testing, testing. Anyone can see me?")
		#TODO remember this one here
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

camera.stop_preview()
bg.terminate()


#overlay in picamera is still not working as expected. not using it
#Image (Image.open & etc) is from the PIL Library
