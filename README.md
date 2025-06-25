# tg-monitor-mvp

This repository contains the initial building blocks for a future Telegram monitoring server. It currently includes small experiments with [Telethon](https://github.com/LonamiWebs/Telethon).

## Hello Telethon

A simple example script `hello.py` demonstrates sending a `"Hello, Telegram!"` message to your own account.

### Usage

First, run the setup script to create a virtual environment and install the required packages:

```shell
sh setup.sh
```

After installation, activate the virtual environment. If you use **Bash** run:

```bash
source .venv/bin/activate
```

For **Fish** run:

```fish
source .venv/bin/activate.fish
```

Next, obtain your `API_ID` and `API_HASH` from [my.telegram.org](https://my.telegram.org) and store them in a `.env` file. Start by copying the example:

```shell
cp .env.example .env
```

Edit `.env` and fill in your credentials:

```env
API_ID=12345
API_HASH=your_api_hash
```

The example script automatically loads these variables from `.env` when run. It will exit with an error if either value is missing.

Finally, run the example script:

```shell
python hello.py
```

The script itself is non-interactive. Telethon may still prompt you to sign in on first use. Afterwards a message is sent to your **Saved Messages**.
