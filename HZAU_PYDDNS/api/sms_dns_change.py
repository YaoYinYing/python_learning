#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import const
client = AcsClient(const.ACCESS_KEY_ID, const.ACCESS_KEY_SECRET, 'cn-hangzhou')
def dns_record_update_sms(name, newip):
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https') # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', const.admin_phonenumber)
    request.add_query_param('SignName', const.sms_signature)
    request.add_query_param('TemplateCode', const.sms_temp_code)
    request.add_query_param('TemplateParam', "{\"pcname\":\"" + name +"\",\"newip\":\"" + newip + "\"}")

    response = client.do_action(request)
    # python2:  print(response) 
    print(str(response, encoding = 'utf-8'))
