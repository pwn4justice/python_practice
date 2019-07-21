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
    pass


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

    if 'www' in host:
        host = '.'.join(host.split('.')[1:])

    if url.path != '':
        resource = url.path.split('/')[-1:][0]

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

    if isWebsite(host):
        pass

    msg = "GET " + resource + " HTTP/1.1"
    msg += "\r\n\r\n"

    msg = bytes(msg, encoding='utf-8')
    s.send(msg)
    buffer = s.recv(1024)
    print("[*] Header: \n" + buffer.decode().strip())
        
    # get Content-Length:
    content_length = re.findall("Content-Length:\s(.*?)\s\s", buffer.decode().strip(), re.M)[0]
    content_length = int(content_length)
    contentMB = content_length / 1024 / 1024
    print("[*] Size: %.2f MB" % contentMB)

    # record downloaded size
    size = 0
    blocks = content_length/50
    k = int( blocks - 1024 * ( blocks // 1024) )

    ## time start 
    start = time.time()
    while True:
        buffer = s.recv(1024)
        
        ## show download bar
        size += len(buffer)
        print('\r' + "[*] Downloading Process: %s%.2f%%" % ('>' * (size * 50 // content_length), size / content_length * 100), end='')
        
        if not buffer:
            break
        if resource == '/':
            resource = "index.html"

        with open(resource, 'ab') as f:
            f.write(buffer)
    
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
    #if url is not an ip address, it will return 'bad request - 404'
    #so when using this tool to wget a website, should constuct a more
    #complicated request HEADER!!!
    if username and password:
        retrieveData(url, username=username, password=password)
    else:
        retrieveData(url)


    
