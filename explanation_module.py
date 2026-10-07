import os
from functools import lru_cache

from ai_client import generate_text

LOCAL_MODEL = os.getenv("LOCAL_EXPLANATION_MODEL", "MBZUAI/LaMini-Flan-T5-783M")
USE_LOCAL = os.getenv("USE_LOCAL_EXPLANATION", "false").lower() == "true"


@lru_cache(maxsize=1)
def _load_local_model():
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(LOCAL_MODEL)
    model = AutoModelForSeq2SeqLM.from_pretrained(LOCAL_MODEL)
    return tokenizer, model


def explain_topic(topic: str) -> str:
    prompt = (
        f"Explain the following educational topic for a beginner: {topic}\n"
        "Use simple language, short paragraphs, and one small example when useful."
    )
    if USE_LOCAL:
        try:
            tokenizer, model = _load_local_model()
            inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
            outputs = model.generate(**inputs, max_new_tokens=180, num_beams=4)
            return tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
        except Exception:
            # Gemini remains the reliable cloud fallback if local model loading fails.
            pass
    return generate_text(prompt, temperature=0.3)
