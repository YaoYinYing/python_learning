#!python
# -*- coding: utf8 -*-
# hzau_ddns api based on alidns python sdk
# this script is developed and maintained by Yao Yin Ying.
# GitHub: https://github.com/YaoYinYing


import traceback

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordInfoRequest import DescribeDomainRecordInfoRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest


import time
import sms_dns_change as sms
from const import client, domain_name, token
import cgi
import json
import os
from ddns_db import insert_change,exist_and_count



log_file = "./Update.log"

def error_response(response_code):
    response_code_dict = {"401.1": "HTTPS REQUEST SCHEME IS REQUIRED.",
                          "401.2": "TOKEN ERROR",
                          "503.1": "CONNECTION ERROR",
                          "503.2": "Failed to create new record.",
                          "503.3": "Failed to read full records.",
                          "503.4": "Failed to renew record.",
                          }
    # print("HTTP/1.1 %s OK\r\n" % response_code.split(".")[0])
    print("content-type:text/html")
    print("")
    print({response_code: response_code_dict[response_code]})
    exit()
    pass

def OK_response(response_code):
    response_code_dict = {"200.1 OK": "records created", "200.2 OK": "records unchanged",
                          "200.3 OK": "records modified."}
    #print("HTTP/1.1 200 OK\r\n")
    print("content-type:text/html")
    print("")
    print({response_code: response_code_dict[response_code]})


def get_client_ip_addr():
    if os.environ['REQUEST_SCHEME'] == "https":
        return os.environ['REMOTE_ADDR']
    else:
        error_response("401.1")
        #print({"401.1": "HTTPS REQUEST SCHEME IS REQUIRED."})
        


def post_data():
    form = cgi.FieldStorage()
    token_post = form.getvalue('token')
    # print("token_posted = %s" % token_post)
    record_name = form.getvalue('name')
    if token_post == token:
        return record_name
    else:
        error_response("401.2")
        #print({"401.2": "TOKEN ERROR"})
        


# Step 1: describe full records，updated 
def describe_full_records(domain_name):
    request = DescribeDomainRecordsRequest()
    request.set_accept_format('json')
    request.set_DomainName(domain_name)
    try:
        response = client.do_action_with_exception(request)
        return json.loads(response.decode())
    except Exception as e:
        error_response("503.1")
        #print({"503.1": "CONNECTION ERROR"})
        


# Step 2: search name from existed records
def search_name_from_full_records(name, response_full):
    record_exist = False
    for item in response_full['DomainRecords']["Record"]:
        if name == item["RR"]:
            record_exist = True
            return record_exist, item
    else:
        return record_exist, []


# Step 3a:  if name is not exists, create new record for the name, updated
def create_record(domain_name, name, ip):
    request = AddDomainRecordRequest()
    request.set_accept_format('json')
    request.set_DomainName(domain_name)
    request.set_RR(name)
    request.set_Type("A")
    request.set_Value(ip)
    with open(log_file, 'a') as logfile:
        try:
            response = client.do_action_with_exception(request)
            sms.dns_record_update_sms(name, "-".join(ip.split(".")))
            logfile.write("%s \t %s \n" % (str(time.asctime(time.localtime(time.time()))), response))
            r_j = json.loads(response.decode())
            request_id = r_j["RequestId"]
            record_id = r_j["RecordId"]
            insert_change(request_id=request_id,record_id = record_id,domain=domain_name, name =name,ip_addr= ip)
            exist_and_count(domain_name,name,record_id)
            OK_response("200.1 OK")

        except Exception as e:
            logfile.write("%s \t %s \n" % (str(time.asctime(time.localtime(time.time()))), traceback.print_exc()))
            error_response("503.2")
            #print({"503.2": "Failed to create new record."})
            


# Step 3b: if name exists, describe record for the name, updated
# return ip value in record
def describe_name_record(record_id):
    request = DescribeDomainRecordInfoRequest()
    request.set_accept_format('json')
    request.set_RecordId(record_id)
    with open(log_file, "a") as logfile:
        try:
            response = client.do_action_with_exception(request).decode()
            ip_value_in_record = json.loads(response)['Value']
            return ip_value_in_record
        except Exception as e:
            logfile.write("%s \t %s \n" % (str(time.asctime(time.localtime(time.time()))), traceback.print_exc()))
            error_response("503.3")
            #print({"503.3": "Failed to read full records."})
            


# Step 4. if name exists and changed in post, modify the name record. updated
def modify_record_name(domain_name, name, record_id, new_ip_addr):
    request = UpdateDomainRecordRequest()
    request.set_accept_format('json')
    request.set_RecordId(record_id)
    request.set_RR(name)
    request.set_Type("A")
    request.set_Value(new_ip_addr)
    with open(log_file, "a") as logfile:
        try:
            response = client.do_action_with_exception(request)
            sms.dns_record_update_sms(name, "-".join(new_ip_addr.split(".")))
            logfile.write("%s \t %s \n" % (str(time.asctime(time.localtime(time.time()))), response))
            r_j = json.loads(response.decode())
            request_id = r_j["RequestId"]
            record_id = r_j["RecordId"]
            insert_change(request_id=request_id, record_id=record_id, domain=domain_name, name=name, ip_addr=new_ip_addr)
            exist_and_count(domain_name, name, record_id)
            OK_response("200.3 OK")
        except Exception as e:
            logfile.write("%s \t %s \n" % (str(time.asctime(time.localtime(time.time()))), traceback.print_exc()))
            error_response("503.4")
            #print({"503.4": "Failed to renew record."})
            


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
        exist_and_count(domain_name, name_post, record_id)
        OK_response("200.2 OK")
    else:
        modify_record_name(domain_name, name_post, record_id, client_ip)
else:
    create_record(domain_name, name_post, client_ip)
