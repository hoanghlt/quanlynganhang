import mysql.connector
from mysql.connector import Error


def create_db_connection():
    with open("config.txt", "r") as f:
        user = f.readline().rstrip()
        password = f.readline().rstrip()

    try:
        mydb = mysql.connector.connect(host='localhost',
                                       database='quanlynganhang',
                                       user=user,
                                       password=password)
        if mydb.is_connected():
            db_Info = mydb.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = mydb.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            return mydb

    except Error as e:
        print("Error while connecting to MySQL", e)


def close_db_connection(connection):
    if connection:
        connection.close()
        print("MySQL connection closed")

# Chạy ví dụ:
# db_connection = create_db_connection()
# if db_connection:
#     # Thực hiện các thao tác cơ sở dữ liệu ở đây
#     # ...
#     close_db_connection(db_connection)
