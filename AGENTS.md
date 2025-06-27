# AGENTS.md

This repository hosts a minimal Telegram monitoring server built with Telethon. The legacy `hello.py` example has been replaced by a small server (`server.py`) that watches configured public chats and passes new messages to a pluggable handler. API credentials are still loaded from a `.env` file and the application must remain non-interactive. When a configured chat cannot be found, the server logs an error and continues with the remaining chats.

## Guidelines for contributors and Codex agents

- Keep the application non-interactive. Fail fast if required environment variables are missing.
- Validate Python files with `python3 -m py_compile`.
- Validate shell scripts with `sh -n`.
- Dependencies are listed in `requirements.txt`; setup is automated via `setup.sh`.
- Provide concise commit messages and update documentation when behavior changes.
- The application uses Python's ``logging`` module. ``setup_logging`` configures
  a console handler and a rotating file handler at ``runtime/server.log``.
  Adjust verbosity with the ``LOG_LEVEL`` environment variable
  (``ERROR``, ``WARNING``, ``INFO``, ``DEBUG``).
  Use the following guidelines for log levels:
  * **ERROR** – critical issues that severely impact the server's
    operation and typically cause a failure.
  * **WARNING** – recoverable problems affecting individual messages or
    other situations that require attention but don't stop the server.
  * **INFO** – normal operational messages and important state changes;
    avoid excessive repetition to keep logs readable.
  * **DEBUG** – verbose output useful when diagnosing problems. This
    level may include repetitive messages.
