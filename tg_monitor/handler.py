from typing import List
from telethon.tl.custom.message import Message


class BaseMessageHandler:
    async def handle(self, chat: str, messages: List[Message]) -> None:
        """Process a batch of messages for a chat.

        Override this method with custom logic.
        """
        raise NotImplementedError


class PrintMessageHandler(BaseMessageHandler):
    async def handle(self, chat: str, messages: List[Message]) -> None:
        for m in messages:
            print(f"[{chat}] {m.sender_id}: {m.text}")
