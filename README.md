# tg-monitor-mvp

This project provides a minimal Telegram monitoring server built with [Telethon](https://github.com/LonamiWebs/Telethon). It watches one public chat defined in `config.json` and forwards new messages to a pluggable handler.

The default handler simply prints messages to stdout. Messages from the same chat are processed in the order they arrive, batching any new ones while a previous batch is handled.

## Setup

Install dependencies inside a virtual environment:

```sh
sh setup.sh
```

Activate the environment (Bash example):

```sh
source .venv/bin/activate
```

Copy the example configuration files and fill in the required values:

```sh
cp .env.example .env
cp config.json.example config.json
```

Edit `.env` and provide your `API_ID` and `API_HASH` from [my.telegram.org](https://my.telegram.org). `config.json` lists the public chats to monitor.

## Running

Start the monitoring server:

```sh
python server.py
```

The server is non‑interactive. It will exit with an error if required configuration is missing.
