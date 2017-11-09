from socket import *
import time
from allgo_utils import *



client_socket = socket(AF_INET,SOCK_STREAM)
client_socket.connect(('localhost',8004))
ult=ultrasonic()


try:
    while True:
        dist= ult.distance()
        print "Distance: %.1f cm" % dist
        client_socket.send(str(dist))
        time.sleep(0.1)
finally:
    client_socket.close()




