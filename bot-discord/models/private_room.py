from models.base.room_base import BaseRoom
from models.base.traits import OpenableRoom, CloseableRoom

class PrivateRoom(BaseRoom, OpenableRoom, CloseableRoom):
    """Represents an individual study session for a single user."""
    def __init__(self, user_id: int, name: str):
        """Initializes a private room session.

        Args:
            user_id (int): Owner of the session.
            name (str): Room display name.
        """
        super().__init__(name)
        self.user_id = user_id
    
    def open(self) -> None:
        """Starts the session. (Inherited from OpenableRoom)"""
        pass

    def close(self) -> None:
        """Finalizes the session and marks the end time."""
        self._mark_as_finished()

    @classmethod
    def from_duration(cls, user_id: int, name: str, duration_seconds: int) -> "PrivateRoom":
        """
        Factory method to create a PrivateRoom instance from a known duration.

        Args:
            user_id (int): User ID.
            name (str): Room name.
            duration_seconds (int): Elapsed time.

        Returns:
            PrivateRoom: A reconstructed room object.
        """
        return super().create_history_entry(name, duration_seconds, user_id=user_id)
