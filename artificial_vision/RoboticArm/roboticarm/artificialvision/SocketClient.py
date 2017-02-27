'''
import socket

print('flag1')
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('flag2')
clientsocket.connect(('172.16.69.174', 8089))
x= 99
y= 10
clientsocket.send(str.encode('hello\n',encoding="UTF-8"))

print('inizio')
#clientsocket.send(str.encode(str(x) + ", "+ str(y),encoding="UTF-8"))
print('fine')
'''

import socket

x= 99
y= 10

soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print('flag2')
soc.connect(("172.16.69.174", 8089))

print('flag3')
#clients_input = input("What you want to proceed my dear client?\n")
clients_input = str(x) + "," + str(y) + "\n"
nbyte = soc.send(clients_input.encode("utf8")) # we must encode the string to bytes

print(nbyte)

soc.shutdown(socket.SHUT_RDWR)
soc.close()