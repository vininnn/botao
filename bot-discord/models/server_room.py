from models.base.room_base import BaseRoom
from models.base.traits import OpenableRoom, JoinableRoom
from models.room_student import RoomStudent

class ServerRoom(BaseRoom, OpenableRoom, JoinableRoom):
    def __init__(self, guild_id: int, name: str):
        super.__init__(name)
        self.guild_id = guild_id
        # user_id -> Obj RoomStudent
        self.students: dict[int, RoomStudent] = {}

    def open(self) -> None:
        pass

    def join(self, user_id: int) -> None:
        if user_id in self.students:
            raise ValueError("Student is already in a server room.")

        self.students[user_id] = RoomStudent(user_id)

    def leave(self, user_id: int) -> int:
        if user_id not in self.students:
            raise ValueError("Student is not in a server room.")

        student = self.students.pop(user_id)
        return student.leave()

    # Return True if the room is empty
    def is_empty(self) -> bool:
        return len(self.students) == 0
