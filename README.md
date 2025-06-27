# tg-monitor-mvp

This project provides a minimal Telegram monitoring server built with [Telethon](https://github.com/LonamiWebs/Telethon). It watches the public chats listed in `config.json` and forwards new messages to a pluggable handler.

The default handler prints messages to stdout (showing each sender's username
when available) and writes the most recent one to `runtime/last_message.json`
using prettified JSON. Messages from the same chat
are processed in the order they arrive, batching any new ones while a previous
batch is handled. Runtime files, including the Telethon session, live inside the
`runtime/` directory which is ignored by git.
Datetime values in the JSON dump are encoded as ISO 8601 strings.

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

The server is non‑interactive. It prints errors to stderr when a configured chat is not found and skips it. If no valid chats remain, the server exits with an error.
All runtime files, including the Telethon session and the JSON dump, are stored in the `runtime/` directory.
