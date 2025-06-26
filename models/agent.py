from enums import AgentStatus


class Agent:
    """
    Represents an agent with a code name, real name, location,
    status, and number of missions completed.
    """

    def __init__(
            self,
            code_name: str,
            real_name: str,
            location: str,
            status: str = "active",
            missions_completed: int = 0,
            _id: int = None,
    ):
        """
        Initializes an Agent object with the given parameters.

        :param code_name: Code name of the agent
        :param real_name: Real name of the agent
        :param location: Location of the agent
        :param status: Status of the agent (must be one of: 'ACTIVE', 'INACTIVE', 'SUSPENDED', 'TERMINATED')
        :param missions_completed: Number of missions completed by the agent
        :param _id: Optional unique identifier for the agent
        """
        self.id: int | None = _id
        self.code_name: str = code_name
        self.real_name: str = real_name
        self.location: str = location
        self.status: AgentStatus = self.validate_status(status)
        self.missions_completed: int = missions_completed

    def __str__(self):
        """String representation of the Agent object."""
        if self.id is not None:
            return (
                f"Agent {self.code_name} ({self.real_name}) - ID: {self.id}, "
                f"Status: {self.status}, Location: {self.location}, "
                f"Missions Completed: {self.missions_completed}"
            )
        return (
            f"Agent {self.code_name} ({self.real_name}) - "
            f"Status: {self.status}, Location: {self.location}, "
            f"Missions Completed: {self.missions_completed}"
        )

    @staticmethod
    def validate_status(status: str) -> AgentStatus:
        """
        Validates the status string against the AgentStatus enum by name.
        Converts to uppercase and checks if it matches any enum member.

        :param status: Status string (must be one of: 'ACTIVE', 'INACTIVE', 'SUSPENDED', 'TERMINATED')
        :return: AgentStatus enum value
        :raises ValueError: If status is not a valid enum name
        """
        if not isinstance(status, str):
            raise TypeError(f"Expected status as string, got {type(status).__name__}")

        status_name = status.upper()
        if status_name not in AgentStatus.__members__:
            raise ValueError(
                f"Invalid status: '{status}'. Must be one of: {list(AgentStatus.__members__.keys())}"
            )
        return AgentStatus[status_name]