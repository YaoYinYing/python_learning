#!python

import datetime
import re


def ip_from_blacklist():
    with open("./conf/blacklist.conf", 'r') as blacklist:
        file = blacklist.read()
        return re.findall(r'[^ ]Deny from (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', file)


def error_event_logged():
    with open("./logs/error.log", 'r') as error_log:
        file = error_log.read()
        # print(file)
        return re.findall(
            r"\[client (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):\d+] script '([\d\S]+)' not found or unable to stat",
            file) + \
               re.findall(
                   r"\[client (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):\d+] AH02811: script not found or unable to stat: ([\d\S]+)",
                   file)


def ip_error_count(error_event_list):
    ip_count_logged = {}
    for item in error_event_list:
        if item[0] not in ip_count_logged:
            ip_count_logged[item[0]] = 1
        else:
            ip_count_logged[item[0]] += 1
    return ip_count_logged
    pass


def black_list_append(ip_from_blacklist, ip_from_error_event, error_event_logged):
    ip_blacklist_append = []
    for ip in ip_from_error_event:
        if (ip not in ip_from_blacklist) and (ip_from_error_event[ip] >= 6):
            ip_blacklist_append.append(ip)
            with open("./conf/blacklist.conf", 'a') as blacklist:
                blacklist.write(
                    "\n\n# Auto added at %s, %s counts" % (str(datetime.datetime.now()), ip_from_error_event[ip]))
                g = [x[1] for x in error_event_logged if x[0] == ip]
                blacklist.write("\n# latest detect: %s" % g[-1])
                blacklist.write("\nDeny from %s" % ip)


def clear_error_log():
    with open("./logs/error.log", 'w') as error_log:
        error_log.write("")

ip_from_blacklist_start = ip_from_blacklist()

black_list_append(ip_from_blacklist=ip_from_blacklist(),
                  ip_from_error_event=ip_error_count(error_event_logged()),
                  error_event_logged=error_event_logged())

ip_from_blacklist_updated = ip_from_blacklist()

if ip_from_blacklist_start.__len__() != ip_from_blacklist_updated.__len__():
    clear_error_log()
