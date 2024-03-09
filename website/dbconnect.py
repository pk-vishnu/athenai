import mysql.connector

db_config = {
    "user": "root",
    "password": "root",
    "host": "localhost",
    "database": "athenai",
}

def connect_to_database():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as e:
        print("Error connecting to MySQL database:", e)
        return None