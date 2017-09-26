#### Hybrid Python test invloving  GPIO pin and Mplayer slave mode
import os
from time import sleep
from subprocess import call
import logging

####import GPIO library
import RPi.GPIO as GPIO

#set GPIO numbering mode and define input pin
GPIO.setmode(GPIO.BOARD)
GPIO.setup(37,GPIO.IN)

###Set up Logging
logging.basicConfig(filename='/tmp/hybrid.log',level=logging.DEBUG)
logging.debug("------ STARTING -------")
###Python Control of Mplayer

pipe = "/home/pi/swinggPipe"
song = "SWINGONE41117_516PM.aif"
#song = "HelloKatharine.wav"
#### Pipe Set Up
#pipeTry = call("sudo mkfifo " + pipe, shell=True)
#if (pipeTry):
#    logging.debug("pipe error; " + str(pipeTry))
#    logging.debug("try command: sudo rm " + pipe)

### Launch mplayer in slave  mode  FROM another script
#sleep (15)
#print ("launching mplayer")
#command = "mplayer " + song + " -loop 0 -slave -input file=" +pipe + " &"
#mplayerTry = call(command, shell=True)
#if (mplayerTry):
#    logging.debug("mplayer error: " + str(mplayerTry))
#else:
#    logging.debug("mplayer seems to be okay!")

#print ("playing 10 seconds of sound for calibration.")
#sleep(10)

#pausing mplayer
print ("pausing mplayer")
command = "echo pause > " + pipe
call(command, shell=True)
sleep(1)
### MAIN PROGRAM LOOP

###maybe try
# unPause = "echo pausing_keep . " + pipe
# pause = "echo pausing_toggle > " + pipe

unPause = "echo pause > " + pipe
pause = unPause

HIGH = True
LOW = False

activeState = HIGH #change to HIGH for active High

fadeInDuration  = 0.5      ### Time in seconds for fade in
fadeOutDuration = 0.5      ### Time in seconds for fade out
stayOnDuration  = 7.0      ### Time in seconds for music to stay on

isPaused = True

# Set up for pin commands...
while True:
	if (GPIO.input(37)==activeState and isPaused):
		call(unPause, shell=True)
                print "unPausing"
		
		command = ""
		print("testing fade in - " + str(int(fadeInDuration)) + " second fade in\n")

		for i in range(100):            #count up to 100%
    			command = "echo volume " + str(i) + " 1 >" + pipe
			call(command, shell=True)
			sleep(fadeInDuration/100)
		isPaused = False
        
        ### Stay on for stayOnTime - reset time if re-triggered
		i = 100
		while i > 0:
		  sleep(stayOnDuration/100)
		  i -= 1
		  if GPIO.input(37) == activeState:
                    i = 100

	elif (GPIO.input(37)== (not activeState) and not isPaused):
#Fade out is not happening.
		print "Pausing"

		command = ""
		fadeTime =0.5                  #Time in seconds for fade
		print("testing fade out - " + str(int(fadeOutDuration)) + " second fade out\n")

		for i in range(100,-1,-1):      #count down from 100%
			command = "echo volume " + str(i) + " 1 >" + pipe
			call(command, shell=True)
			sleep(fadeOutDuration/100)

		sleep(0.5)
		call (pause, shell=True)
		isPaused = True
	sleep(0.01)
