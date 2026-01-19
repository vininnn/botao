from models.private_room import PrivateRoom
from models.server_room import ServerRoom

class ServerRoomManager:
    """Manages shared study rooms across different Discord guilds."""
    def __init__(self, room_manager):
        """Initializes the manager with internal tracking for rooms and student locations.

        Args:
            room_manager: PrivateRoomManager instance for history integration.
        """
        self._server_rooms: dict[tuple[int, str], ServerRoom] = {}
        self._student_location: dict[int, tuple[int, str]] = {}
        self._room_manager = room_manager

    def open(self, guild_id: int, name: str) -> None:
        """Creates and opens a new shared room in a guild.

        Args:
            guild_id (int): Discord Guild ID.
            name (str): Unique name for the room in that server.

        Raises:
            ValueError: If a room with the same name already exists in the guild.
        """
        key = (guild_id, name)

        if key in self._server_rooms:
            raise ValueError(f'A shared room named "{name}" already exists in this server.')
        
        room = ServerRoom(guild_id, name)
        room.open()
        self._server_rooms[key] = room

    def join(self, guild_id: int, name: str, user_id: int) -> None:
        """Adds a user to an existing server room.

        Args:
            guild_id (int): Discord Guild ID.
            name (str): Name of the room to join.
            user_id (int): Discord User ID.

        Raises:
            ValueError: If user is already in a Server Room.
            ValueError: If the room doesn't exist.
        """
        key = (guild_id, name)

        if user_id in self._student_location:
            raise ValueError('You are already in a Server Room!')

        if key not in self._server_rooms:
            raise ValueError('This Server Room does not exist!')

        room = self._server_rooms[key]
        room.join(user_id)
        self._student_location[user_id] = key

    def leave(self, user_id: int) -> PrivateRoom:
        """Removes a user from their current server room and saves the session to history.

        Args:
            user_id (int): Discord User ID.

        Raises:
            ValueError: If the user is not in a server room.

        Returns:
            PrivateRoom: A history entry representing the finished session.
        """
        if user_id not in self._student_location:
            raise ValueError('You are not in a Server Room!')

        key = self._student_location.pop(user_id)
        room = self._server_rooms[key]

        total_seconds = room.leave(user_id)

        history_entry = PrivateRoom.from_duration(user_id, room.name, total_seconds)
        self._room_manager.add_history_entry(history_entry)

        # If room is empty, it is cancelled
        if room.is_empty():
            del self._server_rooms[key]

        return history_entry

    def list_rooms(self, guild_id: int) -> list[ServerRoom]:
        """Retrieves all active shared rooms within a specific Discord guild.

        Args:
            guild_id (int): The unique ID of the server/guild.

        Raises:
            ValueError: If no active shared rooms are found for the given guild.

        Returns:
            list[ServerRoom]: A list of active ServerRoom objects.
        """
        room_list = []
        for (gid, _), room in self._server_rooms.items():
            if gid == guild_id:
                room_list.append(room)
        
        if not room_list:
            raise ValueError('There are no active shared rooms in this server.')
        return room_list
    
    def is_user_in_server_room(self, user_id: int) -> bool:
        """Checks if a user is currently participating in any shared server room.

        Args:
            user_id (int): The Discord user ID to verify.

        Returns:
            bool: True if the user is in a server room, False otherwise.
        """
        return user_id in self._student_location

    def get_user_room(self, user_id: int) -> ServerRoom:
        """Locates and returns the specific room object where a user is present.

        Args:
            user_id (int): The Discord user ID.

        Raises:
            ValueError: If the user is not found in any active server room.

        Returns:
            ServerRoom: The room object the user is currently in
        """
        location = self._student_location.get(user_id)

        if not location:
            raise ValueError('You are not in any server room.')
        return self._server_rooms.get(location)
    