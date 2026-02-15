# SQL Agent – Agentic SQL Enterprise Assistant

A full-stack **natural language to SQL** application with an AI agent (Claude via AWS Bedrock), orchestration layer, and React frontend. Users can ask questions in plain English and get executed queries, result tables, and charts.

## Architecture

- **Client** (React + Vite) – Chat UI, result tables, charts
- **Orchestrator** (Node.js/Express) – Auth, session management, job queue (BullMQ + Redis), proxies to agent
- **Agent** (Python/FastAPI) – LangGraph pipeline: plan → generate SQL → validate → execute → self-heal; uses ChromaDB for schema context
- **Database** – PostgreSQL (schema + seed data), Redis, ChromaDB

## Prerequisites

- Docker & Docker Compose
- AWS account (Bedrock access for Claude)
- Node.js 18+ and Python 3.11+ (for local dev without Docker)

## Quick Start (Docker)

1. **Clone and enter the repo**
   ```bash
   git clone https://github.com/YOUR_USERNAME/sql-agent.git
   cd sql-agent
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env: set AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION, MODEL_ID, and JWT_SECRET
   ```

3. **Run everything**
   ```bash
   docker-compose up --build
   ```

4. **Open the app**
   - Frontend: http://localhost:5173  
   - Orchestrator API: http://localhost:3000  

## Environment Variables

See `.env.example`. Key variables:

- **AWS Bedrock**: `AWS_ACCESS_KEY`, `AWS_SECRET_KEY`, `AWS_REGION`, `MODEL_ID`
- **PostgreSQL**: `PG_*` (defaults work with Docker)
- **Orchestrator**: `JWT_SECRET` (set a strong value in production)
- **Client (build-time)**: `VITE_API_URL` – set to your deployed API URL for production builds

## Project Structure

```
├── client/          # React frontend
├── orchestrator/    # Node.js API & job queue
├── agent/           # Python FastAPI + LangGraph agent
├── database/        # PostgreSQL schema & seed
├── docker-compose.yml
└── .env.example
```

## Hosting / Deployment

- **Option A – All-in-one (e.g. Railway, Render)**  
  Deploy with Docker Compose or multiple services: run Postgres, Redis, ChromaDB, agent, orchestrator, and serve the client build (e.g. from the orchestrator or a static host).

- **Option B – Split**  
  - **Frontend**: Vercel or Netlify (build `client` with `VITE_API_URL` set to your API).  
  - **Backend**: Railway or Render (orchestrator + agent + Postgres, Redis, ChromaDB).

For resume/demo, pushing this repo to GitHub and adding a **live demo** link (from whichever hosting you choose) is recommended.

## License

MIT
