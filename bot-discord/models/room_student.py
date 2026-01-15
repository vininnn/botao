from datetime import datetime, timezone

class RoomStudent:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.total_seconds = 0
        self.join_time: datetime = datetime.now(timezone.utc)

    # It ends the participation and returns the accumulated time in seconds.
    def leave(self) -> int:
        elapsed = int((datetime.now(timezone.utc) - self.join_time).total_seconds())
        self.total_seconds += elapsed
        return self.total_seconds
