import sqlite3

connection = sqlite3.connect("bloodbank.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT,
    age INTEGER,
    gender TEXT,
    blood_group TEXT,
    mobile TEXT,
    email TEXT,
    address TEXT,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS donors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    donor_name TEXT,
    age INTEGER,
    gender TEXT,
    blood_group TEXT,
    mobile TEXT,
    city TEXT,
    location TEXT,
    last_donation TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS hospitals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hospital_name TEXT,
    mobile TEXT,
    city TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS emergency_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_name TEXT,
    blood_group TEXT,
    hospital_name TEXT,
    mobile TEXT
)
""")

connection.commit()

cursor.close()
connection.close()

print("Database created successfully.")