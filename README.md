# AI-Powered CRM Assistant

A full-stack portfolio project that combines CRM workflows with an AI assistant. Users can manage leads/clients, store notes, track status, and generate AI-supported summaries and follow-up messages.

## Tech Stack

**Frontend:** React, TypeScript, Vite, CSS

**Backend:** Python, FastAPI, SQLAlchemy, SQLite, REST APIs

**AI:** OpenAI API integration with a safe local fallback when no API key is available

**Deployment-ready:** Frontend can be deployed to Vercel; backend can be deployed to Render/Railway

## Features

- User registration and login
- Client/lead management
- Client status and priority tracking
- Notes for each client
- AI summary generation for client history
- AI follow-up message generation
- REST API architecture
- Local SQLite database
- Clean README for GitHub portfolio presentation

## Project Architecture

```text
ai-powered-crm-assistant/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app and routes
│   │   ├── models.py        # SQLAlchemy database models
│   │   ├── schemas.py       # Pydantic request/response schemas
│   │   ├── database.py      # DB connection and session
│   │   ├── auth.py          # Password hashing and token helpers
│   │   └── ai_service.py    # AI assistant logic
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── App.tsx          # Main React app
    │   ├── api.ts           # API client
    │   ├── main.tsx
    │   └── style.css
    ├── package.json
    └── vite.config.ts
```

## API Overview

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/auth/register` | Create a user account |
| POST | `/auth/login` | Log in and receive access token |
| GET | `/clients` | List user clients |
| POST | `/clients` | Create a new client |
| PUT | `/clients/{id}` | Update client data |
| DELETE | `/clients/{id}` | Delete a client |
| GET | `/clients/{id}/notes` | List notes for a client |
| POST | `/clients/{id}/notes` | Add a note |
| POST | `/ai/client-summary/{id}` | Generate client summary |
| POST | `/ai/follow-up/{id}` | Generate follow-up message |

## How to Run Locally

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend runs on: `http://localhost:8000`

### Optional AI Key

Create a `.env` file inside `backend/`:

```env
OPENAI_API_KEY=your_key_here
```

If no key is provided, the app uses a local fallback response so the demo still works.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on: `http://localhost:5173`

## Suggested CV Bullet

**AI-Powered CRM Assistant — Personal Full-Stack Project**  
*React, TypeScript, Python FastAPI, REST APIs, SQLite, OpenAI API, Vercel/Render-ready*

- Built a full-stack CRM dashboard with authentication, client management, notes, lead status tracking, and API-connected user workflows.
- Integrated an AI assistant to summarize client history and generate follow-up messages using CRM data and LLM API logic.
- Designed REST API endpoints for authentication, client records, notes, and AI requests with structured backend logic and database-driven workflows.
- Prepared the project for GitHub portfolio presentation with architecture documentation, setup instructions, and deployment-ready structure.

## Next Improvements

- Add JWT authentication instead of simple demo tokens
- Add role-based access control
- Add PostgreSQL for production deployment
- Add automated tests with Pytest and Playwright
- Add CI/CD workflow with GitHub Actions
