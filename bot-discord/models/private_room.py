from models.base.room_base import BaseRoom
from models.base.traits import OpenableRoom, CloseableRoom

class PrivateRoom(BaseRoom, OpenableRoom, CloseableRoom):
    """Represents an individual study room for a single user."""
    def __init__(self, user_id: int, guild_name: str, name: str):
        """Initializes a Private Study Room.

        Args:
            user_id (int): Owner of the room.
            guild_name (str): The Discord server name.
            name (str): Room name.
        """
        super().__init__(name)
        self.guild_name = guild_name
        self.user_id = user_id
    
    def open(self) -> None:
        """Starts the room."""
        pass

    def close(self) -> None:
        """Finalizes the room and marks the end time."""
        self._mark_as_finished()

    @classmethod
    def from_duration(cls, user_id: int, guild_name, name: str, duration_seconds: int) -> "PrivateRoom":
        """
        Factory method to create a PrivateRoom instance from a known duration.

        Args:
            user_id (int): The Discord user ID.
            guild_name (str): The Discord server name.
            name (str): Room name.
            duration_seconds (int): Elapsed time.

        Returns:
            PrivateRoom: A reconstructed room object.
        """
        return super().create_history_entry(name, duration_seconds, user_id=user_id, guild_name=guild_name)
