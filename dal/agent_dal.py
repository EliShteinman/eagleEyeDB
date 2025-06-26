from logging_config import logger
from dal.dal import get_connection


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
                INSERT IGNORE INTO agents (code_name, real_name, location, status, missions_completed)
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
