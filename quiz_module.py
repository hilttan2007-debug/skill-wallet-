from ai_client import generate_json

QUIZ_SCHEMA = {
    "type": "object",
    "properties": {
        "questions": {
            "type": "array",
            "minItems": 3,
            "maxItems": 3,
            "items": {
                "type": "object",
                "properties": {
                    "question": {"type": "string"},
                    "options": {"type": "array", "minItems": 4, "maxItems": 4, "items": {"type": "string"}},
                    "correct_answer": {"type": "string"},
                    "explanation": {"type": "string"},
                },
                "required": ["question", "options", "correct_answer", "explanation"],
            },
        }
    },
    "required": ["questions"],
}


def generate_quiz(source: str) -> dict:
    prompt = f"""Create exactly 3 multiple-choice questions from the following topic or passage.
Each question must have exactly 4 options. The correct_answer must exactly match one option.
Give a short explanation for the correct answer.

SOURCE:
{source}
"""
    data = generate_json(prompt, QUIZ_SCHEMA)
    questions = data.get("questions", [])
    if len(questions) != 3:
        raise ValueError("The model did not return exactly 3 quiz questions.")
    for q in questions:
        if len(q.get("options", [])) != 4 or q["correct_answer"] not in q["options"]:
            raise ValueError("Invalid quiz structure returned by the model.")
    return data
