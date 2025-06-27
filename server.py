from pathlib import Path
import asyncio
import logging
from telethon import TelegramClient
from dotenv import load_dotenv

from tg_monitor.config import load_config
from tg_monitor.handler import (
    PrintMessageHandler,
    GPTLoggingHandler,
    MultiHandler,
)
from tg_monitor.make_handler import MakeWebhookHandler
from tg_monitor.monitor import ChatMonitor
from tg_monitor import gpt_processor
from tg_monitor.logging import setup_logging

logger = logging.getLogger(__name__)
RUNTIME_DIR = Path("runtime")


async def main() -> None:
    load_dotenv(Path('.') / '.env')
    setup_logging()
    config = load_config()

    gpt_processor.set_gpt_model(config.gpt_model)


    client = TelegramClient(
        str(RUNTIME_DIR / 'monitor'),
        config.api_id,
        config.api_hash,
    )
    handler = MultiHandler(
        PrintMessageHandler(RUNTIME_DIR / 'last_message.json'),
        GPTLoggingHandler(RUNTIME_DIR / 'gpt_results.jsonl'),
        MakeWebhookHandler(),
    )

    async with client:
        if not config.chats:
            logger.error("no chats configured")
            return

        monitors = []
        for chat in config.chats:
            try:
                monitor = ChatMonitor(client, chat, handler)
                await monitor.start()
            except ValueError as exc:
                logger.error("%s", exc)
                continue
            monitors.append(monitor)
            logger.info("Monitoring chat: %s", chat)

        if not monitors:
            logger.error("no valid chats to monitor")
            return

        await client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.run(main())
