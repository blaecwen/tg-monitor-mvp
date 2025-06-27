# tg-monitor-mvp

This project provides a minimal Telegram monitoring server built with [Telethon](https://github.com/LonamiWebs/Telethon). It watches the public chats listed in `config.json` and forwards new messages to a pluggable handler.

The default handler logs messages to the console and writes the most recent one to
`runtime/last_message.json` using prettified JSON. A second handler processes
each message with an OpenAI GPT model and appends the generated JSON
to `runtime/gpt_results.jsonl`. Messages from the same chat are processed in the
order they arrive, batching any new ones while a previous batch is handled.
Runtime files, including the Telethon session, live inside the `runtime/`
directory which is ignored by git.

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

Edit `.env` and provide your `API_ID`, `API_HASH`, and `OPENAI_API_KEY`.
`GPT_PROMPT_FILE` is optional and can point to a custom prompt file. If unset,
the built-in prompt `tg_monitor/gpt_prompt.txt` is used.
`config.json` lists the public chats to monitor and can override the GPT model
with a `gpt_model` field (defaults to `gpt-4o`).

## Running

Start the monitoring server:

```sh
python server.py
```

The server is non‑interactive. Messages and errors are logged to the console and
`runtime/server.log`. Set the `LOG_LEVEL` environment variable to control the
verbosity. When a configured chat cannot be found, the error is logged and the
server continues. If no valid chats remain, the server exits with an error. The
GPT logging handler logs the selected model when the server starts and writes
only successful JSON results. Any parsing or API errors are logged as warnings.
All runtime files, including the Telethon session and the JSON dump, are stored
in the `runtime/` directory.

## Logging levels

- **ERROR**: critical issues affecting server performance
- **WARNING**: recoverable problems with individual messages
- **INFO**: key configuration or state changes, avoid spamming
- **DEBUG**: additional details useful when debugging

A `robots.txt` file disables indexing of the `runtime/` directory.
