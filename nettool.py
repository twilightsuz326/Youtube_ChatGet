import httplib2
import urllib
import urllib.request
import csv

http = httplib2.Http()

def htmlget(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36"}
    content = http.request(url, 'GET', headers=headers)[1].decode("utf-8")
    return content

def phpapi(body):
    content = http.request("https://superchat.jp/api/download.php", 
        method="POST", 
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        body=urllib.parse.urlencode(body) )[1].decode("utf-8")

    return content.splitlines()

def sendline(message):
    LINE_NOTIFY_URL = 'https://notify-api.line.me/api/notify'
    TOKEN = "RX2ZD1aGdtOhVWQwsJBowhvGtAbErW0f8pivQsgRB8m"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer ' + TOKEN
    }
    body = {
        'message': message,
    }
    data = urllib.parse.urlencode(body)

    req = urllib.request.Request(LINE_NOTIFY_URL, data=data.encode('utf-8'), method='POST', headers=headers)
    with urllib.request.urlopen(req) as res:
        print(res.read())
        response_body = res.read().decode("utf-8")

if __name__ == "__main__":
    sendline("a")