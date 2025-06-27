import json
import os
from pathlib import Path
from dataclasses import dataclass
from typing import List


@dataclass
class AppConfig:
    api_id: int
    api_hash: str
    chats: List[str]
    gpt_model: str = "gpt-3.5-turbo"


def load_config(path: Path | str = "config.json") -> AppConfig:
    path = Path(path)
    with path.open() as f:
        data = json.load(f)

    chats = data.get("chats", [])
    gpt_model = data.get("gpt_model", "gpt-3.5-turbo")

    api_id = os.environ.get("API_ID")
    api_hash = os.environ.get("API_HASH")
    if not api_id or not api_hash:
        raise RuntimeError("API_ID and API_HASH must be set in the environment")

    return AppConfig(api_id=int(api_id), api_hash=api_hash, chats=chats, gpt_model=gpt_model)
