from pathlib import Path
import asyncio
from telethon import TelegramClient
from dotenv import load_dotenv

from tg_monitor.config import load_config
from tg_monitor.handler import PrintMessageHandler
from tg_monitor.monitor import ChatMonitor


async def main() -> None:
    load_dotenv(Path('.') / '.env')
    config = load_config()

    client = TelegramClient('monitor', config.api_id, config.api_hash)
    handler = PrintMessageHandler()

    async with client:
        if not config.chats:
            raise RuntimeError("No chats configured")
        monitor = ChatMonitor(client, config.chats[0], handler)
        await monitor.start()
        print(f"Monitoring chat: {config.chats[0]}")
        await client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.run(main())
