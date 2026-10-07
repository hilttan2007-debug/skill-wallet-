from ai_client import generate_text


def answer_question(question: str) -> str:
    prompt = (
        "Answer this academic/general knowledge question clearly and directly. "
        "If the question is ambiguous, state the assumption you made.\n\n"
        f"Question: {question}"
    )
    return generate_text(prompt, temperature=0.2)
