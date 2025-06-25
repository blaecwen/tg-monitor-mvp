from getpass import getpass
import os
from telethon import TelegramClient

api_id = os.environ.get('API_ID')
if api_id is None:
    api_id = int(input('Enter your API ID: '))
else:
    api_id = int(api_id)

api_hash = os.environ.get('API_HASH')
if api_hash is None:
    api_hash = getpass('Enter your API Hash: ')

# This session name will create a file 'hello.session'
client = TelegramClient('hello', api_id, api_hash)

async def main():
    # Send a message to yourself ("Saved Messages")
    await client.send_message('me', 'Hello, Telegram!')
    print('Message sent successfully!')

with client:
    client.loop.run_until_complete(main())
