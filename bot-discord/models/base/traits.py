from abc import ABC, abstractmethod

class OpenableRoom(ABC):
    @abstractmethod
    def open(self) -> None:
        pass

class CloseableRoom(ABC):
    @abstractmethod
    def close(self) -> None:
        pass

class JoinableRoom(ABC):
    @abstractmethod
    def join(self, user_id: int) -> None:
        pass

    @abstractmethod
    def leave(self, user_id: int) -> int:
        pass
    