from models.session import Session

class SessionManager:
    def __init__(self):
        # user_id -> active session
        self._active_session : dict[int, Session] = {}
        # user_id -> list of finished sessions
        self._ended_sessions : dict[int, list[Session]] = {}

    # Create a new session for the user
    # Return False if user is already in a session
    def start_session(self, user_id: int, session_name: str) -> bool:
        if user_id in self._active_session:
            return False
        
        session = Session(user_id, session_name)
        self._active_session[user_id] = session
        return True
    
    # End an active session of a user
    # Return None if user not in a session
    def end_session(self, user_id: int) -> Session | None:
        session = self._active_session.pop(user_id, None)
        
        if session is None:
            return None
        
        session.set_end_time()
        if user_id not in self._ended_sessions:
            self._ended_sessions[user_id] = []
        self._ended_sessions[user_id].append(session)
        return session
    
    # Return an active session for the user, if any
    def get_active_session(self, user_id: int) -> Session | None:
        return self._active_session.get(user_id)
    
    # Returns the user's finished sessions history
    def get_ended_sessions(self, user_id: int) -> list[Session]:
        return self._ended_sessions.get(user_id, [])
    
    # Returns the user's time spent in a session
    def get_total_time_by_session(self, user_id: int, name: str) -> int:
        session = self._ended_sessions.get(user_id, [])
        
        return sum(
            sessions.duration_seconds
            for sessions in session
            if sessions.session_name == name
        )
    