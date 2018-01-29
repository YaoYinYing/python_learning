from aliyunsdkcore.client import AcsClient
from aliyunsdkalidns.request.v20150109 import UpdateDomainRecordRequest
from aliyunsdkalidns.request.v20150109 import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109 import DescribeDomainRecordInfoRequest
import re
import time
import paramiko


def getCurrentIp():
    # get ifconfig data by ssh
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=#hostname#, port=22, username=user, password=pass)
    stdin, stdout, stderr = ssh.exec_command('ifconfig')
    res, err = stdout.read(), stderr.read()
    result = res if res else err
    ssh.close()

    # Cation! if the configuration of miwifi mini router is changed, this must be checked.
    wanip = re.findall(r'\d+\.\d+\.\d+\.\d+', result.decode())[8]
    return wanip
    pass

def DescribeFtp(client):
    descrRequest=DescribeDomainRecordInfoRequest.DescribeDomainRecordInfoRequest()
    descrRequest.set_action_name("DescribeDomainRecordInfo")
    descrRequest.set_RecordId(RecordID)
    try:
        response=client.do_action_with_exception(descrRequest).decode()
        ori_ip = re.findall(r'\d+\.\d+\.\d+\.\d+', response)[0]
        print(response)
        return ori_ip
        pass
    except Exception as e:
        print(e)
        pass
    pass


def ModifyFtpDnsRequest(client,IpAddr):
    ftpDnsModifyRequest = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
    ftpDnsModifyRequest.set_action_name("UpdateDomainRecord")
    ftpDnsModifyRequest.set_RecordId(RecordId)
    ftpDnsModifyRequest.set_Type("A")
    ftpDnsModifyRequest.set_Value(IpAddr)
    ftpDnsModifyRequest.set_RR(Value)
    logfile=open(logfile,"a")
    print("newip= %s\tori_ip= %s ,write the new ip in file." % (wanip,ori_ip))
    logfile.write("newip= %s\tori_ip= %s ,write the new ip in file.\n" % (wanip,ori_ip))

    try:
        response = client.do_action_with_exception(ftpDnsModifyRequest)
        print(response)
        logfile.write("%s \t %s \n" % (str(time.asctime( time.localtime(time.time()) )), response))
    except Exception as e:
        print(e)
        logfile.write("%s \t %s \n" % (str(time.asctime( time.localtime(time.time())) ), e))
    logfile.close()
    pass

# unused function, but necessaray for first time configuration
def DescribeDnsYYY(client):
    descr=DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    descr.set_action_name("DescribeDomainRecords")
    descr.set_DomainName(DomainName)
    logfile=open(logfile,"a")
    try:
        response=client.do_action_with_exception(descr)
        print(response)
        logfile.write("%s \t %s \n" % (str(time.asctime( time.localtime(time.time()) )), response))
        pass
    except Exception as e:
        print(e)
        logfile.write("%s \t %s \n" % (str(time.asctime( time.localtime(time.time())) ), e))
        pass
    logfile.close()
    pass

# def the client inf.
client=AcsClient(???,???,"cn-hangzhou")

# ori_ip: current Dns record, get from alidns
ori_ip=DescribeFtp(client)

# wanip: WAN IP or HZAU, get by ssh the miwifi mini
wanip=getCurrentIp()
print(wanip)

if ori_ip == wanip:
    print("newip= %s\tori_ip= %s , keep the original ip." % (wanip, ori_ip))
    logfile = open(logfile, "a")
    logfile.write("%s\nnewip= %s\tori_ip= %s , keep the original ip.\n" % (str(time.asctime( time.localtime(time.time()) )),wanip, ori_ip))
    logfile.close()
    pass
else:
    updateDns = ModifyFtpDnsRequest(client, wanip)
    pass
