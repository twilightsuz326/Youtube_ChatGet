import httplib2

def htmlget(url):
    http = httplib2.Http()
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36"}
    content = http.request(url, 'GET', headers=headers)[1].decode("utf-8")
    return content

    