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
If `MAKE_WEBHOOK_URL` is set, any GPT result whose `relevance` is not
`irrelevant` is POSTed to that URL. When the variable is missing, the
server prints a warning and continues without Make integration.

## Running

Start the monitoring server:

```sh
python server.py
```

The server is non‑interactive. Messages and errors are logged to the console and
`runtime/server.log`. When a configured chat cannot be found, the error is
logged and the server continues. If no valid chats remain, the server exits with
an error. When the server starts the GPT logging handler prints a one-line
summary of the GPT settings (model, temperature and prompt file) and writes only
successful JSON results. GPT responses use the API's JSON mode, so the content
is returned directly as a JSON object. Any parsing or API errors are logged as
warnings and include the raw response at the debug level. All runtime files,
including the
Telethon session and the JSON dump, are stored in the `runtime/` directory.

A `robots.txt` file disables indexing of the `runtime/` directory.

## Deploying on Render.com

The repository includes a `render.yaml` file for deploying as a Background Worker.
Render installs dependencies via `setup.sh` and runs `python server.py`.

1. Sign in to [Render](https://render.com/) and choose **New > Blueprint**.
2. Select this repository and confirm the service settings.
   - **Branch**: `master` (the worker redeploys on each push).
   - **Environment**: `Python`.
3. Set the environment variables `API_ID`, `API_HASH` and `OPENAI_API_KEY`.
   Optional variables `GPT_PROMPT_FILE` and `MAKE_WEBHOOK_URL` can also be set.
4. Provide a `config.json` file in the repository or upload it as a secret file.
   Use `config.json.example` as a template.

Deploying the blueprint creates a worker that automatically tracks the
latest `master` commit.
