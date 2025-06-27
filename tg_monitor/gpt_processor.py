"""Stub GPT processing utilities."""

from typing import Any

# In a real implementation this would call an LLM API like OpenAI's ChatGPT.
# For now we return a dummy JSON object based on the message text.
async def process_text_with_gpt(text: str) -> dict[str, Any]:
    """Process text with GPT and return structured JSON.

    The prompt and API call are omitted in this stub implementation.
    """
    # TODO: Replace with actual API call
    return {"summary": text[:30]}
