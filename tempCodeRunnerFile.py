import mysql.connector

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_MYSQL_PASSWORD",
        database="learning_progress"
    )

    if connection.is_connected():
        print("Successfully connected to MySQL!")
        print("Database: learning_progress")

    connection.close()

except mysql.connector.Error as error:
    print("Connection failed:", error)