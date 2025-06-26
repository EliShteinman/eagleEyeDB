from logging_config import logger
from models.agent import Agent
from dal.agent_dal import get_all_agents, add_agent_to_db


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
    all_agents = get_all_agents()
    if all_agents:
        logger.info("All agents in the database:")
        for agent in all_agents:
            print(agent)
    else:
        logger.error("No agents found or failed to retrieve agents from the database.")
