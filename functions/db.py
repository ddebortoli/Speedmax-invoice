from getpass import getuser
from flaskext.mysql import MySQL
from flask import Flask
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()

import os
app = Flask(__name__)
mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = os.getenv('MYSQL_DB')
app.config['MYSQL_DATABASE_HOST'] = os.getenv('MYSQL_HOST')

mysql.init_app(app)

def getGeneralData():
    conn = mysql.connect()
    cur =conn.cursor()
    cur.execute('CALL `getDataFromClient`(0);')
    data = cur.fetchall()
    cur.execute('CALL `getLocations`();')
    locationsData = cur.fetchall()
    cur.execute('CALL `getPackages`();')
    packagesData = cur.fetchall()
    cur.execute('CALL `getPaymentMethods`();')
    paymentMethods = cur.fetchall()
    cur.close()
    return data,locationsData,packagesData,paymentMethods

def getGeneralDataForUpdate(id):
    conn = mysql.connect()
    cur =conn.cursor()
    cur.execute('CALL `getPersonalData`({0});'.format(id))
    data = cur.fetchall()
    cur.execute('CALL `getLocations`();')
    locationsData = cur.fetchall()
    cur.execute('CALL `getPackages`();')
    packagesData = cur.fetchall()
    cur.execute('CALL `getPaymentMethods`();')
    paymentMethods = cur.fetchall()
    print(data)
    cur.close()
    return data,locationsData,packagesData,paymentMethods

def updateUserData(fullname,phone,email,adress,location,package,payment,id):
    conn = mysql.connect()
    cur =conn.cursor()
    cur.execute("""
            UPDATE datos_cliente SET `fullname`=%s,`phone`=%s,`email`=%s,`adress`=%s,
            `location`=%s,`packageId`=%s,`paymentMethodId`=%s WHERE Id = %s
        """, (fullname, phone, email,adress,location,package,payment, id))
    conn.commit()
    cur.close()

def getClientIdFromAdress(adress):
    conn = mysql.connect()
    cur =conn.cursor()
    cur.execute("CALL `getIdFromClient`('{}');".format(adress))
    currentId = cur.fetchone()
    cur.close()
    if currentId != None:
        return currentId[0]
    return None

def addClient(fullname,phone,email,adress,location,package,payment):
    conn = mysql.connect()
    cur =conn.cursor()
    cur.execute("""INSERT INTO datos_cliente 
                (fullname,phone,email,adress,location,packageId,paymentMethodId)
                VALUES(%s,%s,%s,%s,%s,%s,%s)""",(fullname,phone,email,adress,location,package,payment))
    conn.commit()
    userId = getClientIdFromAdress(adress)
    if userId:
            currentTime = datetime.now().strftime("%Y-%m-%d")
            cur.execute('INSERT INTO invoicestatus (`ID`, `creationDate`, `latePayment`, `lastPayment`, `isOnline`)VALUES(%s,%s,%s,%s,%s)',(userId,currentTime,0,currentTime,True))
            conn.commit()
    cur.close()

def deleteClient(id):
    conn = mysql.connect()
    cur =conn.cursor()
    cur.execute('DELETE FROM datos_cliente WHERE id = {0}'.format(id))
    conn.commit()
# settings

