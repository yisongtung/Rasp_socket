import socket
from datetime import datetime
import RPi.GPIO as GPIO

import smbus
import time

GPIO.setmode(GPIO.BCM)              
GPIO.setup(17, GPIO.IN)

i=1                             
filename="Test-Run-"+str(datetime.now())+"Log.txt"

#HOST ='192.168.43.73' # Server IP or Hostname
HOST = '10.0.1.34'
PORT = 12345 # Pick an open Port (1000+ recommended), must match the client sport
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

def write_time(i, data, start_time, end_time, delta):                             
    with open(filename, "a") as log:                  
        log.write("{0},{1} ,{2}, {3}, {4}\n".format(i, str(data), str(start_time), str(end_time), str(delta)))
        #log.write("{0},{1}\n".format(i,str(current_time)))

#managing error exception
try:
    s.bind((HOST, PORT))
except socket.error:
    print 'Bind failed '

s.listen(5)
print 'Socket awaiting messages'
(conn, addr) = s.accept()
print 'Connected'


# Define some device parameters
I2C_ADDR  = 0x27 # I2C device address
LCD_WIDTH = 16   # Maximum characters per line

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

#Open I2C interface
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1

def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off 
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = the data
  # mode = 1 for data
  #        0 for command

  bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
  bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

  # High bits
  bus.write_byte(I2C_ADDR, bits_high)
  lcd_toggle_enable(bits_high)

  # Low bits
  bus.write_byte(I2C_ADDR, bits_low)
  lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
  # Toggle enable
  time.sleep(E_DELAY)
  bus.write_byte(I2C_ADDR, (bits | ENABLE))
  time.sleep(E_PULSE)
  bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
  time.sleep(E_DELAY)

def lcd_string(message,line):
  # Send string to display

  message = message.ljust(LCD_WIDTH," ")

  lcd_byte(line, LCD_CMD)

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)



# awaiting for message
lcd_init()
while True:
    data = conn.recv(1024)
    print 'Start Time : ' + data
    
    reply =''
    if (data != ''):
        start_time = datetime.now()
        lcd_string(datetime.now().strftime("%H:%M:%S"),LCD_LINE_1)
    
    while True:
       if GPIO.input(17) == GPIO.LOW :
            #print '22'
            end_time=datetime.now()
            delta = end_time - start_time
            print start_time, end_time, delta.total_seconds()
            write_time(i, data, start_time, end_time, delta.total_seconds())
            i = i + 1
            #lcd_string(str(end_time),LCD_LINE_1)
            lcd_string(end_time.strftime("%H:%M:%S"),LCD_LINE_1)
            lcd_string(str(delta),LCD_LINE_2)
            break
    #write_time(i, data)
    #i = i + 1


    # process your message
    if data == 'Hello':
        reply = 'Hi, back!'
    elif data == 'This is important':
        reply = 'OK, I have done the important thing you have asked me!'

    #and so on and on until??    
    elif data == 'quit':
        conn.send('Terminate')
        break
    else:
        reply = 'Unknown command'
 
    # Sending reply
    conn.send(reply)
conn.close() # Close connections
