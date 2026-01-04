from models.participant_session import ParticipantSession

class SharedSession:
    # Shared session within a single server
    def __init__(self, guild_id: int, name: str):
        self.guild_id = guild_id
        self.name = name
        self.participants: dict[int, ParticipantSession] = {}

    # Add a user in the shared session
    def add_participant(self, user_id: int) -> None:
        if user_id in self.participants:
            raise ValueError("User already in shared session")

        self.participants[user_id] = ParticipantSession(user_id)

    # Remove a user in the shared session
    def remove_participant(self, user_id: int) -> int:
        if user_id not in self.participants:
            raise ValueError("User not in shared session")

        participant = self.participants.pop(user_id)
        return participant.leave()

    # Return True if the session is empty
    def is_empty(self) -> bool:
        return len(self.participants) == 0

    # Return ids of active participants
    def get_participant_ids(self) -> list[int]:
        return list(self.participants.keys())
