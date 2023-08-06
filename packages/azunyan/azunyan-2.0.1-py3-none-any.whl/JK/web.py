import requests

def rGET(url, headers='default', cookies={}, timeout=30, retry=5):
    if headers == 'default':
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"
        }
    for i in range(retry):
        try:
            result = requests.get(url, headers=headers, cookies=cookies, timeout=timeout)
            return result
        except:
            print(F'Get failed, retry {i+1}/{retry}')
    print('Get failed')

def rPOST(url, data, headers='default', cookies={}, timeout=30, retry=5):
    if headers == 'default':
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"
        }
    for i in range(retry):
        try:
            result = requests.post(url, data=data, headers=headers, cookies=cookies, timeout=timeout)
            return result
        except:
            print(F'Post failed, retry {i+1}/{retry}')
    print('Post failed')
