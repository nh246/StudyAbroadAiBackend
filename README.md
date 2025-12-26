# StudyAbroadAi Backend
# StudyAbroadAi Frontend Repo : https://github.com/nh246/Studyabroadai

FastAPI backend using **GitHub Models o4-mini** and **Tavily Search** for AI-powered study abroad consultation.

## 🚀 Tech Stack

- FastAPI
- GitHub Models (o4-mini)
- Tavily Search API
- LangChain
- Python 3.10+

## 📋 Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Add your API keys:
- **GITHUB_TOKEN**: https://github.com/settings/tokens
- **TAVILY_API_KEY**: https://tavily.com

### 3. Run Locally

```bash
uvicorn main:app --reload
```

API: http://localhost:8000
Docs: http://localhost:8000/docs

## 🌐 Deploy to Cloudflare Workers

See [DEPLOYMENT.md](DEPLOYMENT.md)

## 📖 API Endpoints

### `POST /profile/submit`
Submit user profile

### `POST /chat/ask`
Chat with AI (requires user_id)

### `GET /profile/get/{user_id}`
Get user profile

### `GET /health`
Health check

## 📁 Structure

```
app/
├── main.py              # FastAPI app
├── api/v1/endpoints/    # API routes
├── services/            # Business logic
│   ├── chat_service.py  # GitHub Models
│   └── search_service.py # Tavily search
├── schemas/             # Pydantic models
└── core/                # Config
```

## 📄 License

MIT
