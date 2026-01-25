from models.private_room import PrivateRoom
from models.server_room import ServerRoom

class ServerRoomManager:
    """Manages server rooms across different Discord guilds."""
    def __init__(self, private_manager):
        """Initializes the manager with internal tracking for rooms and student locations.

        Args:
            private_manager: PrivateRoomManager instance for history integration.
        """
        self._server_rooms: dict[tuple[int, str], ServerRoom] = {}
        self._student_location: dict[int, tuple[int, str]] = {}
        self._private_manager = private_manager

    def open(self, guild_id: int, guild_name: str, name: str, channel_id: int) -> None:
        """Opens a new Server Study Room in a guild.

        Args:
            guild_id (int): The Discord server ID.
            guild_name (str): The Discord server name.
            name (str): Room name.
            channel_id (int): The Discord channel ID.

        Raises:
            ValueError: If a room with the same name already exists in the guild.
        """
        key = (guild_id, name)

        if key in self._server_rooms:
            raise ValueError(f'A Server Study Room named "{name}" already exists in this server.')
        
        room = ServerRoom(guild_id, guild_name, name, channel_id)
        room.open()
        self._server_rooms[key] = room

    def join(self, guild_id: int, name: str, user_id: int) -> None:
        """Adds a user to an existing Server Study Room.

        Args:
            guild_id (int): The Discord server ID.
            name (str): Room name.
            user_id (int): The Discord user ID.

        Raises:
            ValueError: If user is already in a Server Study Room.
            ValueError: If the room doesn't exist.
        """
        key = (guild_id, name)

        if user_id in self._student_location:
            raise ValueError('You already are in a Server Study Room! Leave it first.')

        if key not in self._server_rooms:
            raise ValueError('This Server Study Room does not exist!')

        room = self._server_rooms[key]
        room.join(user_id)
        self._student_location[user_id] = key

    def leave(self, user_id: int) -> PrivateRoom:
        """Removes a user from their current Server Study Room and saves it to history.

        Args:
            user_id (int): The Discord user ID.

        Raises:
            ValueError: If the user is not in a Server Study Room.

        Returns:
            PrivateRoom: A history entry representing the finished room.
        """
        if user_id not in self._student_location:
            raise ValueError('You are not in a Server Study Room!')

        key = self._student_location.pop(user_id)
        room = self._server_rooms[key]

        total_seconds = room.leave(user_id)

        history_entry = PrivateRoom.from_duration(user_id, room.guild_name, room.name, total_seconds)
        self._private_manager.add_history_entry(history_entry)

        # If room is empty, it is cancelled
        if room.is_empty():
            del self._server_rooms[key]

        return history_entry

    def list_rooms(self, guild_id: int) -> list[ServerRoom]:
        """Retrieves all active server rooms within a specific Discord guild.

        Args:
            guild_id (int): The Discord server ID.

        Raises:
            ValueError: If no active server rooms are found for the given guild.

        Returns:
            list[ServerRoom]: A list of active ServerRoom objects.
        """
        room_list = []
        for (gid, _), room in self._server_rooms.items():
            if gid == guild_id:
                room_list.append(room)
        
        if not room_list:
            raise ValueError('There are no active server rooms in this server.')
        return room_list
    
    def is_user_in_server_room(self, user_id: int) -> bool:
        """Checks if a user is currently participating in any Server Study Room.

        Args:
            user_id (int): The Discord user ID.

        Returns:
            bool: True if the user is in a Server Study Room, False otherwise.
        """
        return user_id in self._student_location

    def get_user_room(self, user_id: int) -> ServerRoom:
        """Locates and returns the specific room object where a user is present.

        Args:
            user_id (int): The Discord user ID.

        Raises:
            ValueError: If the user is not found in any active Server Study Room.

        Returns:
            ServerRoom: The room object the user is currently in.
        """
        location = self._student_location.get(user_id)

        if not location:
            raise ValueError('You are not in a Server Study Room.')
        return self._server_rooms.get(location)
    
    def get_room(self, guild_id: int, name: str) -> ServerRoom:
        """Locates and returns the specific room object by guild ID and room name.

        Args:
            guild_id (int): The Discord server ID.
            name (str): Room name.

        Raises:
            ValueError: If the room doesn't exist.

        Returns:
            ServerRoom: The room object with the search name.
        """
        key = (guild_id, name)
        room = self._server_rooms.get(key)

        if not room:
            raise ValueError('This Server Study Room does not exist!')
        return room
    