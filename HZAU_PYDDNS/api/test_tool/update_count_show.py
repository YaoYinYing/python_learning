#!python
import sqlite3
import time,datetime
import traceback
import cgi


def ddns_count_show():
    conn = sqlite3.connect("sqlite file")
    c = conn.cursor()
    sql = '''SELECT * FROM DDNS_UPDATE_COUNT;''' 
    
    try:
        data=c.execute(sql)
        for item in data:
            date_latest_check = time.mktime(time.strptime(time.strftime(item[-1].split(" ")[0]),"%Y-%m-%d"))
            date_now = time.mktime(time.strptime(time.strftime(str(datetime.datetime.now()).split(" ")[0]),"%Y-%m-%d")) 

            if int(date_now)-int(date_latest_check) < 86400:
                print(item)
                print("</br>")


    except Exception as e:
        traceback.print_exc()
    finally:
        conn.close()

    pass

print("content-type:text/html")
print("")
print("<meta http-equiv = 'refresh' content = 30 />")
ddns_count_show()
