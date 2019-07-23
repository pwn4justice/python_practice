# 
# -*- encoding: utf-8 -*-
# wget.py - a small tool to mock 'wget' in windows
# author : pwn4justice
# 

import sys
import getopt
import socket
import re
import time
from urllib import parse

def isWebsite(host):
    if not re.match("^([0-9]\.?)", host):
        return True
    else:
        return False
    

def usage():
    print("usage: wget.py -u 'site' [options]")
    print("options:")
    print("\t\t -h, --help \t\t show this page.")
    print("\t\t -u, --url \t\t must follow an url.")
    print("\t\t -i \t\t\t using username and password.")
    pass


def retrieveData(url, username=None, password=None):

    # split host and port
    url = parse.urlparse(url)
    host = url.netloc
    port = 80
    resource = '/'

    if re.match(".*?:[0-9]+", url.netloc):
        host = url.netloc.split(':')[0]
        port = int(url.netloc.split(':')[1])

    #if 'www' in host:
    #    host = '.'.join(host.split('.')[1:])

    if url.path != '':
        #resource = url.path.split('/')[-1:][0]
        resource = url.path
        
    # Print Info:
    print("Host: \t" + host)
    print("Port: \t" + str(port))
    print("Get: \t" + resource)
    print('-' * 20)
    print("[*] Start to download ... ") 

    # start to retrieve 
    # construct GET requests
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))

    #construct a request msg
    msg = "GET " + resource + " HTTP/1.1\r\n"
    
    if isWebsite(host):
        header_host = "Host: %s\r\n" % host
        msg += header_host
        
    msg += "\r\n\r\n"
    print(msg)
    msg = bytes(msg, encoding='utf-8')
    
    #send
    s.send(msg)
    buffer = s.recv(2048)
    
    print(buffer)
    #split head and body
    header = buffer.decode().split('\r\n\r\n')[0]
    body = buffer.decode().split('\r\n\r\n')[1]
    
    print("[*] Header: \n" + header.strip())

    # get Content-Length:
    try:
        content_length = re.findall("Content-Length:\s(.*?)\s\s", header.strip(), re.M)[0]
        content_length = int(content_length)
        contentMB = content_length / 1024 / 1024
    except IndexError:
        content_length = 0
        contentMB = 0
    print("[*] Size: %.2f MB" % contentMB)
    #print("[*] Body: %s \n" % body.strip())

    # record downloaded size
    size = 0
    
    ## time start 
    start = time.time()
    body = bytes(body.encode('utf-8'))
    
                    
    if resource == '/':
        resource = "index.html"
    else:
        resource = resource.split('/')[-1]
        
    while True:
        if len(body):
            with open(resource, 'ab') as f:
                f.write(body)
            body = ""         
        s.settimeout(5.0)
        
        try:
            buffer = s.recv(1024)
        except socket.timeout:
            buffer = b""
            break                      
        
        if not len(buffer):
            break          
        
        with open(resource, 'ab') as f:
            f.write(buffer)

        ## show download bar
        try:
            size += len(buffer)
            print('\r' + "[*] Downloading Process: %s%.2f%%" % ('>' * (size * 50 // content_length), size / content_length * 100), end='')
        except ZeroDivisionError:
            print("No data was retrieved, shutdown ...")
            sys.exit()
            
    ## time end
    end = time.time()
    print("\n[*] Download Complete! ")
    print("[*] Cost: %.2fs ; Save to: %s - %.2f MB" % ( end-start, resource, contentMB))
    print("")
    s.close()

if __name__ == "__main__":
    args = sys.argv[1:]
    try:
        opts, args = getopt.getopt(args, 'hu:i',["help","url="])
    except getopt.GetoptError:
        print("getopt.GetoptError")
        sys.exit(2)

    username = None
    password = None
    url_set = False

    for o, v in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit(-1)
        elif o in ('-i', ):
            if url_set:   
                username = input("username: ")
                password = input("password: ")
        elif o in ('-u', '--url'):
            url_set = True
            url = v 
        else:
            usage()
            sys.exit(-1)
    
    # start handling
    if not url_set:
        usage()
        sys.exit(1)     # 1: url not set!
        
    if 'http://' not in url and 'https://' not in url:
         url = 'http://' + url

    print('-' * 20)
    print("URL: \t" + url)

    if username and password:
        retrieveData(url, username=username, password=password)
    else:
        retrieveData(url)


    
