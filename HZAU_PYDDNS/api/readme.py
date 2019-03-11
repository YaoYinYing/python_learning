#!python
#coding:utf-8

'''

DNS data
----------------
a. describe full records
    descr = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    descr.set_action_name("DescribeDomainRecords")
    descr.set_DomainName("yinlab.cn")
    response = client.do_action_with_exception(descr)
b. describe record info (for one record)
    descrRequest = DescribeDomainRecordInfoRequest.DescribeDomainRecordInfoRequest()
    descrRequest.set_action_name("DescribeDomainRecordInfo")
    descrRequest.set_RecordId("3716386743014400")
    response = client.do_action_with_exception(descrRequest).decode()
c. Modify Record
    ftpDnsModifyRequest = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
    ftpDnsModifyRequest.set_action_name("UpdateDomainRecord")
    ftpDnsModifyRequest.set_RecordId(RecordId)
    ftpDnsModifyRequest.set_Type("A")
    ftpDnsModifyRequest.set_Value(IpAddr)
    ftpDnsModifyRequest.set_RR("ftp")
    response = client.do_action_with_exception(ftpDnsModifyRequest)
'''
'''

for client post
----------------
data = { 'token': "token","name": "name"}

'''
