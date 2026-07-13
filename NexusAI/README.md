# NexusAI

An AI-powered student success platform — one place for chat guidance, coding help,
study planning, resume feedback, and PDF Q&A. Five agents, one backend, one frontend.

```
backend/   Flask API — 5 agent route/service pairs, SQLAlchemy models, OpenAI/Anthropic switch
frontend/  React + Vite + Tailwind — dashboard + one page per agent
```

## 1. Local setup

**Requirements:** Python 3.10+, Node 18+.

### Windows (automated)
```powershell
.\setup.ps1
```

### Manual (macOS/Linux/Windows)
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # then fill in your API key(s)
python app.py                   # runs on http://localhost:5000

# Frontend (separate terminal)
cd frontend
npm install
cp .env.example .env            # VITE_API_URL=http://localhost:5000
npm run dev                     # runs on http://localhost:5173
```

Open `http://localhost:5173`. The backend defaults to a local SQLite file
(`backend/nexus_ai.db`) — no database setup needed for local dev.

## 2. Configuring the AI provider

Both OpenAI and Anthropic are wired in. Set `AI_PROVIDER` in `backend/.env` to
whichever you want as the default, and fill in the matching key:

```env
AI_PROVIDER=openai          # or "anthropic"
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-sonnet-5
```

You only need to fill in the key for the provider you're actually using.
Every request can also override the provider per-call (see `services/ai_service.py`),
so you can run both side by side if you want to compare.

## 3. Deploying — Render (backend) + Vercel (frontend)

### Backend → Render
1. Push this repo to GitHub.
2. On Render: **New → Blueprint**, point it at the repo. It will read `render.yaml`
   and provision a web service + a free Postgres database automatically.
   (No `render.yaml`? Create a **Web Service** manually with root directory `backend`,
   build command `pip install -r requirements.txt`, start command
   `gunicorn app:app --bind 0.0.0.0:$PORT`.)
3. In the service's **Environment** tab, set:
   - `OPENAI_API_KEY` and/or `ANTHROPIC_API_KEY`
   - `AI_PROVIDER` (`openai` or `anthropic`)
   - `CORS_ORIGINS` — set this **after** step 4, once you have your Vercel URL
     (e.g. `https://nexus-ai.vercel.app`)
4. Deploy. Note the resulting backend URL, e.g. `https://nexus-ai-backend.onrender.com`.

### Frontend → Vercel
1. Import the repo on Vercel, set the **root directory** to `frontend`.
2. Framework preset: Vite. Build command `npm run build`, output directory `dist`
   (Vercel auto-detects these).
3. Add environment variable `VITE_API_URL` = your Render backend URL from above.
4. Deploy. Then go back to Render and set `CORS_ORIGINS` to your Vercel URL so the
   backend accepts requests from it.

### Notes
- Render's free tier spins down on inactivity — the first request after idle will
  be slow (~30-60s cold start). Fine for a demo, worth a paid tier before real users.
- SQLite doesn't persist reliably on Render's ephemeral filesystem — the Blueprint
  provisions a real Postgres database and points `DATABASE_URL` at it automatically.
- Uploaded resumes/PDFs are deleted from disk immediately after processing; only
  the extracted text and AI feedback are stored in the database.

## 4. Project structure reference

| Path | Purpose |
|---|---|
| `backend/database/models.py` | User, Conversation, Message, StudyPlan, ResumeReview, PDFDocument |
| `backend/services/ai_service.py` | Single point of contact with OpenAI/Anthropic — everything else calls this |
| `backend/prompts/system_prompts.py` | The persona/instructions for each of the 5 agents |
| `backend/routes/*.py` | One Flask blueprint per agent, thin — just request/response handling |
| `backend/services/*.py` | Business logic per agent — builds prompts, calls ai_service, persists to DB |
| `frontend/src/pages/*.jsx` | One page per agent, all built on the shared `ChatWindow` component where applicable |
| `frontend/src/services/api.js` | Every backend call the frontend makes, in one file |

## 5. What's intentionally minimal (v1)

This is a working MVP, not a production-hardened app. Before real users, you'll
want: real authentication (currently `user_id` is an optional, unauthenticated
field), rate limiting on AI endpoints, and moving off Render's free tier /
SQLite-adjacent constraints. See the in-chat product review for a fuller list.
