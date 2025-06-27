import os
import sys
from typing import List

import aiohttp
from telethon.tl.custom.message import Message

from .gpt_processor import process_text_with_gpt
from .handler import BaseMessageHandler


class MakeWebhookHandler(BaseMessageHandler):
    """Send relevant GPT results to a Make webhook."""

    def __init__(self, webhook_url: str | None = None) -> None:
        self.webhook_url = webhook_url or os.environ.get("MAKE_WEBHOOK_URL")
        if not self.webhook_url:
            print(
                "Warning: MAKE_WEBHOOK_URL is not set; Make webhook disabled",
                file=sys.stderr,
            )

    async def handle(self, chat: str, messages: List[Message]) -> None:
        if not self.webhook_url:
            return

        async with aiohttp.ClientSession() as session:
            for m in messages:
                result = getattr(m, "gpt_result", None)
                if result is None:
                    result = await process_text_with_gpt(m.text or "")
                    m.gpt_result = result
                relevance = result.get("relevance")
                if relevance and relevance != "irrelevant":
                    await session.post(
                        self.webhook_url,
                        json={"chat": chat, "message_id": m.id, "result": result},
                    )

