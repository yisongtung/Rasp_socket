import socket
import RPi.GPIO as GPIO
import time
from datetime import datetime 
import os

GPIO.setmode(GPIO.BCM)
#GPIO.setup(26, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(26,GPIO.IN)

HOST ='10.0.1.29' # Enter IP or Hostname of your server
PORT = 12345 # Pick an open Port (1000+ recommended), must match the server port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))



#Lets loop awaiting for your input
while True:
    
    inputValue = GPIO.input(26)
    if (inputValue == GPIO.LOW):
    #if GPIO.input(26):
    	#command = raw_input('button pressed')
    	print ("button pressed")
    	print (datetime.now())
        #s.send("button pressed")
        s.send(str(datetime.now()))
    time.sleep(0.1)



    #command = raw_input('Enter your command: ')
    #s.send(command)
    #reply = s.recv(1024)
    #if reply == 'Terminate':
    #    break
    #print reply
    
    

