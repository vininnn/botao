from datetime import datetime, timezone

class RoomStudent:
    """Represents a student's individual session within a shared room."""
    def __init__(self, user_id: int):
        """Initializes the student record with the current UTC join time.

        Args:
            user_id (int): The Discord user ID.
        """
        self.user_id = user_id
        self.join_time: datetime = datetime.now(timezone.utc)

    def leave(self) -> int:
        """Ends the session and calculates total time spent.

        Returns:
            int: Accumulated time in seconds since joining.
        """
        elapsed = int((datetime.now(timezone.utc) - self.join_time).total_seconds())
        return elapsed
