"""GPT processing utilities."""

from __future__ import annotations

import json
import os
from typing import Any

import openai

PROMPT_TEMPLATE = """You are a sales assistant helping identify leads in public Telegram chats.

- Determine if it's a standalone message or part of a thread
- Evaluate how relevant the message is to our offers

Your job is to detect if the message clearly relates to our business offerings.
Ignore spam, code, jokes, news, or other irrelevant content.
Do not assume intent without clear signals that user who sent message is looking for something that our company may potentially offer.
If it is something that we can offer, but don't have in the listing, it shoud be still considered as relevant

------

We offer rental properties all over the Bali, current product listings:
1. 4-bedroom, 3-bathroom luxury villa in Canggu, Bali. 400m² building on 270m² land, spread over 3 floors. Monthly rent IDR 80M (~USD 5,000). Includes private pool (54m²), garage (48m²), steam room, ice bath, and cinema room. Fully furnished, quiet location near cafes and beach. Ready to move in.


Your output must be in JSON with the following fields:
- message_type: single message / part of thread
- relevance: perfect match / relevant, need ask more info / relevant, no product match / irrelevant
- explanation: concise description of why this relevance classification was chosen (be extra concise if it is irrelevant message)
- suggested_next_step: concise suggestion of what to do next with this lead (put NFA if irrelevant)

Example 1
Message: "Looking for a villa in Canggu, 3-4 bedrooms, monthly rent under 90 million. Prefer near cafes."
Expected output:
{
"message_type": "single message",
"relevance": "perfect match",
"explanation": "User specifies location (Canggu), bedroom count (3-4), and budget (under 90M), all matching our listed villa.",
"suggested_next_step": "Offer product 1 and include key features like pool and proximity to cafes."
}

Example 2
Message: "Looking for a place near Ubud for a couple weeks. Budget 50M."
Expected output:
{
"message_type": "single message",
"relevance": "relevant, no product match",
"explanation": "User is looking to rent in Bali, but location (Ubud) and budget (50M) do not match our Canggu listing.",
"suggested_next_step": "Mention we only have a villa in Canggu currently and ask if location flexibility is possible."
}

Example 3
Message: "Yes, we’re still looking. Ideally something furnished with a pool in Canggu."
Expected output:
{
"message_type": "part of thread",
"relevance": "perfect match",
"explanation": "Message confirms interest in Canggu, furnished rental, with pool. All aspects match our offering.",
"suggested_next_step": "Offer product 1 and highlight it's fully furnished with a private pool."
}

Example 4
Message: Anyone knows where to buy good surfboards in Bali?
Expected output:
{
"message_type": "single message",
"relevance": "irrelevant",
"explanation": "Topic is about surfboards, not housing or rentals.",
"suggested_next_step": "NFA"
}

The actual message I want you to analyze is below
--------- Message Start ---------
{{1.message.text}}
--------- Message End ---------
"""


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
    prompt = PROMPT_TEMPLATE.replace("{{1.message.text}}", text)
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
