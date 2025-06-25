# AGENTS.md

This repository is an early exploration of a Telegram monitoring server built with Telethon. It uses a Python script `hello.py` to send a sample message. The project expects API credentials in a `.env` file and must remain non-interactive.

## Guidelines for contributors and Codex agents

- Keep the application non-interactive. Fail fast if required environment variables are missing.
- Validate Python files with `python3 -m py_compile`.
- Validate shell scripts with `sh -n`.
- Dependencies are listed in `requirements.txt`; setup is automated via `setup.sh`.
- Provide concise commit messages and update documentation when behavior changes.
