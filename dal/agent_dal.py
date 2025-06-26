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

# SQL queries
get_all = "SELECT * FROM agents"
add_agent = """
            INSERT INTO agents (codeName, realName, location, status, missionsCompleted) 
            VALUES (%s, %s, %s, %s, 5)
            """
agents = [
    ("Agent001", "Jason Bourne", "New York", "Active"),
    ("Agent002", "Natasha Romanoff", "Moscow", "Inactive"),
    ("Agent003", "Ethan Hunt", "Paris", "Active"),
    ("Agent004", "Lara Croft", "Cairo", "Inactive")
]

def main():
    with get_connection() as conn:
        if conn and conn.is_connected():
            with conn.cursor(dictionary=True) as cmd:
                for agent in agents:
                    cmd.execute(add_agent, agent)
                    conn.commit()
                # rows = cursor.fetchall()
                # while cursor.fetchone():
                #     print(cursor.fetchone())
                for row in cmd:
                    print(row)

                # for row in rows:
                #     print(row)
        else:
            logger.error("Failed to connect to the database after multiple attempts.")
            exit(1)


if __name__ == "__main__":
    main()
    # Uncomment the following lines to add an agent
    # with get_connection() as cnx:
    #     if cnx and cnx.is_connected():
    #         with cnx.cursor() as cursor:
    #             cursor.execute(add_agent, val)
    #             cnx.commit()
    #             print("Agent added successfully.")
    #     else:
    #         logger.error("Failed to connect to the database after multiple attempts.")
    #         exit(1)