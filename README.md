# tg-monitor-mvp

This repository includes small experiments with Telegram using [Telethon](https://github.com/LonamiWebs/Telethon).

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

Next, obtain your `API_ID` and `API_HASH` from [my.telegram.org](https://my.telegram.org) and set them as environment variables:

```shell
export API_ID=12345
export API_HASH=your_api_hash
```

Finally, run the example script:

```shell
python hello.py
```

You will be prompted to log in on the first run. Afterwards a message is sent to your **Saved Messages**.
