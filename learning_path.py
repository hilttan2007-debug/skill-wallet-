from ai_client import generate_text


def get_learning_recommendations(topic: str) -> str:
    prompt = f"""Create a personalized learning path for: {topic}

Organize it from beginner to advanced. Include:
1. Prerequisites
2. Beginner concepts
3. Intermediate concepts
4. Advanced concepts
5. A practical mini-project or activity
6. Suggested learning resources by type (videos, articles, books, documentation)
7. A simple suggested timeline

Keep the plan realistic and easy to follow. Do not invent specific URLs unless you are certain they are official resources.
"""
    return generate_text(prompt, temperature=0.4)
