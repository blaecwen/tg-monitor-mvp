# AGENTS.md

This repository hosts a minimal Telegram monitoring server built with Telethon. The legacy `hello.py` example has been replaced by a small server (`server.py`) that watches configured public chats and passes new messages to a pluggable handler. API credentials are still loaded from a `.env` file and the application must remain non-interactive. When a configured chat cannot be found, the server prints an error to stderr and continues with the remaining chats.

## Guidelines for contributors and Codex agents

- Keep the application non-interactive. Fail fast if required environment variables are missing.
- Validate Python files with `python3 -m py_compile`.
- Validate shell scripts with `sh -n`.
- Dependencies are listed in `requirements.txt`; setup is automated via `setup.sh`.
- Provide concise commit messages and update documentation when behavior changes.
- Until proper logging is added, print errors to stderr.
