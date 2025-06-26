import os
from dotenv import load_dotenv

import mysql
import logging
from mysql.connector import connection
import time

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Log to console
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

# Also log to a file
file_handler = logging.FileHandler("cpy-errors.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Load environment variables from .env file
load_dotenv()

config = {
    "host": os.getenv("DATABASE_HOST", "localhost"),
    "port": int(os.getenv("DATABASE_PORT", 3306)),
    "user": os.getenv("DATABASE_USER", "root"),
    "password": os.getenv("DATABASE_PASSWORD", ""),
    "database": os.getenv("DATABASE_NAME", "eagleEyeDB"),
}
cmd = "SELECT * FROM agents"
add_agent = "INSERT INTO agents (codeName, realName, location, status, missionsCompleted) VALUES (%s, %s, %s, %s, 5)"
val = ("Agent007", "James Bond", "London", "Active")


def get_connection(_config=config, attempts=3, delay=2):
    attempt = 1
    # Implement a reconnection routine
    while attempt < attempts + 1:
        try:
            return mysql.connector.connect(**_config)
        except (mysql.connector.Error, IOError) as err:
            if attempts is attempt:
                # Attempts to reconnect failed; returning None
                logger.info("Failed to connect, exiting without a connection: %s", err)
                return None
            logger.info(
                "Connection failed: %s. Retrying (%d/%d)...",
                err,
                attempt,
                attempts - 1,
            )
            # progressive reconnect delay
            time.sleep(delay**attempt)
            attempt += 1
    return None


with get_connection() as cnx:
    if cnx and cnx.is_connected():
        with cnx.cursor() as cursor:
            result = cursor.execute(cmd)
            # cnx.commit()
            rows = cursor.fetchall()
            for rows in rows:
                print(rows)
    else:
        logger.error("Failed to connect to the database after multiple attempts.")
        exit(1)


get_connection()
