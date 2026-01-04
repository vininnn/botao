from datetime import datetime, timezone, timedelta

class Session:
    def __init__(self, user_id: int, session_name: str):
        self.user_id = user_id
        self.session_name = session_name
        self.start_time: datetime = datetime.now(timezone.utc)
        self.end_time: datetime | None = None
    
    def set_end_time(self) -> None:
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

    # Creates an ended sessions from a duration in seconds
    # Used by shared sessions
    @classmethod
    def from_duration(cls, user_id: int, name: str, duration_seconds: int) -> "Session":
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(seconds=duration_seconds)

        session = cls(user_id, name)
        session.start_time = start_time
        session.end_time = end_time

        return session
