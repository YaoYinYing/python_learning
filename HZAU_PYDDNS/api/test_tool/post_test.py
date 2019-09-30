import requests

data = {"token": "token",
        # set here if not default domain name record is modified.
        #"domain_name": "not default domain",
        "name" : "name"}
url = "https://host/HZAU_DDNS/api/index.py"


name_list = ["namelist"]

for name in name_list:
    data["name"] = name
    r = requests.post(url, data=data)
    print(r.status_code)
    print(r.content.decode())
