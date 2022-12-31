#
#   THIS IS VERY MUCH SO A WORK IN PROGRESS
#   DONT EXPECT THIS TO BE 100% FUNCTIONAL
#

import random, string
import sqlite3 as sl
from cryptography.fernet import Fernet

#DATABASE CONNECTION
con = sl.connect('gen.db')
cur = con.cursor()
setKey = ""
#DATABASE CONNECTION END

#TABLE CREATION / CONNECTION
try:
    cur.execute("CREATE TABLE genKey(key)")
    print("Key Table Created")
except:
    print("Key Table Found :)")
try:
    cur.execute("CREATE TABLE passwords(website, email, password)")
    print("Password Table Created :)")
except:
    print("Password Table Found")
#TABLE CRATION / CONNECTION END

#GET KEY
keyRet = cur.execute("SELECT key FROM genKey")
#GET KEY END

#CHECK KEY
key = keyRet.fetchone()
if (key is None):
    #Gen Key if doesn't exist
    setKey = Fernet.generate_key()
    #set key to list
    key = [setKey]
    #Send Key to database
    cur.execute("INSERT INTO genKey VALUES(?)", key)
    con.commit()
    print("Key Set")
print("Key Found")
#CHECK KEY END

#CONVERT KEY TO STRING
listlessKey = (key[0])
#CONVERT KEY TO STRING END

#INITIALIZE FERNET
fernet = Fernet(listlessKey)
#INITIALIZE FERNET END

#FUNCTIONS
def genPassword(length):
    print("Generating...")
    password = ("".join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=length)))
    return password

def readData(Data):
    print("Not sure how this is gonna work yet")

def encryptData(Data):
    byteEncData = str.encode(Data)
    encryptedData = fernet.encrypt(byteEncData)
    return encryptedData

def decryptData(Data):
    decryptedData = fernet.decrypt(Data)
    stringData = decryptedData.decode("utf-8")
    return stringData
    

def sendToDataBase(EncWeb, EncEmail, EncPass):
    print("Test Func")
#FUNCTIONS END
