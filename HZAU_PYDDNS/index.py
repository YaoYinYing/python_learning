#!python
# -*- coding: utf8 -*-
# hzau_ddns api based on alidns python sdk
# this script is developed and maintained by Yao Yin Ying.
# GitHub: https://github.com/YaoYinYing


import traceback
from aliyunsdkalidns.request.v20150109 import AddDomainRecordRequest
from aliyunsdkalidns.request.v20150109 import UpdateDomainRecordRequest
from aliyunsdkalidns.request.v20150109 import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109 import DescribeDomainRecordInfoRequest
import re
import time
import sms_dns_change as sms
from const import client, domain_name, token
import cgi
import json
import os

print("content-type:text/html")
print("")

log_file = "./Update.log"


def OK_response(response_code):
    response_code_dict = {"200.1 OK": "records created", "200.2 OK": "records unchanged",
                          "200.3 OK": "records modified."}
    print({response_code: response_code_dict[response_code]})


def get_client_ip_addr():
    if os.environ['REQUEST_SCHEME'] == "https":
        return os.environ['REMOTE_ADDR']
    else:
        print({"401": "HTTPS REQUEST SCHEME IS REQUIRED."})
        exit()


def post_data():
    form = cgi.FieldStorage()
    token_post = form.getvalue('token')
    # print("token_posted = %s" % token_post)
    record_name = form.getvalue('name')
    if token_post == token:
        return record_name
    else:
        print({"401": "token error"})
        exit()


# Step 1: describe full records
def describe_full_records(domain_name):
    descr = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    descr.set_action_name("DescribeDomainRecords")
    descr.set_DomainName(domain_name)
    try:
        response = client.do_action_with_exception(descr)
        r_j = json.loads(response.decode())
        return r_j
    except Exception as e:
        print({"500": "Connection error"})
        exit()


# Step 2: search name from existed records
def search_name_from_full_records(name, response_full):
    record_exist = False
    for item in response_full['DomainRecords']["Record"]:
        if name == item["RR"]:
            record_exist = True
            return record_exist, item
    else:
        return record_exist, []


# Step 3a:  if not name is not exists, create new records for the name
def create_record(domain_name, name, ip):
    add_domain_record = AddDomainRecordRequest.AddDomainRecordRequest()
    add_domain_record.set_action_name("AddDomainRecord")
    add_domain_record.set_DomainName(domain_name)
    add_domain_record.set_RR(name)
    add_domain_record.set_Type("A")
    add_domain_record.set_Value(ip)
    with open(log_file, 'a') as logfile:
        try:
            response = client.do_action_with_exception(add_domain_record)
            sms.dns_record_update_sms(name, "-".join(ip.split(".")))
            logfile.write("%s \t %s \n" % (str(time.asctime(time.localtime(time.time()))), response))
            OK_response("200.1 OK")
        except Exception as e:
            logfile.write("%s \t %s \n" % (str(time.asctime(time.localtime(time.time()))), traceback.print_exc()))
            print({"500": "Failed to create new record."})
            exit()


# Step 3b: if name exists, describe record for the name
# return ip value in record
def describe_name_record(record_id):
    describe_request = DescribeDomainRecordInfoRequest.DescribeDomainRecordInfoRequest()
    describe_request.set_action_name("DescribeDomainRecordInfo")
    describe_request.set_RecordId(record_id)
    with open(log_file, "a") as logfile:
        try:
            response = client.do_action_with_exception(describe_request).decode()
            ip_value_in_record = re.findall(r'\d+\.\d+\.\d+\.\d+', response)[0]
            return ip_value_in_record
        except Exception as e:
            logfile.write("%s \t %s \n" % (str(time.asctime(time.localtime(time.time()))), traceback.print_exc()))
            exit()


# Step 4. if name exists and changed in post, modify the name record.
def modify_record_name(name, record_id, new_ip_addr):
    ftpDnsModifyRequest = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
    ftpDnsModifyRequest.set_action_name("UpdateDomainRecord")
    ftpDnsModifyRequest.set_RecordId(record_id)
    ftpDnsModifyRequest.set_Type("A")
    ftpDnsModifyRequest.set_Value(new_ip_addr)
    ftpDnsModifyRequest.set_RR(name)
    with open(log_file, "a") as logfile:
        try:
            response = client.do_action_with_exception(ftpDnsModifyRequest)
            sms.dns_record_update_sms(name, "-".join(new_ip_addr.split(".")))
            logfile.write("%s \t %s \n" % (str(time.asctime(time.localtime(time.time()))), response))
            OK_response("200.3 OK")
        except Exception as e:
            logfile.write("%s \t %s \n" % (str(time.asctime(time.localtime(time.time()))), traceback.print_exc()))


client_ip = get_client_ip_addr()
name_post = post_data()
full_records_response = describe_full_records(domain_name)
is_name_existed, name_data = search_name_from_full_records(name_post, full_records_response)
if is_name_existed:
    # name record exists
    # compare and modify the records
    record_id = name_data['RecordId']
    ip_in_record = describe_name_record(record_id)
    if ip_in_record == client_ip:
        OK_response("200.2 OK")
    else:
        modify_record_name(name_post, record_id, client_ip)
else:
    create_record(domain_name, name_post, client_ip)
