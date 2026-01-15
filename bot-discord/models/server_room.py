from models.room_student import RoomStudent

class ServerRoom:
    # Shared room within a single server
    def __init__(self, guild_id: int, name: str):
        self.guild_id = guild_id
        self.room_name = name
        self.students: dict[int, RoomStudent] = {}

    # Add a user in the shared room
    def add_student(self, user_id: int) -> None:
        if user_id in self.students:
            raise ValueError("User already in a server room")

        self.students[user_id] = RoomStudent(user_id)

    # Remove a user in the shared room
    def remove_student(self, user_id: int) -> int:
        if user_id not in self.students:
            raise ValueError("User not in a server room")

        student = self.students.pop(user_id)
        return student.leave()

    # Return True if the room is empty
    def is_empty(self) -> bool:
        return len(self.students) == 0

    # Return ids of active participants
    def get_students_ids(self) -> list[int]:
        return list(self.students.keys())
