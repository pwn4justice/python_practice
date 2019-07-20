# -*- encoding: utf-8 -*-
# name:     wget.py - a small tool to simulate 'wget' in Windows
# author:   pwn4justice
# 待改进：  请求局域网 python -m http.server 时工作正常，请求网络IP
#           或者网站（如：baidu.com）则会 404,估计是没有完善的请求头
#           信息所以被拒绝；还有 ftp 功能没有完善；账号密码验证功能
#           等，注意有时间改进一下

import sys
import getopt
import socket
import re
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
    print("[*] Header: " + buffer.decode().strip())
    print("[*] Downloading Process: ", end="")

    while True:
        buffer = s.recv(1024)
        if not buffer:
            break
        if resource == '/':
            resource = "index.html"
        print("*", end="")

        #if isWebsite, then may use 'w' only??
        with open(resource, 'ab') as f:
            f.write(buffer)
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


    
