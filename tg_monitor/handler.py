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


class MultiHandler(BaseMessageHandler):
    """Chain multiple handlers together."""

    def __init__(self, *handlers: BaseMessageHandler) -> None:
        self.handlers = handlers

    async def handle(self, chat: str, messages: List[Message]) -> None:
        for h in self.handlers:
            await h.handle(chat, messages)


class PrintMessageHandler(BaseMessageHandler):
    def __init__(self, dump_file: Path | str = Path("runtime/last_message.json")) -> None:
        self.dump_file = Path(dump_file)
        self.dump_file.parent.mkdir(parents=True, exist_ok=True)

    async def handle(self, chat: str, messages: List[Message]) -> None:
        for m in messages:
            sender = await m.get_sender()
            username = getattr(sender, "username", None) if sender else None
            print(f"[{chat}] {username or m.sender_id}: {m.text}")

        last = messages[-1]
        with self.dump_file.open("w", encoding="utf-8") as f:
            json.dump(last.to_dict(), f, indent=2, ensure_ascii=False, default=str)
            f.write("\n")

            
class GPTLoggingHandler(BaseMessageHandler):
    """Handler that processes messages with GPT and logs JSON results."""

    def __init__(self, log_file: Path | str = Path("runtime/gpt_results.jsonl")) -> None:
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    async def handle(self, chat: str, messages: List[Message]) -> None:
        from .gpt_processor import process_text_with_gpt

        for m in messages:
            result = await process_text_with_gpt(m.text or "")
            record = {
                "chat": chat,
                "message_id": m.id,
                "result": result,
            }
            with self.log_file.open("a", encoding="utf-8") as f:
                json.dump(record, f, ensure_ascii=False, default=str)
                f.write("\n")

