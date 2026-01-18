from models.base.room_base import BaseRoom
from models.base.traits import OpenableRoom, CloseableRoom

class PrivateRoom(BaseRoom, OpenableRoom, CloseableRoom):
    def __init__(self, user_id: int, name: str):
        super().__init__(name)
        self.user_id = user_id
    
    def open(self) -> None:
        pass

    def close(self) -> None:
        self._mark_as_finished()

    @classmethod
    def from_duration(cls, user_id: int, name: str, duration_seconds: int) -> "PrivateRoom":
        return super().create_history_entry(name, duration_seconds, user_id=user_id)
