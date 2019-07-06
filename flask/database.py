import sys
import mysql.connector


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE weatherstation")


mycursor.close()
mydb.close()

# Setup Tables

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="weatherstation"
)

mycursor = mydb.cursor()

mycursor.execute(
    "CREATE TABLE temperature (id INT AUTO_INCREMENT PRIMARY KEY, value INT, date DATETIME)")
mycursor.execute(
    "CREATE TABLE humidity (id INT AUTO_INCREMENT PRIMARY KEY, value INT, date DATETIME)")

mycursor.close()
mydb.close()
