import psycopg2
import os
from dotenv import load_dotenv

load_dotenv('config.env', override=True)

db = os.getenv("database", "")
host_url = os.getenv("host", "")
user_ = os.getenv("user", "")
pass_ = os.getenv("password", "")
port = os.getenv("port", "")


def db_connection():
    conn = psycopg2.connect(database=db,
        host=host_url,
        user = user_,
        password=pass_,
        port=port
    )
    
    con=conn.cursor()
    return con,conn

def creating_tables(con,conn) -> None:
    con.execute("""
        create table files_details(
           	id int PRIMARY KEY,
           	name varchar(30),
           	Type varchar(30),
           	size bigint,
           	create_time timestamp,
           	modified_time timestamp,
           	Path varchar(100)
        );""")
    con.execute("""
        create table files_count(
            id int Primary Key,
            count int
        );""")
    conn.commit()
    
    
def getting_count(con,conn):
    con.execute("select * from files_count where id = 1")
    return con.fetchall()

def update_files_count(con,conn,k) -> None:
    con.execute(f"update files_count set count = {k} where id = 1")
    conn.commit()
    