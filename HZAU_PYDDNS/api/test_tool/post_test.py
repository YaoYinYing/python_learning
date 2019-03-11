import requests

data = {"token": "my_token",
        "name" : "record_name"}
url = "https://host/DDNS/api/index.py"

r= requests.post(url, data=data)
# print(r.status_code)
print(r.content.decode())
