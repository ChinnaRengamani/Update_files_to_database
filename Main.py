
import os
import stat
from database import db_connection,creating_tables, getting_count, update_files_count
from datetime import datetime
import psycopg2
from dotenv import load_dotenv
from time import sleep

def convert_unix_time_to_date(unix_time: float):
    return datetime.fromtimestamp(
            int(unix_time)
        ).strftime('%Y-%m-%d %H:%M:%S')

def directory_to_files(path: str):
    f=list()
    for i in os.scandir(path):
        if i.is_dir():
            
            f.extend(directory_to_files(i.path))
        else:
            f.append([i.name,i.stat().st_size,convert_unix_time_to_date(i.stat().st_birthtime),convert_unix_time_to_date(i.stat().st_mtime),i.path])
        
    return f

def update_files_to_db(con: psycopg2.extensions.cursor , conn: psycopg2.extensions.connection , files: list):
    k=1
    con.execute("truncate files_details")
    for i in files:
        c=f"""insert into files_details(id,name,Type,size,create_time,modified_time,Path) values({k},'{i[0]}','{i[0].split(".")[-1]}',{i[1]},timestamp '{i[2]}',timestamp '{i[3]}','{i[4]}')"""
        print(c)
        con.execute(c)
        conn.commit
        k+=1
    return k-1

def main():
    load_dotenv('config.env', override=True)
    path: str = os.getenv("PATH","")
    
    files: list[str | list] = list()
    
    for i in os.scandir(path):
        if i.is_dir():
            files.extend(directory_to_files(path = i.path))
        else:
            files.append([i.name,i.stat().st_size,convert_unix_time_to_date(i.stat().st_birthtime),convert_unix_time_to_date(i.stat().st_mtime),i.path])

    con,conn = db_connection()
    
    # creating_tables(con,conn)  # for creating Table
    
    count_from_db = getting_count(con,conn)[0][1]
    
    if count_from_db < len(files): 
        k = update_files_to_db(con,conn,files)
        update_files_count(con,conn,k)
    print('\nsleeping for 60 Seconds')
    sleep(60)
    return main()

if __name__ == '__main__':
    main()