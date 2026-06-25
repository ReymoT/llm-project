from abc import ABC, abstractmethod


class Backend(ABC):
    name: str

    @abstractmethod
    async def chat_completions(self, payload: dict):
        pass

    @abstractmethod
    async def health(self) -> bool:
        pass
