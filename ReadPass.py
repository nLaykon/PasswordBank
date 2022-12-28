import time, random, string
import sqlite3 as sl
from cryptography.fernet import Fernet
con = sl.connect('gen.db')
cur = con.cursor()
setKey = ""

#get key
keyRet = cur.execute("SELECT key FROM genKey")
key = keyRet.fetchone()
listlessKey = (key[0])
fernet = Fernet(listlessKey)

#Dump passwords
for row in cur.execute("SELECT website, email, password FROM passwords ORDER BY website"):
    decryptedPass = fernet.decrypt(row[2])

    print(row[0] + "    " + row[1] + "    " + decryptedPass.decode("utf-8"))
