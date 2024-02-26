import os

import psycopg2
import time
from dotenv import load_dotenv

load_dotenv('config.env', override=True)
path = os.getenv("PATH", "")
db = os.getenv("database", "")
host_url = os.getenv("host", "")
user_ = os.getenv("user", "")
pass_ = os.getenv("password", "")
port = os.getenv("port", "")

conn = psycopg2.connect(database=db,
    host=host_url,
    user = user_,
    password=pass_,
    port=port
)

con=conn.cursor()
#  For Creating Tables for files and file_types
# con.execute("""
    # Create table files(
    #         ID int Primary Key,
    #         file_name varchar(100),
    #         file_type varchar(10));""")

# # Creating table for update trigger
# con.execute("""
# Create table Update_files_in_db(
#       id  serial,
#       file_count int
# );
# """)

def checking_files():
    list_files = os.listdir(path)
    print(list_files)
    return list_files

def get_file_count_from_db(con,conn):
    con.execute("select * from Update_files_in_db")
    f = con.fetchall()
    return f

def get_files_from_db(con,conn):
    con.execute("select * from files")
    f = con.fetchall()
    return f

def update_file_to_db(con,conn,count):
    con.execute(f"update Update_files_in_db set file_count ={count} where id = 1")
    conn.commit()
    con.execute("select * from Update_files_in_db")
    print(con.fetchall())

def updating_file_name(con,conn,l,no):
    for i in l:
        v=i.split(".")
        con.execute(f"insert into files(file_name,file_type) values ('{v[0]}','{v[1]}')")
        conn.commit()
    update_file_to_db(con,conn,no)
while True:
    list_files = checking_files()
    no_of_files = len(list_files)
    count_from_db = get_file_count_from_db(con,conn)
    print(list_files,no_of_files,count_from_db[0][1])
    if count_from_db[0][1]< no_of_files:
        new_list_to_update=[]
        list_files_from_db = get_files_from_db(con,conn)
        print(list_files_from_db)
        new_l=[]
        for i in list_files_from_db:
            i=list(i)
            i.pop(0)
            i=".".join(i)
            new_l.append(i)
        for i in list_files:
            if i not in new_l:
                print(i,new_l)
                new_list_to_update.append(i)
        updating_file_name(con,conn,new_list_to_update,no_of_files)

    time.sleep(30)
