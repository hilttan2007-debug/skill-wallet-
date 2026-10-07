# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight FastAPI + HTML/CSS/JavaScript learning assistant based on the supplied project documentation. It provides:

- Q&A through Gemini
- Simple concept explanations
- 3-question, 4-option MCQ quizzes with answer feedback
- Educational text summarization
- Beginner-to-advanced learning paths
- A responsive browser interface
- REST endpoints for every module

The original document specifies Gemini 1.5 Pro and LaMini-Flan-T5-783M. The implementation keeps the same architecture and module responsibilities, but uses Google's current `google-genai` SDK and a configurable Gemini model so the project is not tied to the older SDK. Google currently documents `google-genai` and `client.models.generate_content(...)` for Python. See the official docs linked below.

## Project structure

```text
EduGenie/
├── main.py
├── ai_client.py
├── explanation_module.py
├── qna.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
├── static/
│   ├── app.js
│   └── style.css
└── tests/
    └── test_app.py
```

## Requirements

- Python 3.10+
- A Gemini API key
- Internet access for Gemini API calls
- VS Code recommended

## VS Code setup

1. Extract/open the `EduGenie` folder in VS Code.
2. Open the integrated terminal.
3. Create a virtual environment:

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:

```bat
.venv\Scripts\activate
```

4. Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

5. Copy `.env.example` to `.env` and put your Gemini API key in `GEMINI_API_KEY`.

6. Start the application:

```bash
uvicorn main:app --reload
```

7. Open `http://127.0.0.1:8000` in your browser.

FastAPI's API documentation is also available at `http://127.0.0.1:8000/docs`.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Web application |
| GET | `/health` | Health check |
| POST | `/qa` | Answer a question |
| POST | `/explain` | Explain a topic |
| POST | `/quiz` | Generate exactly 3 MCQs |
| POST | `/summarize` | Summarize educational text |
| POST | `/learn/recommendations` | Generate a learning path |

POST body for text endpoints:

```json
{"text":"Explain photosynthesis in simple words."}
```

Quiz response shape:

```json
{
  "questions": [
    {
      "question": "...",
      "options": ["...", "...", "...", "..."],
      "correct_answer": "...",
      "explanation": "..."
    }
  ]
}
```

## Testing

Install pytest if needed:

```bash
pip install pytest
```

Run:

```bash
pytest -q
```

The included tests verify the app routes and frontend serving without making live Gemini calls.

For a live AI test, start the server and use the browser or Swagger UI. A successful `/health` response should be:

```json
{"status":"ok","service":"EduGenie"}
```

## Optional local LaMini model

The project documentation describes LaMini-Flan-T5-783M for concept explanations. To enable that path:

```bash
pip install transformers torch
```

Then set:

```env
USE_LOCAL_EXPLANATION=true
LOCAL_EXPLANATION_MODEL=MBZUAI/LaMini-Flan-T5-783M
```

The first local-model request downloads the model. If local loading fails, EduGenie falls back to Gemini so the application remains usable.

## Security notes

- Never commit `.env` or your API key.
- Keep the Gemini API key on the backend; the browser never receives it.
- The project limits normal text requests to 20,000 characters.
- AI output should still be checked before being used as authoritative educational material.
