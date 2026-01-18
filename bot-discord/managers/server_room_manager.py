from models.private_room import PrivateRoom
from models.server_room import ServerRoom

class ServerRoomManager:
    def __init__(self, room_manager):
        self._server_rooms: dict[tuple[int, str], ServerRoom] = {}
        self._student_location: dict[int, tuple[int, str]] = {}
        self._room_manager = room_manager

    def open(self, guild_id: int, name: str) -> None:
        key = (guild_id, name)

        if key in self._server_rooms:
            raise ValueError('A Server Room with this name already exists.')
        
        room = ServerRoom(guild_id, name)
        room.open()
        self._server_rooms[key] = room

    def join(self, guild_id: int, name: str, user_id: int) -> None:
        key = (guild_id, name)

        if user_id in self._student_location:
            raise ValueError('You are already in a Server Room!')

        if self._room_manager.has_open_room(user_id):
            raise ValueError('You are currently in a Private Room!')

        if key not in self._server_rooms:
            raise ValueError('This Server Room does not exist!')

        room = self._server_rooms[key]
        room.join(user_id)
        self._student_location[user_id] = key

    def leave(self, user_id: int) -> PrivateRoom:
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

    # Return all shared room from the server
    def list_rooms(self, guild_id: int) -> list[ServerRoom]:
        room_list = []
        for (gid, _), room in self._server_rooms.items():
            if gid == guild_id:
                room_list.append(room)

        return room_list
    
    # Verify if user already in a shared room
    def is_user_in_server_room(self, user_id: int) -> bool:
        return user_id in self._student_location

    def get_user_room(self, user_id: int) -> ServerRoom | None:
        """Retorna o objeto da sala onde o usuário está, se houver."""
        location = self._student_location.get(user_id)
        if location:
            return self._server_rooms.get(location)
        return None
    