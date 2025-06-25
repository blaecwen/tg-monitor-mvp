import os
import sys
from pathlib import Path
from telethon import TelegramClient
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv(Path('.') / '.env')

api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
if not api_id or not api_hash:
    sys.stderr.write('Error: API_ID and API_HASH must be set in the .env file\n')
    sys.exit(1)

api_id = int(api_id)

# This session name will create a file 'hello.session'
client = TelegramClient('hello', api_id, api_hash)

async def main():
    # Send a message to yourself ("Saved Messages")
    await client.send_message('me', 'Hello, Telegram!')
    print('Message sent successfully!')

with client:
    client.loop.run_until_complete(main())
