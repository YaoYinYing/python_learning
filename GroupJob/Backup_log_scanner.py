# -*- coding:utf8 -*-
# This script is aimed to ftp backup log scanning.
# created: 2018-12-21
# maintainer: Yao Yin Ying

import re
import os
import time
import traceback

# long term maintaining list for members who have left this lab.
unavailable_member =["..."]

# Check file name. this function returns False when a filename without surfix--.log is given.
def file_checker(file_name):
    if file_name.find(".log") != -1:
        return True
        pass
    else:
        return False
        pass
    pass


def logging(log_msg):
    global analysis_log_file
    with open(analysis_log_file, "a") as log_write:
        log_write.write(log_msg + "\n")
    pass


def log_reading(log_file_name):
    users_this_day = {}
    with open(log_file_name, 'r', encoding='UTF-8') as read_log:
        for line in read_log:
            # print(line)
            if line.split(" ").__len__() < 9:
                continue
            # print(line.split(" "))
            user_in_line = line.split(" ")[4]
            # print(user_in_line)
            if user_in_line.split("\\").__len__() > 1:
                user = user_in_line.split("\\")[1]
                # print(user)
                if user not in users_this_day:
                    users_this_day[user] = 1
                else:
                    users_this_day[user] = users_this_day[user] + 1
                pass
            pass
    return users_this_day


def yinlab_members_list():
    out_dir = "F:/ftplog"
    os.system("net localgroup YinlabMembers >userlist")
    with open('/'.join([out_dir, "userlist"]), 'r', encoding='gbk') as user_list_read:
        users_list_cmd = user_list_read.readlines()
        pass

    os.system("del /q userlist")
    #print(users_list_cmd[6:-2])
    yinlab_member_list = []
    for user in users_list_cmd[6:-2]:
        yinlab_member_list.append(user.rstrip("\n"))
    # print(yinlab_member_list)
    for member in yinlab_member_list:
        if member in unavailable_member:
            yinlab_member_list.remove(member)
    return yinlab_member_list


if __name__ == "__main__":
    print("hoellw")
    try:
        unbackup_members = yinlab_members_list()
        backup_members = []

        working_dir = "F:/ftplog/FTPSVC1"
        result_dir = working_dir + "/result"

        if not os.path.exists(result_dir):
            os.makedirs(result_dir)
            pass
        analysis_log_file = result_dir + "/User_analysis_" + time.strftime("%Y_%m_%d_%H_%M_%S",
                                                                           time.localtime(int(time.time()))) + ".log"
        logging("Initializing ... ")

        # existed log will be read
        selected_log = os.listdir(working_dir)
        logging("Selected logs: \n%s" % selected_log)

        for log_file in selected_log:
            if file_checker(log_file):
                print("Processing %s ... " %log_file)
                log_date = "20" + re.findall(r'u_ex(\d{6}).log', log_file)[0]

                log_date_formatted = '-'.join([log_date[:4], log_date[4:6], log_date[-2:]])
                logging("=========================================")
                logging("%s log" % log_date_formatted)
                logging("Reading logfile: %s" % log_file)
                logging("=========================================")
                users_this_day = log_reading('/'.join([working_dir, log_file]))
                logging("Member\t\tCount")
                for user in users_this_day:
                    logging("%s\t\t%s" % (user, users_this_day[user]))
                    if user in unbackup_members:
                        unbackup_members.remove(user)
                    if user not in backup_members:
                        backup_members.append(user)
                pass

                logging("=========================================")
                logging("Finishing Reading logfile: %s\n" % log_file)


        logging("=========================================\n")
        logging("Finishing Analyzing.\n")
        logging("=========================================")
        logging("Here's member list with data backup.")
        logging("=========================================")
        for user in backup_members:
            logging("%s\t" % (user))
        logging("=========================================\n\n")

        logging("=========================================")
        logging("Here're members need data backup.")
        logging("=========================================")
        for user in unbackup_members:
            logging("%s\t" % (user))
        logging("=========================================\n")

        logging("End of analysis report.")
        print("End of analysis report.")
    except Exception as e:
        print(traceback.print_exc())
        logging(traceback.print_exc())
        print("An error detected, please see the report for details.\n%s" % analysis_log_file)
        pass
