from urllib import request

while True:
    try:
        request.urlretrieve("http://www.python.org", "python.html")
        break
    except Exception as e:
        print(e)
