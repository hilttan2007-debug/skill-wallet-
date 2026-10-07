import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")


@lru_cache(maxsize=1)
def get_client():
    from google import genai
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured. Copy .env.example to .env and add your key.")
    return genai.Client(api_key=api_key)


def generate_text(prompt: str, *, system_instruction: str | None = None, temperature: float = 0.4) -> str:
    client = get_client()
    config = {
        "temperature": temperature,
        "max_output_tokens": 2048,
        "system_instruction": system_instruction or (
            "You are EduGenie, a careful educational assistant. "
            "Give accurate, age-appropriate, concise answers. "
            "When unsure, clearly say so rather than inventing facts."
        ),
    }
    response = client.models.generate_content(model=DEFAULT_MODEL, contents=prompt, config=config)
    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned no text response.")
    return text.strip()


def generate_json(prompt: str, schema: dict) -> dict:
    client = get_client()
    response = client.models.generate_content(
        model=DEFAULT_MODEL,
        contents=prompt,
        config={
            "temperature": 0.3,
            "max_output_tokens": 3000,
            "response_mime_type": "application/json",
            "response_schema": schema,
            "system_instruction": (
                "You are EduGenie. Return only valid JSON matching the supplied schema. "
                "Do not include markdown fences or commentary."
            ),
        },
    )
    parsed = getattr(response, "parsed", None)
    if parsed is not None:
        if hasattr(parsed, "model_dump"):
            return parsed.model_dump()
        if isinstance(parsed, dict):
            return parsed
    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned no JSON response.")
    import json
    return json.loads(clean_json_block(text))


def clean_json_block(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return text
