from datetime import datetime, timezone, timedelta
from abc import ABC

class BaseRoom(ABC):
    def __init__(self, name: str):
        self.name = name
        self.start_time: datetime = datetime.now(timezone.utc)
        self.end_time: datetime | None = None

    def _mark_as_finished(self) -> None:
        if self.end_time is None:
            self.end_time = datetime.now(timezone.utc)
        
    @property
    def is_active(self) -> bool:
        return self.end_time is None
    
    @property
    def duration_seconds(self) -> int:
        if self.end_time:
            return int((self.end_time - self.start_time).total_seconds())
        else:
            return int((datetime.now(timezone.utc) - self.start_time).total_seconds())
        
    @classmethod
    def create_history_entry(cls, name: str, duration_seconds: int, **kwargs):
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(seconds=duration_seconds)
        
        room = cls(name=name, **kwargs)
        room.start_time = start_time
        room.end_time = end_time
        
        return room        
