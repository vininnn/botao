from abc import ABC, abstractmethod

class OpenableRoom(ABC):
    """Interface for rooms that can be opened/started."""
    @abstractmethod
    def open(self) -> None:
        """Defines the logic to initialize/start a room session."""
        pass

class CloseableRoom(ABC):
    """Interface for rooms that can be explicitly closed."""
    @abstractmethod
    def close(self) -> None:
        """Defines the logic to finalize a room session."""
        pass

class JoinableRoom(ABC):
    """Interface for rooms that support multiple participants joining and leaving."""
    @abstractmethod
    def join(self, user_id: int) -> None:
        """Registers a user into the room session."""
        pass

    @abstractmethod
    def leave(self, user_id: int) -> int:
        """Removes a user and returns their individual session duration."""
        pass
    