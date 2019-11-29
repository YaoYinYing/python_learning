

# 【文档】HZAU DDNS动态解析

`_维护者：Yao Yin Ying_`

### 目的

校园网为拨号上网，由网络中心DHCP服务器动态分配IP地址。而固定IP需要以学校职工名义向网络中心提分配的出申请，再经过各级审批，步骤多，耗时长。为保证在校园网内顺利提供服务，本人根据阿里云公开API编写了HZAU DDNS动态解析服务。该服务适用于：

*   动态解析校园网内服务器域名
*   跳过IP固定申请，在校园网内提供服务（不固定IP，不开放对外端口）
*   作为心跳检测，监控服务器是否离线
*   监测和记录校园网网络故障事件

### 项目地址
该项目已经移动到：

[https://github.com/YaoYinYing/HZAU_DDNS](https://github.com/YaoYinYing/HZAU_DDNS)


此处项目不再更新。
### 服务端部署

1.  安装Anaconda3
2.  安装阿里云python sdk： `pip install aliyun-python-sdk-core`
3.  安装阿里云解析DNS sdk：`pip install aliyun-python-sdk-alidns`
4.  安装OpenSSL支持：`pip install pyopenssl`
5.  申请阿里云域名和云解析
6.  申请阿里云解析和短信服务操作权限的RAM子账号
7.  申请阿里云短信服务模板， 注意参数“pcname”和“newip” 分别对应子域名和IP地址（已改写为短线相连格式，原格式会被阿里云短信平台拦截）
8.  在HTTP服务器的配制文件中设置py文件为可执行
9.  在HTTP服务器的配制文件中设置https访问，注意添加证书
10.  将api目录下的文件释放至服务器下子目录，
11.  修改const.py中的参数，如下：

项目 | 属性 | 值 | 默认值与定义
----|-----|----|-----
request_method_limit | Boolean | - |False，若为True则禁止get
client | AcsClient实例 | RAM账号* | ""，必填
ACCESS_KEY_ID | str | RAM账号** | ""，必填 
ACCESS_KEY_SECRET | str | RAM账号** | ""，必填
token | str | 动态解析口令 | ""，必填
domain_name | str | 域名| ""，必填
domain_name_list | str list | 域名列表| []，必填
admin_phonenumber | str | 手机号码| ""，放空则不发短信
sms_signature | str | 短信签名| ""
sms_temp_code | str | 短信模板号| ""
serverchan_SCKEY | str | Server酱token| ""，放空则不发消息

*参见[阿里云python SDK快速指南](https://help.aliyun.com/document_detail/53090.html)和阿里云[OpenAPI Explorer](https://api.aliyun.com)

**阿里云控制台-accesskeys-开始使用子用户accesskey，填写RAM子账号，并添加权限，获得 ACCESS_KEY和ACCESS_SECRET

### 客户端部署

#### curl

_Windows 10下可用cmd执行该命令_

**通过curl，只能一次解析一个。**

`curl https://服务器地址/DDNS目录/index.py -X POST -d "token=解析口令&name=解析子域名"`

#### python requests

**批量解析**

将test_tool/post_test.py释放到任意目录，修改如下参数：

项目 | 属性 | 值
----|-----|----
token | str | 必填，动态解析口令，同服务器
namelist | str list | 必填，子域名列表 ，用英文引号包括，每个子域名用英文逗号隔开
domain_name | str | 指定解析域名，不加此参数则解析默认域名

1.  安装python3
2.  安装Requests: `pip install requests`
3.  修改token和namelist
4.  运行 `python post_test.py`


#### 定期任务

Windows: 任务计划管理器

Linux: cron

### 返回值定义与调试措施

返回值 | 定义 | 解决措施
-------|-------|-------
“401.0”: “HTTPS REQUEST SCHEME IS REQUIRED.” | 使用了不安全的http协议访问 | 改用https协议访问
"401.1": "POST REQUEST_METHOD IS REQUIRED." | 只允许POST | 只用POST，或者将const.request_method_limit改为False
“401.2”: “TOKEN ERROR” | 解析口令错误 | 修改解析口令，和服务端一致
"401.3": "INVALID DOMAIN" | 非允许自定义域名 | 修改为允许域名，或将此域名添加到域名列表
“503.1”: “CONNECTION ERROR” | 服务端网络错误 | 服务端网络修复，或稍后再试
“503.2”: “Failed to create new record.” | 新解析记录添加失败 | 检查子域名是否有非法字符，或稍后再试
“503.3”: “Failed to read full records.” | 域名解析查询失败，获取不到现在的解析情况 | 服务端网络修复，或稍后再试
“503.4”: “Failed to renew record.” | 更新解析记录失败 | 服务端网络修复，或稍后再试
“200.1 OK”: “records created” | 解析记录成功添加 | –
“200.2 OK”: “records unchanged” | 解析记录维持不变 | –
“200.3 OK”: “records modified.” | 解析记录成功修改 | –

### **工具集**

说明：该工具集为该服务的扩展，访问不需要通过https协议。根据获取的DDNS数据，用户可以定制其他工具。

#### 解析记录变更过程记录

`test_tool/update_count_show.py`

#### 解析记录更新情况记录（服务器心跳）

`test_tool/update_history_show.py`

