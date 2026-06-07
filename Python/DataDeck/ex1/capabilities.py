from abc import ABC, abstractmethod


class HealCapability(ABC):
    """Abstract capability for healing."""

    @abstractmethod
    def heal(self) -> str:
        pass


class TransformCapability(ABC):
    """Abstract capability for transformation."""

    def __init__(self) -> None:
        self._transformed: bool = False

    @abstractmethod
    def transform(self) -> str:
        pass

    @abstractmethod
    def revert(self) -> str:
        pass
