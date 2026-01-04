from models.session import Session
from models.shared_session import SharedSession

class SharedSessionManager:
    def __init__(self, session_manager):
        self._shared_sessions: dict[tuple[int, str], SharedSession] = {}
        self._user_in_shared: dict[int, tuple[int, str]] = {}
        self._session_manager = session_manager

    def start(self, guild_id: int, name: str) -> None:
        key = (guild_id, name)

        if key in self._shared_sessions:
            raise ValueError('Shared session already exists')
        
        self._shared_sessions[key] = SharedSession(guild_id, name)

    def join(self, guild_id: int, name: str, user_id: int) -> None:
        key = (guild_id, name)

        if user_id in self._user_in_shared:
            raise ValueError("User already in a session")

        if key not in self._shared_sessions:
            raise ValueError("Shared session does not exist")

        shared = self._shared_sessions[key]
        shared.add_participant(user_id)

        self._user_in_shared[user_id] = key

    def leave(self, user_id: int) -> Session:
        if user_id not in self._user_in_shared:
            raise ValueError("User is not in a shared session")

        key = self._user_in_shared.pop(user_id)
        shared_session = self._shared_sessions[key]

        total_seconds = shared_session.remove_participant(user_id)

        session = Session.from_duration(
            user_id=user_id,
            name=shared_session.name,
            duration_seconds=total_seconds
        )

        self._session_manager.add_finished_session(session)

        # If session is empty, it is cancelled
        if shared_session.is_empty():
            del self._shared_sessions[key]

        return session

