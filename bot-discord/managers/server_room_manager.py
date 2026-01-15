from models.room import Room
from models.server_room import ServerRoom

class ServerRoomManager:
    def __init__(self, room_manager):
        self._server_rooms: dict[tuple[int, str], ServerRoom] = {}
        self._user_in_server_room: dict[int, tuple[int, str]] = {}
        self._room_manager = room_manager

    def start(self, guild_id: int, name: str) -> None:
        key = (guild_id, name)

        if key in self._server_rooms:
            raise ValueError('This server room already exists!')
        
        self._server_rooms[key] = ServerRoom(guild_id, name)

    def join(self, guild_id: int, name: str, user_id: int) -> None:
        key = (guild_id, name)

        if user_id in self._user_in_server_room:
            raise ValueError('You are already in a server room!')

        if self._room_manager.has_open_room(user_id):
            raise ValueError('You are already in a private room!')

        if key not in self._server_rooms:
            raise ValueError('This server room does not exist!')

        shared = self._server_rooms[key]
        shared.add_student(user_id)

        self._user_in_server_room[user_id] = key

    def leave(self, user_id: int) -> Room:
        if user_id not in self._user_in_server_room:
            raise ValueError('You are not in a server room!')

        key = self._user_in_server_room.pop(user_id)
        server_room = self._server_rooms[key]

        total_seconds = server_room.remove_student(user_id)

        room = Room.from_duration(
            user_id=user_id,
            name=server_room.room_name,
            duration_seconds=total_seconds
        )

        self._room_manager.add_closed_room(room)

        # If room is empty, it is cancelled
        if server_room.is_empty():
            del self._server_rooms[key]

        return room

    # Return all shared room from the server
    def list_rooms(self, guild_id: int) -> list[ServerRoom]:
        room_list = []
        for (gid, _), sesison in self._server_rooms.items():
            if gid == guild_id:
                room_list.append(sesison)

        return room_list
    
    # Verify if user already in a shared room
    def is_user_in_server_room(self, user_id: int) -> bool:
        return user_id in self._user_in_server_room