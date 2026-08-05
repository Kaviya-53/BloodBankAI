import pymysql

def get_connection():
    connection = pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="#Kaviya@2007",   # Replace with your MySQL root password
        database="bloodbank",
        port=3306,
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection