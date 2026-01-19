from datetime import datetime, timezone, timedelta
from abc import ABC

class BaseRoom(ABC):
    """Abstract base class representing the core timing logic for any room type."""
    def __init__(self, name: str):
        """Initializes a room with a name and a start timestamp.

        Args:
            name (str): The display name of the room.
        """
        self.name = name
        self.start_time: datetime = datetime.now(timezone.utc)
        self.end_time: datetime | None = None

    def _mark_as_finished(self) -> None:
        """Sets the end time to the current moment if not already finished."""
        if self.end_time is None:
            self.end_time = datetime.now(timezone.utc)
        
    @property
    def is_active(self) -> bool:
        """bool: True if the room is currently ongoing (no end time set)."""
        return self.end_time is None
    
    @property
    def duration_seconds(self) -> int:
        """Calculates the total duration of the room session in seconds.

        Returns:
            int: Seconds elapsed between start and end (or current time if active).
        """
        if self.end_time:
            return int((self.end_time - self.start_time).total_seconds())
        else:
            return int((datetime.now(timezone.utc) - self.start_time).total_seconds())
        
    @classmethod
    def create_history_entry(cls, name: str, duration_seconds: int, **kwargs) -> BaseRoom:  # type: ignore
        """Reconstructs a room object from historical data for record-keeping.

        Args:
            name (str): Original name of the room.
            duration_seconds (int): Total time spent in the room.
            **kwargs: Additional fields required by subclasses (e.g., user_id).

        Returns:
            BaseRoom: A finished room instance with calculated start/end times.
        """
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(seconds=duration_seconds)
        
        room = cls(name=name, **kwargs)
        room.start_time = start_time
        room.end_time = end_time
        
        return room        
