import random, string
import sqlite3 as sl
from cryptography.fernet import Fernet

def genPassword(length):
    print("Generating...")
    password = ("".join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=length)))
    return password
