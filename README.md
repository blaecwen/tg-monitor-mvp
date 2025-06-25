# tg-monitor-mvp

This repository includes small experiments with Telegram using [Telethon](https://github.com/LonamiWebs/Telethon).

## Hello Telethon

A simple example script `hello.py` demonstrates sending a `"Hello, Telegram!"` message to your own account.

### Usage

1. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
   Then install dependencies:
   ```bash
   pip install telethon
   ```
2. Obtain your `API_ID` and `API_HASH` from [my.telegram.org](https://my.telegram.org) and set them as environment variables:
   ```bash
   export API_ID=12345
   export API_HASH=your_api_hash
   ```
3. Run the script:
   ```bash
   python hello.py
   ```
   You will be prompted to log in on first run. Afterwards a message is sent to your **Saved Messages**.
