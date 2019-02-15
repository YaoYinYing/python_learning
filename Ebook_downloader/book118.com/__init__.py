'''
Training project of python programming
Project: Ebook downloader for book118.com
Author: Yao Yin Ying
Date: 2019-02-15

Features:
1. Resume from breakpoint

'''

import const as const
import urllib.request
import requests
import re
import traceback
import json
import os
import time


def doc_title_fetch(url):
    cid = doc_cid(url)
    header = const.headers
    header['Referer'] = header['Referer'] % cid
    r = requests.get(url, headers=header, allow_redirects=False)
    # print(r.content.decode())
    return re.findall(r'<title>(.*)</title>', r.content.decode())[0]
    pass


def doc_cid(url):
    return str(re.findall(r'max.book118.com/html/\d+/\d+/(\d+).shtm', url)[0])


def doc_info(url):
    try:
        cid = doc_cid(url)
        # print(cid)
        # print(type(cid))
        header = const.headers
        # print(header)

        r = requests.get("https://max.book118.com/index.php?g=Home&m=View&a=viewUrl&cid=%s&flag=1" % cid,
                         headers=header)
        read_page_url = r.content.decode()
        # print(read_page_url)

        # fetching url parameters
        read_page_url_para = read_page_url.split("?")[-1].split("&")
        read_page_url_para_dict = {}
        for item in read_page_url_para:
            read_page_url_para_dict[item.split("=")[0]] = "=".join(item.split("=")[1:])
            pass

        r_read = requests.get("https:%s" % read_page_url)
        file_str = re.findall(r'<input type="hidden" id="Url" value="([A-Za-z0-9@_]+=*)"', r_read.content.decode())[0]
        read_limit = \
        re.findall(r'<input type="hidden" id="ReadLimit" value="(.*)" autocomplete="off" />', r_read.content.decode())[
            0]
        view_host = re.findall(r'//(.*\.book118\.com)', read_page_url)[0]
        print(file_str)
        read_page_url_para_dict["f"] = file_str
        # print(read_page_url_para_dict)
        print(read_limit)
        return read_page_url_para_dict, read_limit, view_host
        pass

    except Exception as e:
        traceback.print_exc()

        pass

    pass


def all_page_url(doc_info: dict, read_limit, view_host, page_flag, ):
    global doc_page_info, r_page_info, next_page_url, all_page_url_dict, doc_url_view, page_count, url_var, header
    if page_flag == 0:
        cid = doc_cid(url)
        header = const.headers
        header['Host'] = view_host
        all_page_url_dict = {}

        doc_url_view = "https://%s/PW/GetPage?isMobile=false" % view_host
        doc_page_img_url = ""
        next_page_url = "https://" + view_host + "/img?img=%s&tp="

        # fetch doc page info
        url_var = ""
        doc_info.pop("readpage")
        for item in doc_info:
            url_var += ("&" + item + "=" + str(doc_info[item]))
            # print(item)
            pass
        r_page_info_url = doc_url_view + url_var + "&readLimit=" + read_limit + "&img="
        # print(url_var)
        r_page_info = requests.get(r_page_info_url, headers=header)
        # print(r_page_info_url)
        # print(r_page_info.content.decode())
        doc_page_info = json.loads(r_page_info.content.decode())
        page_count = doc_page_info['PageCount']
    else:

        pass

    try:

        for page in range(page_flag, page_count):
            page_img_url = next_page_url % doc_page_info["NextPage"]
            print(
                "Fetching page %s / %s(%s Percent)" % (doc_page_info["PageIndex"], page_count, page / page_count * 100))
            all_page_url_dict[page] = doc_page_info["NextPage"]
            urllib.request.urlretrieve(page_img_url, doc_dir + "/" + str(page) + ".jpg")
            next_page_view_url = doc_url_view + url_var + "&readLimit=" + read_limit + "&img=" + doc_page_info[
                "NextPage"]
            # die here mostly in bad network connection
            r_page_info = requests.get(next_page_view_url, headers=header,timeout=0.5)
            # print(next_page_view_url)
            page_flag += 1
            # print(r_page_info.content.decode())
            doc_page_info = json.loads(r_page_info.content.decode())
            time.sleep(0.1)
            pass

        pass

    except Exception as e:
        # traceback.print_exc()
        print("Connection Timeout. Resume from breakpoint...")
        # resume from break point
        all_page_url(doc_info_dict, read_limit, view_host, page_flag)
        pass
    pass


working_dir = "./results"

page_flag = 0

url = "https://max.book118.com/html/2017/0703/120036825.shtm"

doc_title = doc_title_fetch(url)
doc_dir = "/".join([working_dir, doc_title])
if not os.path.exists(doc_dir):
    os.makedirs(doc_dir)

doc_info_dict, read_limit, view_host = doc_info(url)
print(doc_info_dict)
all_page_url(doc_info_dict, read_limit, view_host, page_flag)
