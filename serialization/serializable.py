from abc import ABC, abstractmethod

class Serializable(ABC):
    @abstractmethod
    def get_serialization_data(self) -> dict[str, any]:
        pass

    @abstractmethod
    def get_identifier(self) -> str:
        pass