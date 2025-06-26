import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

mydb = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", 3306)),
    user=os.getenv("DB_USER", "root"),
    passwd=os.getenv("DB_PASSWORD", ""),
    database=os.getenv("DB_NAME", "eagleEyeDB")
)

cursor = mydb.cursor()
