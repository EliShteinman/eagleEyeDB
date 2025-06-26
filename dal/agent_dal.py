import os
from dotenv import load_dotenv

import mysql
import logging
from mysql.connector import connection
import time

from models.agent import Agent

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



def get_all_agents():
    get_all = "SELECT * FROM agents"
    with get_connection() as conn:
        if conn and conn.is_connected():
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(get_all)
                return cursor.fetchall()
        else:
            logger.error("Failed to connect to the database after multiple attempts.")
            return None

def add_agent_to_db(agent: tuple):
    add_agent = """
                INSERT INTO agents (code_name, real_name, location, status, missions_completed)
                VALUES (%s, %s, %s, %s, %s)
                """
    with get_connection() as conn:
        if conn and conn.is_connected():
            with conn.cursor() as cursor:
                cursor.execute(add_agent, agent)
                conn.commit()
                logger.info("Agent added successfully: %s", agent)
        else:
            logger.error("Failed to connect to the database after multiple attempts.")
            return None

def main():
    agents = [
        ("Agent001", "Jason Bourne", "New York", "Active", 5),
        ("Agent002", "Natasha Romanoff", "Moscow", "Inactive", 3),
        ("Agent003", "Ethan Hunt", "Paris", "Active", 7),
        ("Agent004", "Lara Croft", "Cairo", "Inactive", 2),
        ("Agent005", "James Bond", "London", "Active", 10),
        ("Agent006", "John Wick", "New York", "Active", 8),
        ("Agent007", "Black Widow", "Budapest", "Inactive", 4),
        ("Agent008", "Tom Cruise", "Tokyo", "Active", 6),
    ]
    for agent in agents:
        add_agent_to_db(agent)
    all_agents = get_all_agents()
    if all_agents:
        logger.info("All agents in the database:")
        for agent in all_agents:
            agent = Agent(**agent)
            print(agent)


if __name__ == "__main__":
    main()