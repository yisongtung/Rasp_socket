import socket
from datetime import datetime
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)              
GPIO.setup(17, GPIO.IN)

i=1                             
filename="Test-Run-"+str(datetime.now())+"Log.txt"

HOST ='10.0.1.29' # Server IP or Hostname
PORT = 12345 # Pick an open Port (1000+ recommended), must match the client sport
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

def write_time(i, start_time, end_time):                             
    with open(filename, "a") as log:                  
        log.write("{0},{1} ,{2}\n".format(i,str(start_time),str(end_time)))
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

# awaiting for message
while True:
    data = conn.recv(1024)
    print 'I sent a message back in response to: ' + data
    reply =''
    
    while True:
       if GPIO.input(17) == GPIO.LOW :
            #print '22'
            end_time=datetime.now()
            write_time(i, data, end_time)
            i = i + 1
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
