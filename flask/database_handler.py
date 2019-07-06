import mysql.connector
import datetime
import json
import time

try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="weatherstation"
    )
    mycursor = mydb.cursor()
except:
    print("Failed to connect to MySQL")


def insert_temperature(value):
    now = datetime.datetime.now()
    date = now.strftime('%Y-%m-%d %H:%M:%S')
    temp = int(value)
    try:
        mycursor.execute("""
        INSERT INTO temperature (value, date) VALUES (%d,'%s')
        """ % (temp, date))
        mydb.commit()
        print(mycursor.rowcount, "record inserted into Temperature")
    except:
        print("Failed to insert into Temperature")
        mydb.rollback()


def insert_humidity(value):
    now = datetime.datetime.now()
    date = now.strftime('%Y-%m-%d %H:%M:%S')
    temp = int(value)
    try:
        mycursor.execute("""
        INSERT INTO humidity (value, date) VALUES (%d,'%s')
        """ % (temp, date))
        mydb.commit()
        print(mycursor.rowcount, "record inserted into Humidity")
    except:
        print("Failed to insert into Humidity")
        mydb.rollback()


def read_temperature():
    mycursor.execute("SELECT * FROM temperature ORDER BY id DESC")
    #myresult = mycursor.fetchall()
    myresult = mycursor.fetchmany(size=10)
    mycursor.reset()
    myresult.reverse()

    results = []
    temp = {}
    for x in myresult:
        temp['id'] = x[0]
        temp['value'] = x[1]
        temp['date'] = str(x[2])
        results.append(temp)
        temp = {}

    return json.dumps(results)


def read_humidity():
    mycursor.execute("SELECT * FROM humidity ORDER BY id DESC")
    #myresult = mycursor.fetchall()
    myresult = mycursor.fetchmany(size=10)
    mycursor.reset()
    myresult.reverse()

    results = []
    humid = {}
    for x in myresult:
        humid['id'] = x[0]
        humid['value'] = x[1]
        humid['date'] = str(x[2])
        results.append(humid)
        humid = {}
    return json.dumps(results)


def close():
    mycursor.close()
    mydb.close()
