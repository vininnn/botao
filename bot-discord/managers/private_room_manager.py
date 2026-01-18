from models.private_room import Room

class PrivateRoomManager:
    def __init__(self):
        self._open_rooms: dict[int, Room] = {}
        self._closed_rooms: dict[int, list[Room]] = {}
        self._server_room_manager = None

    def set_server_room_manager(self, server_room_manager) -> None:
        self._server_room_manager = server_room_manager

    # Create a new room for the user
    # Return False if user is already in a room
    def open(self, user_id: int, name: str) -> bool:
        if user_id in self._open_rooms:
            return False

        if self._server_room_manager and self._server_room_manager.is_user_in_shared(user_id):
            return False

        room = Room(user_id, name)
        room.open()
        self._open_rooms[user_id] = room
        return True
    
    # End an active room of a user
    # Return None if user not in a room
    def close(self, user_id: int) -> Room | None:
        room = self._open_rooms.pop(user_id, None)
        
        if room is None:
            return None
        
        room.close()
        self._add_to_history(room)
        return room
    
    def _add_to_history(self, room: Room) -> None:
        if room.user_id not in self._closed_rooms:
            self._closed_rooms[room.user_id] = []
        self._closed_rooms[room.user_id].append(room)

    def add_history_entry(self, room: Room) -> None:
        self._add_to_history(room)

    # Return an active room for the user, if any
    def get_open_room(self, user_id: int) -> Room | None:
        return self._open_rooms.get(user_id)
    
    def has_open_room(self, user_id: int) -> bool:
        return user_id in self._open_rooms
    
    # Returns the user's finished rooms history
    def get_closed_rooms(self, user_id: int) -> list[Room]:
        return self._closed_rooms.get(user_id, [])
    
    # Returns the user's time spent in a room
    def get_total_time_by_room(self, user_id: int, name: str) -> int:
        room = self._closed_rooms.get(user_id, [])
        
        return sum(
            rooms.duration_seconds
            for rooms in room
            if rooms.name == name
        )
