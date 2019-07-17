# introduction: - a small curl tool
#       author:   pwn4justice
#         date:   2019/7/15

import requests
import sys

def print_usage():
     print('''A curl tool build by: pwn4justice
Usage:
    curl www.site.com
            ...
        ''')
        

def curl(url):
    #a default header
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    html = requests.get(url, headers = headers)
    print()
    print(html.status_code)
    print(html.text)
    

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print_usage()
    else:
        url = sys.argv[1]
        if ('http' or 'https') not in url:
            url = 'http://' + url
            try:
                print("\nOpen Site: " + url, end='')
                curl(url)
                
            except Exception:
                url = 'https://' + url[7:]
                try:
                    print("\nOpen Site: " + url, end='')
                    curl(url)
                    
                except Exception:
                    print("\nFailed...\n")
                    print_usage()
