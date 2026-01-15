from models.room import Room

class RoomManager:
    def __init__(self):
        # user_id -> active room
        self._open_room: dict[int, Room] = {}
        # user_id -> list of finished rooms
        self._closed_rooms: dict[int, list[Room]] = {}

        # injected later
        self._server_room_manager = None

    def set_server_room_manager(self, server_room_manager) -> None:
        self._server_room_manager = server_room_manager

    # Create a new room for the user
    # Return False if user is already in a room
    def start(self, user_id: int, room_name: str) -> bool:
        if user_id in self._open_room:
            return False

        if self._server_room_manager and self._server_room_manager.is_user_in_shared(user_id):
            return False

        room = Room(user_id, room_name)
        self._open_room[user_id] = room
        return True
    
    # End an active room of a user
    # Return None if user not in a room
    def close(self, user_id: int) -> Room | None:
        room = self._open_room.pop(user_id, None)
        
        if room is None:
            return None
        
        room.set_end_time()
        if user_id not in self._closed_rooms:
            self._closed_rooms[user_id] = []
        self._closed_rooms[user_id].append(room)
        return room
    
    # Return an active room for the user, if any
    def get_active_room(self, user_id: int) -> Room | None:
        return self._open_room.get(user_id)
    
    # Returns the user's finished rooms history
    def get_closed_rooms(self, user_id: int) -> list[Room]:
        return self._closed_rooms.get(user_id, [])
    
    # Returns the user's time spent in a room
    def get_total_time_by_room(self, user_id: int, name: str) -> int:
        room = self._closed_rooms.get(user_id, [])
        
        return sum(
            rooms.duration_seconds
            for rooms in room
            if rooms.room_name == name
        )
    
    # Return True if user is in a active room
    # Used in shared room
    def has_open_room(self, user_id: int) -> bool:
        return user_id in self._open_room
    
    # Registers a finished room (used by shared rooms)
    def add_closed_room(self, room: Room) -> None:
        user_id = room.user_id

        if user_id not in self._closed_rooms:
            self._closed_rooms[user_id] = []

        self._closed_rooms[user_id].append(room)