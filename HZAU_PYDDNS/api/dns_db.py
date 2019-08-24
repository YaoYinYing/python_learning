import sqlite3
import traceback

def create_table():
    conn = sqlite3.connect("db_file_name")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS DDNS_CHANGE_RECORD
    (REQUEST_ID TEXT PRIMARY KEY NOT NULL,
    DOMAIN TEXT NOT NULL,
    NAME TEXT NOT NULL,
    RECORD_ID TEXT NOT NULL,
    IP_ADDR CHAR(50) NOT NULL,
    TIME_STAMP TIMESTAMP NOT NULL DEFAULT (DATETIME('now','localtime')));''')

    conn.commit()
    conn.close()

    pass


def insert_change(request_id, domain, name, record_id, ip_addr):
    conn = sqlite3.connect("db_file_name")
    c = conn.cursor()
    sql = '''INSERT INTO DDNS_CHANGE_RECORD(REQUEST_ID,DOMAIN,NAME,RECORD_ID,IP_ADDR ) VALUES  ('%s','%s','%s','%s','%s');''' % ( request_id, domain, name, record_id, ip_addr)
    try:
        c.execute(sql)
        conn.commit()
    except Exception as e:
        traceback.print_exc()
    finally:
        conn.close()
    pass

def check_data():
    conn = sqlite3.connect("db_file_name")
    c = conn.cursor()
    sql = '''SELECT * FROM DDNS_CHANGE_RECORD'''
    data = c.execute(sql)
    for row in data:
        print(row)
    conn.commit()
    conn.close()


def ddns_count_table_create():
    conn = sqlite3.connect("db_file_name")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS DDNS_UPDATE_COUNT
    (RECORD_ID TEXT PRIMARY KEY NOT NULL,
    DOMAIN TEXT NOT NULL,
    NAME TEXT NOT NULL,
    UPDATE_COUNT INT NULL,
    TIME_STAMP TIMESTAMP NOT NULL DEFAULT (DATETIME('now','localtime')));''')

    conn.commit()
    conn.close()

    pass


def ddns_count_item_insert(domain, name, record_id):
    conn = sqlite3.connect("db_file_name")
    c = conn.cursor()
    sql = '''REPLACE INTO DDNS_UPDATE_COUNT(RECORD_ID,DOMAIN,NAME,UPDATE_COUNT ) VALUES ('%s','%s','%s',IFNULL((SELECT UPDATE_COUNT FROM DDNS_UPDATE_COUNT WHERE RECORD_ID='%s' ),0)+1);''' % (record_id, domain, name, record_id)
    try:
        c.execute(sql)
        conn.commit()

    except Exception as e:
        traceback.print_exc()
    finally:
        conn.close()


def exist_and_count(domain, name, record_id):
    try:
        create_table()
        ddns_count_table_create()
        ddns_count_item_insert(domain, name, record_id)
    except Exception as e:
        traceback.print_exc()



#exist_and_count("yinlab.cn", "guanzeyuan",'17271456555469824')
