from __future__ import annotations

from typing import List
from telethon import TelegramClient, events
from telethon.tl.custom.message import Message

from .handler import BaseMessageHandler


class ChatMonitor:
    def __init__(self, client: TelegramClient, chat: str, handler: BaseMessageHandler) -> None:
        self.client = client
        self.chat = chat
        self.handler = handler
        self._queue: List[Message] = []
        self._processing = False

    async def start(self) -> None:
        # Ensure the chat exists before registering the event handler
        try:
            await self.client.get_entity(self.chat)
        except Exception as exc:  # pragma: no cover - runtime validation
            raise ValueError(f"Chat '{self.chat}' not found") from exc

        @self.client.on(events.NewMessage(chats=self.chat))
        async def _(event: events.NewMessage.Event) -> None:  # pragma: no cover - simple callback
            self._queue.append(event.message)
            if not self._processing:
                await self._process_queue()

    async def _process_queue(self) -> None:
        self._processing = True
        while self._queue:
            batch = self._queue
            self._queue = []
            await self.handler.handle(self.chat, batch)
        self._processing = False
