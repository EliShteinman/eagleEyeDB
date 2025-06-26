from enum import Enum


class AgentStatus(Enum):
    """
    Enum representing the status of an agent.
    """

    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"

    def __str__(self):
        return self.value
