from models.server_room import ServerRoom
from models.private_room import PrivateRoom

class PublicRoomManager:
    """Manages cross-server rooms."""
    def __init__(self, private_manager, server_manager):
        """Initializes the manager with internal tracking for rooms and student locations.

        Args:
            private_manager: PrivateRoomManager instance for history integration.
            server_manager: ServerRoomManager instance for history and commands integration
        """
        self._private_manager = private_manager
        self._server_manager = server_manager

        self._student_location : dict[int, str] = {}

        # Static rooms
        self._public_rooms: dict[str, ServerRoom] = {
            'Computing': ServerRoom(None, None, 'Computing', None),
            'Creative Arts': ServerRoom(None, None, 'Creative Arts', None,),
            'Exact Sciences': ServerRoom(None, None, 'Exact Sciences', None,),
            'Humanities': ServerRoom(None, None, 'Humanities', None,),
            'Writing': ServerRoom(None, None, 'Writing', None,),
        }
    
    def join(self, name: str, user_id: int) -> None:
        """Adds a user to an existing Public Study Room.

        Args:
            name (str): Room name.
            user_id (int): The Discord user ID.

        Raises:
            ValueError: If user is already in a Public Study Room.
        """

        if user_id in self._student_location:
            raise ValueError('You are already in a Public Study Room!')

        room = self._public_rooms[name]
        room.join(user_id)
        self._student_location[user_id] = name

    def leave(self, user_id: int) -> PrivateRoom:
        """Removes a user from their current Public Study Room and saves it to history.

        Args:
            user_id (int): The Discord user ID.

        Raises:
            ValueError: If the user is not in a Public Study Room.

        Returns:
            PrivateRoom: A history entry representing the finished room.
        """
        if user_id not in self._student_location:
            raise ValueError('You are not in a Public Study Room.')

        key = self._student_location.pop(user_id)
        room = self._public_rooms[key]

        total_seconds = room.leave(user_id)
        
        history_entry = PrivateRoom.from_duration(user_id, None, room.name, total_seconds)
        self._private_manager.add_history_entry(history_entry)

        return history_entry

    def list_rooms(self) -> list[ServerRoom]:
        """Retrieves all active global rooms within a spec.
        
        Returns:
            list[ServerRoom]: A list of active ServerRoom objects.
            The list come from server 0 = Global.
        """
        return list(self._public_rooms.values())

    def is_user_in_public_room(self, user_id: int) -> bool:
        """Checks if a user is currently participating in any Public Study Room.

        Args:
            user_id (int): The Discord user ID.

        Returns:
            bool: True if the user is in a Public Study Room, False otherwise.
        """
        return user_id in self._student_location
    
    def get_user_room(self, user_id: int) -> ServerRoom:
        """Locates and returns the specific room object where a user is present.

        Args:
            user_id (int): The Discord user ID.

        Raises:
            ValueError: If the user is not found in any active Public Study Room.

        Returns:
            ServerRoom: The room object the user is currently in.
        """
        location = self._student_location.get(user_id)

        if not location:
            raise ValueError('You are not in any Public Study Room.')
        return self._public_rooms[location]