import time, random, string
import sqlite3 as sl
from cryptography.fernet import Fernet
#connect/create database
con = sl.connect('gen.db')
#create cursor for datavase
cur = con.cursor()
#define key
setKey = ""
#define Length for Generated passwords
length = 0
#Try Creating Key Table
try:
    cur.execute("CREATE TABLE genKey(key)")
    print("Key Table Created")
except:
    print("Key Table Found :)")

#Try Creating Data Table
try:
    cur.execute("CREATE TABLE passwords(website, email, password)")
    print("Password Table Created :)")
except:
    print("Password Table Found")
#Get Encryption Key
keyRet = cur.execute("SELECT key FROM genKey")
key = keyRet.fetchone()
#Check if key doesn't exist
if (key is None):
    #Gen Key if doesn't exist
    setKey = Fernet.generate_key()
    #set key to list
    key = [setKey]
    #Send Key to database
    cur.execute("INSERT INTO genKey VALUES(?)", key)
    con.commit()
    print("Key Set")
#Key Generated or Already exists
print("Key Found")
#Get Key data
listlessKey = (key[0])

#initialize fernet
fernet = Fernet(listlessKey)

#User input
site = input("Please input website(www.example.com): ")
email = input("Please input username or Email(exampleUser // example@example.com): ")

#Select Generate Password or Input Password
confimation = input("Do you want to Generate or Input password? ('G' or 'I'): ")
password = ""
#Generate password if G
if (confimation == "G"):

    length = int(input("How many characters do you want? "))
    print("Generating...")
    password = ("".join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=length)))
    #Convert Password into Bytes
    bytePass = str.encode(password)
    #Encrypt Password using EncryptionKey
    encryptedPass = fernet.encrypt(bytePass)
else:
    #input Password
    password = input("Input Password: ")
    #Convert Password into Bytes
    bytePass = str.encode(password)
    #Encrypt Password
    encryptedPass = fernet.encrypt(bytePass)
#Put all Data into a list
data = ([site, email, encryptedPass])
#Send the list to the database
cur.execute("INSERT INTO passwords VALUES(?, ?, ?)", data)
con.commit()
#Done!
print("Info Saved to Database!")
