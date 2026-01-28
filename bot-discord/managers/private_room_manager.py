from models.private_room import PrivateRoom

class PrivateRoomManager:
    """Manages the lifecycle of Private Study Rooms and tracks user study history."""
    def __init__(self):
        """Initializes the manager with empty active rooms and history records."""
        self._open_rooms: dict[int, PrivateRoom] = {}
        self._closed_rooms: dict[int, list[PrivateRoom]] = {}

    def open(self, user_id: int, guild_name: str, name: str) -> None:
        """Creates and starts a new Private Study Room for a user.

        Args:
            user_id (int): The Discord user ID.
            guild_name (str): The Discord server name.
            name (str): Room name.

        Raises:
            ValueError: If the user already has an active Private Study Room.
        """
        if user_id in self._open_rooms:
            raise ValueError('You already have an active Private Study Room.')

        room = PrivateRoom(user_id, guild_name, name)
        room.open()
        self._open_rooms[user_id] = room
    
    def leave(self, user_id: int) -> PrivateRoom:
        """Ends an active Private Study Room and moves it to the user's history.

        Args:
            user_id (int): The Discord user ID.

        Raises:
            ValueError: If the user does not have an active room to close.

        Returns:
            PrivateRoom: The closed room object containing final timing data.
        """
        room = self._open_rooms.pop(user_id, None)
        
        if room is None:
            raise ValueError("You are not in a Private Study Room! Try open it.")
        
        room.close()
        self._add_to_history(room)
        return room
    
    def _add_to_history(self, room: PrivateRoom) -> None:
        """Internal method to append a closed room to the history dictionary.

        Args:
            room (PrivateRoom): The closed room to record.
        """
        if room.user_id not in self._closed_rooms:
            self._closed_rooms[room.user_id] = []
        self._closed_rooms[room.user_id].append(room)

    def add_history_entry(self, room: PrivateRoom) -> None:
        """Public method to manually add a room to the history (used by Server Study Rooms).

        Args:
            room (PrivateRoom): The closed room to record.
        """
        self._add_to_history(room)

    def get_open_room(self, user_id: int) -> PrivateRoom:
        """Retrieves the user's currently active room.

        Args:
            user_id (int): The Discord user ID.

        Raises:
            ValueError: If no active room is found for the user.

        Returns:
            PrivateRoom: The active room object.
        """
        room = self._open_rooms.get(user_id)
        if not room:
            raise ValueError("You don't have a Private Study Room open right now.")
        return room

    def is_user_in_private_room(self, user_id: int) -> bool:
        """Checks if a user has an current private room.
        
        Args:
            user_id (int): The Discord user ID.
        """
        return user_id in self._open_rooms
    
    def get_left_rooms(self, user_id: int) -> list[PrivateRoom]:
        """Returns all closed rooms for a specific user.

        Args:
            user_id (int): The Discord user ID.

        Raises:
            ValueError: If the user has no recorded history.

        Returns:
            list[PrivateRoom]: A list containing all closed rooms of the user.
        """
        history = self._closed_rooms.get(user_id, [])
        if not history:
            raise ValueError('You have no study history yet.')
        return history

    def get_total_time_by_room(self, user_id: int, name: str) -> int:
        """Calculates the sum of all seconds studied across all historical room.

        Args:
            user_id (int): The Discord user ID.
            name (str): Room name

        Returns:
            int: Duration in seconds of the sum of rooms with the same name.
        """
        room = self._closed_rooms.get(user_id, [])
        
        return sum(
            rooms.duration_seconds
            for rooms in room
            if rooms.name == name
        )
