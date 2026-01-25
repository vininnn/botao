from models.base.room_base import BaseRoom
from models.base.traits import OpenableRoom, JoinableRoom
from models.room_student import RoomStudent

class ServerRoom(BaseRoom, OpenableRoom, JoinableRoom):
    """Represents a study room within a Discord server where multiple users can join."""
    def __init__(self, guild_id: int, guild_name: str, name: str, channel_id: int):
        """Initializes a Server Study Room.

        Args:
            guild_id (int): The Discord server ID.
            guild_name (str): The Discord server name.
            name (str): Room name.
            channel_id (int): The Discord channel ID.
        """
        super().__init__(name)
        self.guild_id = guild_id
        self.guild_name = guild_name
        self.channel_id = channel_id
        # user_id -> Obj RoomStudent
        self.students: dict[int, RoomStudent] = {}

    def open(self) -> None:
        """Initializes the room state."""
        pass

    def join(self, user_id: int) -> None:
        """Adds a student to the room and starts their individual timer.

        Args:
            user_id (int): The Discord user ID.

        Raises:
            ValueError: If the student is already in this specific room.
        """
        if user_id in self.students:
            raise ValueError("Student is already in a server room.")

        self.students[user_id] = RoomStudent(user_id)

    def leave(self, user_id: int) -> int:
        """
        Removes a student and returns the duration of their room.

        Args:
            user_id (int): The Discord user ID.

        Raises:
            ValueError: If the student is not in the room.

        Returns:
            int: Seconds spent by the student in the room.
        """
        if user_id not in self.students:
            raise ValueError("Student is not in a server room.")

        student = self.students.pop(user_id)
        return student.leave()

    def is_empty(self) -> bool:
        """Returns True if there are no students currently in the room."""
        return len(self.students) == 0
