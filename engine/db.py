#import csv
#import sqlite3

#conn = sqlite3.connect("jarvis.db")
#cursor = conn.cursor()
#import sqlite3

#conn = sqlite3.connect("jarvis.db")
#cursor = conn.cursor()

# Update all numbers by adding +92 in front if not already present
#cursor.execute("""
    #UPDATE contacts
    #SET mobile_no = '+92' || mobile_no
    #WHERE mobile_no NOT LIKE '+%';""")

#conn.commit()
#conn.close()

#print("✅ All numbers updated successfully!")


# Read selected columns from CSV
#desired_columns_indices = [0, 18]

#with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
    #csvreader = csv.reader(csvfile)
   # for row in csvreader:
        #selected_data = [row[i] for i in desired_columns_indices]
      #  cursor.execute('''INSERT INTO contacts (id, name, mobile_no) VALUES (null, ?, ?);''', tuple(selected_data))

# Add one more manual record (✅ before closing)
#cursor.execute("INSERT INTO contacts VALUES (null,'eman', '3203813938', 'null', 'lahore')")

# Commit and close
#conn.commit()
#conn.close()
#query = 'ahmad'
#query = query.strip().lower()

#cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
#results = cursor.fetchall()
#print(results[0][0])

# testing module
# app_name = "android studio"
# cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
# results = cursor.fetchall()
# print(results[0][0])

# Create a table with the desired columns
# cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL, address VARCHAR(255) NULL)''')


# Specify the column indices you want to import (0-based index)
# Example: Importing the 1st and 3rd columns
# desired_columns_indices = [0, 30]

# Adding personal info table
#query = "CREATE TABLE IF NOT EXISTS info(name VARCHAR(100), designation VARCHAR(50),mobileno VARCHAR(40), email VARCHAR(200), city VARCHAR(300))"
#cursor.execute(query)

# Add Column in contacts table
# cursor.execute("ALTER TABLE contacts ADD COLUMN address VARCHAR(255)")

import csv
import sqlite3

# -------------------------
# CONNECT TO DATABASE ONCE
# -------------------------
conn = sqlite3.connect("jarvis.db")
cursor = conn.cursor()

# -------------------------
# UPDATE NUMBER FORMAT
# -------------------------
cursor.execute("""
    UPDATE contacts
    SET mobile_no = '+92' || mobile_no
    WHERE mobile_no NOT LIKE '+%';
""")
print("✅ All numbers updated successfully!")

# -------------------------
# CREATE INFO TABLE
# -------------------------
cursor.execute("""
    CREATE TABLE IF NOT EXISTS info(
        name VARCHAR(100),
        designation VARCHAR(50),
        mobileno VARCHAR(40),
        email VARCHAR(200),
        city VARCHAR(300)
    )
""")

# -------------------------
# YOU CAN ADD MORE QUERIES HERE SAFELY
# -------------------------

# Example: Adding new record manually
# cursor.execute("INSERT INTO contacts VALUES (null,'eman', '3203813938', 'null', 'lahore')")

# Example: Searching contact
# query = "ahmad"
# query = query.strip().lower()
# cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
# results = cursor.fetchall()
# print(results)

# -------------------------
# FINALLY CLOSE DATABASE
# -------------------------
conn.commit()
conn.close()









# ==============================
# JARVIS PERMANENT CHAT HISTORY
# ==============================

# import os
# import sqlite3

# BASE_DIR = os.path.dirname(
#     os.path.dirname(os.path.abspath(__file__))
# )

# DB_PATH = os.path.join(BASE_DIR, "jarvis.db")


# def create_chat_history_table():
#     conn = sqlite3.connect(DB_PATH)

#     cursor = conn.cursor()

#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS chat_history (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             conversation_id TEXT NOT NULL,
#             role TEXT NOT NULL,
#             message TEXT NOT NULL,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#         )
#     """)

#     conn.commit()
#     conn.close()


# def save_chat_message(conversation_id, role, message):
#     conn = sqlite3.connect(DB_PATH)

#     cursor = conn.cursor()

#     cursor.execute("""
#         INSERT INTO chat_history (
#             conversation_id,
#             role,
#             message
#         )
#         VALUES (?, ?, ?)
#     """, (conversation_id, role, message))

#     conn.commit()
#     conn.close()


# def get_chat_history(conversation_id):
#     conn = sqlite3.connect(DB_PATH)

#     cursor = conn.cursor()

#     cursor.execute("""
#         SELECT role, message, created_at
#         FROM chat_history
#         WHERE conversation_id = ?
#         ORDER BY id ASC
#     """, (conversation_id,))

#     messages = cursor.fetchall()

#     conn.close()

#     return messages

