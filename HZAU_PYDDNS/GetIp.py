# -*- coding: utf8 -*-
# this script is developed and maintained by Yao Yin Ying.
# GitHub: https://github.com/YaoYinYing


import re
import requests


def getIpByNetSpeedTest():
    r=requests.get("http://www.speedtest.net")
    HZAU_IP = re.findall(r'122\.205\.\d{1,3}\.\d{1,3}',r.content.decode())[0]
    print(HZAU_IP)

    return HZAU_IP
    pass

if __name__=="__main__":

    getIpByNetSpeedTest()
    pass
