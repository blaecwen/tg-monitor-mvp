from pathlib import Path
import asyncio
import sys
from telethon import TelegramClient
from dotenv import load_dotenv

from tg_monitor.config import load_config
from tg_monitor.handler import PrintMessageHandler, GPTLoggingHandler, MultiHandler
from tg_monitor.monitor import ChatMonitor
from tg_monitor import gpt_processor

RUNTIME_DIR = Path("runtime")


async def main() -> None:
    load_dotenv(Path('.') / '.env')
    config = load_config()

    gpt_processor.set_gpt_model(config.gpt_model)

    RUNTIME_DIR.mkdir(exist_ok=True)

    client = TelegramClient(
        str(RUNTIME_DIR / 'monitor'),
        config.api_id,
        config.api_hash,
    )
    handler = MultiHandler(
        PrintMessageHandler(RUNTIME_DIR / 'last_message.json'),
        GPTLoggingHandler(RUNTIME_DIR / 'gpt_results.jsonl'),
    )

    async with client:
        if not config.chats:
            print("Error: no chats configured", file=sys.stderr)
            return

        monitors = []
        for chat in config.chats:
            try:
                monitor = ChatMonitor(client, chat, handler)
                await monitor.start()
            except ValueError as exc:
                print(f"Error: {exc}", file=sys.stderr)
                continue
            monitors.append(monitor)
            print(f"Monitoring chat: {chat}")

        if not monitors:
            print("Error: no valid chats to monitor", file=sys.stderr)
            return

        await client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.run(main())
