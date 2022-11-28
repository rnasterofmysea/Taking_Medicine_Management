import requests

def image_data():
    ip = "http://192.168.0.6:8080"
    parameter = "/orb/img"
    res = requests.post(ip + parameter, headers = {'Content-Type': 'application/json'})
    res = res.content.decode('utf-8')
    print(type(res))
    print(res)
image_data()
