# -*- coding:utf8 -*-
# This script is aimed to ftp backup log scanning.
# created: 2018-12-21
'''
Changelog
v1.0 2018-12-21

v1.01 2018-12-22
1. latest backup date.

v1.02 2018-12-30
1. add full name
2. remove file formation of cmd exec [os.popen()]

v1.1 2018-12-31
1. multiprocessing version for get fullname
    main process: read log
    subprocess: get fullname
'''
# maintainer: Yao Yin Ying

import re
import os
import time
import traceback
from multiprocessing import Process,Queue

# long term maintaining list for members who have left this lab.
unavailable_member = [....]


# Check file name. this function returns False when a filename without surfix--.log is given.
def file_checker(file_name):
    if file_name.find(".log") != -1:
        return True
    else:
        return False


def logging(log_msg):
    global analysis_log_file
    with open(analysis_log_file, "a", encoding="utf-8") as log_write:
        log_write.write(log_msg + "\n")


def log_reading(log_file_name):
    users_this_day = {}
    with open(log_file_name, 'r', encoding='UTF-8') as read_log:
        for line in read_log:
            if line.split(" ").__len__() < 9:
                continue
            user_in_line = line.split(" ")[4]
            if user_in_line.split("\\").__len__() > 1:
                user = user_in_line.split("\\")[1]
                if user not in users_this_day:
                    users_this_day[user] = 1
                else:
                    users_this_day[user] = users_this_day[user] + 1
    return users_this_day


def yinlab_members_list():
    cmd = os.popen("net localgroup YinlabMembers")
    users_list_cmd = cmd.read().split("\n")
    yinlab_member_list = []
    for user in users_list_cmd[6:-3]:
        yinlab_member_list.append(user)
    for member in unavailable_member:
        yinlab_member_list.remove(member)
    return yinlab_member_list

def get_fullname_put(q, user_list):
    print('Run subprocess %s (%s)...' % ("get fullname Put_Query", os.getpid()))
    print(user_list)
    def get_each_fullname(user):

        read = os.popen("net user %s" % user)
        user_info = (read.read()).split("\n")
        try:
            fullname = user_info[1].split(" ")[-1]
            return fullname
        except Exception as e:
            logging(str(traceback.print_exc()))
            return "0"
        pass

    fullname_dict ={}
    for user in user_list:
        fullname_dict[user] = get_each_fullname(user)
        # print("Fullname = %s \t user = %s" % (fullname_dict[user],user))
    q.put(fullname_dict)
    print('End subprocess %s (%s)...' % ("get fullname Put_Query", os.getpid()))


    pass


if __name__ == "__main__":

    try:


        print('Main process (%s) start ...' % os.getpid())
        cutoff = int(input("Cutoff for file counting: "))
        unbackup_members = yinlab_members_list()
        backup_members = {}
        fullname_dict = {}
        working_dir = "F:/ftplog/FTPSVC1"
        result_dir = working_dir + "/result"
        if not os.path.exists(result_dir):
            os.makedirs(result_dir)
        analysis_log_file = result_dir + "/User_analysis_" + time.strftime("%Y_%m_%d_%H_%M_%S",
                                                                           time.localtime(int(time.time()))) + ".log"
        print("Initializing ... ")
        logging("Initializing ... ")
        logging("Cutoff = %s" % cutoff)
        logging("unavailable member:\n%s" % unavailable_member)

        # existed log will be read
        selected_log = os.listdir(working_dir)
        logging("Selected logs: \n%s" % selected_log)
        c =0

        q=Queue()
        fullname_put_proc =Process(target=get_fullname_put, args=(q, unbackup_members,))
        #fullname_get_proc =Process(target = get_fullname_get,args=(q,))
        fullname_put_proc.start()


        for log_file in selected_log:
            # test data limit by c for counting
            '''
            c+=1
            if c ==30 :
                break
                '''
            if file_checker(log_file):
                print("Processing %s ... " % log_file)
                log_date = "20" + re.findall(r'u_ex(\d{6}).log', log_file)[0]
                log_date_formatted = '-'.join([log_date[:4], log_date[4:6], log_date[-2:]])
                logging("=========================================")
                logging(log_date_formatted)
                logging("=========================================")
                users_this_day = log_reading('/'.join([working_dir, log_file]))
                logging("Member\t\t\t\t\tCount")
                logging("-----------------------------------------")
                for user in users_this_day:
                    logging("%s%s%s" % (
                        user, "\t" * int(6 - len(bytes(user, encoding=('gbk'))) // 4), users_this_day[user]))
                    if user in unbackup_members and users_this_day[user] > cutoff:
                        unbackup_members.remove(user)
                    if users_this_day[user] > cutoff:
                        backup_members[user] = log_date_formatted
                logging("=========================================")
                logging("Finish Reading logfile: %s\n" % log_file)

        fullname_put_proc.join()
        fullname_dict = q.get(block=True)
        print(fullname_dict)

        logging("=========================================\n")
        logging("Finish Analyzing.\n")

        logging("======================================================")
        logging("Here's member list with data backup.")
        logging("------------------------------------------------------")
        logging("User\t\t\t\t\tFullName\tLatest Update")
        logging("======================================================")
        for user in backup_members:
            #fullname_dict[user] = get_each_fullname(user)
            logging("%s%s%s%s%s" % (user, "\t" * int(6 - len(bytes(user, encoding=('gbk'))) // 4), fullname_dict[user],
                                    "\t" * int(3 - len(bytes(fullname_dict[user], encoding=('gbk'))) // 4),
                                    backup_members[user]))
        logging("======================================================\n\n")

        logging("=========================================")
        logging("Here're members without data backup.")
        logging("=========================================")
        for user in unbackup_members:
            logging("%s%s%s" % (
                user, "\t" * int(6 - len(bytes(user, encoding=('gbk'))) // 4), fullname_dict[user]))
        logging("=========================================\n")

        logging("End of analysis report.")
        print("End of analysis report.")
    except Exception as e:
        logging(str(e))
        print(traceback.print_exc())
        logging(str(traceback.print_exc()))
        print("An error is detected, please see the report for details.\n%s" % analysis_log_file)
        pass
