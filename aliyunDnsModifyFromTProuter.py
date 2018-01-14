# -*- coding: utf8 -*-

from aliyunsdkcore.client import AcsClient
from aliyunsdkalidns.request.v20150109 import UpdateDomainRecordRequest
from aliyunsdkalidns.request.v20150109 import DescribeDomainRecordsRequest
import base64
import re
import requests

# this function works to traditional TP\MW router interface by the base64 encoded auth cookie.
# without the login function, the getWanIp function can still work by referring the header and cookie contents.
# headers are acquired, or the silly router will tell you "You have no authority to access this device!"

client=AcsClient(AccessKey,AccessSecret,"cn-hangzhou")

def getWanIp(host,cookie):
    password_base64 = base64.b64encode("admin:" + password)
    headers = {
        'Host': host,
        'User-Agent' : 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; BOIE9;ZHCN)',
        'Referer' : 'http://'+ host +'/userRpm/StatusRpm.htm',
        }
    url_getIp = 'http://' + host+ "/userRpm/StatusRpm.htm"
    cookie = {"Authorization": "Basic " + password_base64,"ChgPwdSubTag":""}
    try:
        response = requests.get(url=url_getIp, cookies=cookie, headers=headers)

        wanIp=re.findall(r'varwanPara=newArray\((.+?)\)',''.join(response.text.split()))[0].split(",")[2]
        print wanIp
        return wanIp
    except Exception, e:
        print e

    pass

def ModifyFtpDnsRequest(client,IpAddr):
    DnsModifyRequest = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
    DnsModifyRequest.set_action_name("UpdateDomainRecord")
    DnsModifyRequest.set_RecordId(RecordID)
    DnsModifyRequest.set_Type("A")
    DnsModifyRequest.set_Value(IpAddr)
    DnsModifyRequest.set_RR(RecordName)
    try:
        response = client.do_action_with_exception(DnsModifyRequest)
        print response
    except Exception,e:
        print e

    pass

host = host
password=pass
getip=getWanIp(host,password)

def DescribeDns(client):
    descr=DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    descr.set_action_name("DescribeDomainRecords")
    descr.set_DomainName(DomainName)
    try:
        response=client.do_action_with_exception(descr)
        print response
        pass
    except Exception, e:
        print e
        pass

    pass

# first add, get RecordID for modify

# vaddReq=DescribeDnsclient)

# for modification, to get rid of the code problem, use re to filt the ip addr
modifyDns=ModifyFtpDnsRequest(client,re.findall(r'\d+\.\d+\.\d+\.\d+',getWanIp(host,password))[0])
