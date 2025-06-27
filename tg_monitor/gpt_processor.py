"""GPT processing utilities."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import openai

DEFAULT_PROMPT_FILE = Path(__file__).with_name("gpt_prompt.txt")
PROMPT_FILE = Path(os.environ.get("GPT_PROMPT_FILE", DEFAULT_PROMPT_FILE))

_prompt_cache: str | None = None


def _load_prompt() -> str:
    global _prompt_cache
    if _prompt_cache is None:
        with PROMPT_FILE.open(encoding="utf-8") as f:
            _prompt_cache = f.read()
    return _prompt_cache


_client: openai.AsyncOpenAI | None = None


def _get_client() -> openai.AsyncOpenAI:
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is not set")
    global _client
    if _client is None:
        _client = openai.AsyncOpenAI(api_key=key)
    return _client


async def process_text_with_gpt(text: str) -> dict[str, Any]:
    """Process text with GPT and return structured JSON."""

    client = _get_client()
    prompt = _load_prompt().replace("{{text}}", text)
    try:
        resp = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        content = resp.choices[0].message.content
        return json.loads(content)
    except json.JSONDecodeError:
        return {"error": "invalid_json"}
    except Exception as exc:  # pragma: no cover - runtime errors
        return {"error": str(exc)}
