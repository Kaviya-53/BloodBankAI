import sqlite3

def get_connection():
    connection = sqlite3.connect(
        "bloodbank.db",
        check_same_thread=False
    )

    connection.row_factory = sqlite3.Row

    return connection