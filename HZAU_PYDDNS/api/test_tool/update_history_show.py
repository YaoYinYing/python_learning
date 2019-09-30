#!python
import sqlite3
import time,datetime
import traceback
import cgi

hide_column = 0

def check_data():
    conn = sqlite3.connect("sqlite file")
    c = conn.cursor()
    sql = '''SELECT * FROM DDNS_CHANGE_RECORD'''
    print("<html><table border='2' cellspacing='0'> ")
    print("<thead><tr>")
    for x in ["Request id","Domain name", "Sub domain name", "Record id","ip", "Update time"][hide_column:]:
        print("<th>%s</th>" % x )
    print("</tr></thead>")
    print("<tbody>")
    try:
        data=c.execute(sql)
        for item in data:
            date_latest_check = time.mktime(time.strptime(time.strftime(item[-1].split(" ")[0]),"%Y-%m-%d"))
            date_now = time.mktime(time.strptime(time.strftime(str(datetime.datetime.now()).split(" ")[0]),"%Y-%m-%d")) 

            if item[4] != "127.0.0.1":
                print("<tr>")
                for x in item[hide_column:]:
                    print("<td>%s</td>" %x )
                print("</tr>")
        

    except Exception as e:
        traceback.print_exc()
    finally:
        conn.close()

    pass
    print("</tbody></table></html>")
print("content-type:text/html")
print("")
print("<meta http-equiv = 'refresh' content = 30 />")
check_data()
