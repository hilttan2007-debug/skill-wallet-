from ai_client import generate_text


def summarize_text(text: str) -> str:
    prompt = (
        "Summarize the following educational text for quick revision. "
        "Keep the key facts, definitions, and relationships. Use short bullet points when helpful.\n\n"
        f"TEXT:\n{text}"
    )
    return generate_text(prompt, temperature=0.2)
