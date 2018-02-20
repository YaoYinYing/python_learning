# -*- coding: utf8 -*-
# this script is developed and maintained by Yao Yin Ying.
# GitHub: https://github.com/YaoYinYing

# descriptions:
# Direct interaction with SCRAM encrypted router admin site is an extremely complicated problem when i tried to
# get some information from the device. The Huawei WS851 router uses this asymmetric encryption method to prevent
# the administration password from leaking in data transmission procedure by HTTP. By negotiating for a specific
# session id from request headers and cookies with users' browser, the SCRAM mechanism has provided a safety
# environment for user to visit the control panel web site. Here i use selenium and Chrome web driver to visit
# the website as if i do it with a real browser and get the specific session id so that the ordinary request
# can be easily achieved.

# Before everything goes, be sure the chrome web driver of latest version is in python path or linux PATH.

from selenium import webdriver
import time
import re
import requests


# login the Huawei Honor Router by Chrome and return session ID, encn(constant), ence(constant) from cookies
# Chrome will be closed by the value return
def loginRouter(host, password):
    browser = webdriver.Chrome()
    browser.get("http://" + host + "/html/index.html")

    # wait for the website loading
    time.sleep(1)
    input_pass = browser.find_element_by_id('userpassword')
    input_pass.send_keys(password)
    login_button = browser.find_element_by_id("loginbtn")
    login_button.click()

    # wait for the redirection and extract something from cookies
    time.sleep(1)
    login_cookies = browser.get_cookies()
    sessionID = browser.get_cookie("SessionID_R3")[u'value']
    encn = browser.get_cookie("encn")[u'value']
    ence = browser.get_cookie("ence")[u'value']

    # print login_cookies
    # print sessionID
    return sessionID, encn, ence
    pass


# request router information by specific session id, return wan ip
def getWanIp(host, session, encn):
    headers = {'Host': host,
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTM'
                      'L, like Gecko) Chrome/63.0.3239.132 Mobile Safari/537.36',
        'Referer': 'http://' + host + '/html/content.html', }
    cookie = {'_ga': 'GA1.1.1869922932.1513764915', 'activeMenuID': '1', '_gat': 'deviceinfo', 'ence': '010001',
              'SessionID_R3': session, 'encn': encn, 'test': 'cookietest'}
    url_getIp = 'http://' + host + "/api/ntwk/wan?type=active"

    response = requests.get(url=url_getIp, headers=headers, allow_redirects=True, cookies=cookie)

    # print response.content
    # print response.status_code

    wanIp = re.findall(r'"IPv4Addr":"(\d+.\d+.\d+.\d+)",', response.content)[0]

    print wanIp
    return wanIp
    pass


'''
test_login_session,test_encn,test_ence=loginRouter(host=???,password=???)
test_result=getWanIp(host=???,session=test_login_session,encn=test_ence)
'''
