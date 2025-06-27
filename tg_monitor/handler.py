from typing import List
from pathlib import Path
import json
from telethon.tl.custom.message import Message


class BaseMessageHandler:
    async def handle(self, chat: str, messages: List[Message]) -> None:
        """Process a batch of messages for a chat.

        Override this method with custom logic.
        """
        raise NotImplementedError


class PrintMessageHandler(BaseMessageHandler):
    def __init__(self, dump_file: Path | str = Path("runtime/last_message.json")) -> None:
        self.dump_file = Path(dump_file)
        self.dump_file.parent.mkdir(parents=True, exist_ok=True)

    async def handle(self, chat: str, messages: List[Message]) -> None:
        for m in messages:
            print(f"[{chat}] {m.sender_id}: {m.text}")

        last = messages[-1]
        with self.dump_file.open("w", encoding="utf-8") as f:
            json.dump(last.to_dict(), f, indent=2, ensure_ascii=False, default=str)
            f.write("\n")
