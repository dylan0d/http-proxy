import os, sys, socket
from thread import *

proxy_port = int(raw_input("Enter desired port number: "))
block_list = []


max_conn= 50 #maximum number of connections
max_buffer= 8192 #maximum number bytes that can be received at once

def begin():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', proxy_port))
        s.listen(max_conn)
        print "socket initialised succesfully"

    except Exception, e:
        print e
        print "failed to initialise socket"
        sys.exit(2)
    while 1:
        connection, address = s.accept()
        start_new_thread(web_proxy, (connection, address))

    s.close()

def web_proxy(connection, address):
    browser_request = connection.recv(max_buffer) #request from browser
    first_line = browser_request.split('\n')[0]
    url = first_line.split(' ')[1] #url is the 2nd word of the 1st line

    if not url.find("://") == -1:
        url = url[url.find("://")+3:]

    webserver_pos = url.find("/")
    if webserver_pos == -1:
      webserver_pos = len(url)
    url= url[:webserver_pos]

    port_pos=url.find(':')

    if port_pos == -1:
        port = 80
    else:
        port = int(url[port_pos+1:])
        url = url[:port_pos]

    f = open('blocked.txt', 'r')
    block_list = f.read().split('\n')

    if any (b in url for b in block_list):
        print "Website Blocked"
        connection.send("Website Blocked :(")
        connection.close()
        sys.exit(3)
    else:

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((url, port))
            s.send(browser_request) #send request from browser to website

            print "Connection established"

        except:
            print "Illegal request"
            s.close()
            connection.close()
            sys.exit(1)

        while 1:
            data = s.recv(max_buffer)
            if (len(data) >0):
                connection.send(data)#send received data from proxy to browser
                                    #while replies are non 0 length
                print "Received", url
            else:
                break

    s.close()
    connection.close()


    '''    filename = browser_request.split()[1].partition("/")[2]
        fileExist = "false"
        filetouse = "/" + filename
        print "Attempting to connect to ", url, "on port", port

        try:
            # Check whether the file exists in the cache
            f = open(filetouse[1:], "r")
            outputdata = f.readlines()
            fileExist = "true"
            print 'File Exists!'

            # ProxyServer finds a cache hit and generates a response message
            connection.send("HTTP/1.0 200 OK\r\n")
            connection.send("Content-Type:text/html\r\n")

            # Send the content of the requested file to the client
            for i in range(0, len(outputdata)):
                connection.send(outputdata[i])
            print 'Read from cache'

        except IOError:
            if fileExist == "false":
                hostn = filename.replace("www.", "", 1)

                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((url, port))
                    s.send(browser_request) #send request from browser to website

                    fileobj = s.makefile('r', 0)
                    fileobj.write("GET " + "http://" + filename + " HTTP/1.0\n\n")

                    buff = fileobj.readlines()

                    tmpFile = open("./" + filename, "wb")
                    print "request sent"
                    for i in range(0, len(buff)):
                        tmpFile.write(buff[i])
                        conn.send(buff[i])

                    print "Connection established"
                except:
                    print "Illegal request"
                    s.close()
                    connection.close()
                    sys.exit(1)

            else:
                 print "File not Found" '''
begin()
