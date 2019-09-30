# def the client inf.
from aliyunsdkcore.client import AcsClient


# request method limit, set True if post is allowed only.
request_method_limit=False

# aliyun cloud service setting
client = AcsClient()
ACCESS_KEY_ID = ""
ACCESS_KEY_SECRET = ""

# Server setting
token =""
# default domain
domain_name =""
# domain list
domain_name_list =['']

# SMS message setting, remain blank if not used.
admin_phonenumber=""
sms_signature=""
sms_temp_code=""

# serverchan message setting, remain blank if not used.
serverchan_SCKEY=""
