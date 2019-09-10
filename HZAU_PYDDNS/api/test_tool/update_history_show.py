#!python
import sqlite3

def check_data():
    conn = sqlite3.connect("sqlite file")
    c = conn.cursor()
    sql = '''SELECT * FROM DDNS_CHANGE_RECORD'''
    data = c.execute(sql)
    for row in data:
        print(row)
        print("</br>")
    conn.close()

print("content-type:text/html")
print("")
print("<meta http-equiv = 'refresh' content = 30 />")
check_data()
