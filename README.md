# Tech Trend Tracker

A full-stack application that tracks technology trends from news articles.

## Overview

Tech Trend Tracker collects articles from Reuters, processes them with OpenAI embeddings, and displays monthly technology trends and keyword rankings. This app also includes RAG-enhanced semantic search and AI-powered article summaries. The demo uses data from 2024/01 to 2024/12.

## Features

- RAG-enhanced search:
  - Text chunking & embeddings
  - AI-powered summaries
  - Referenced sources with scores
- Keyword-based article search
- Trending entity analysis (companies, people, services)
- Keyword frequency tracking

## Tech Stack

- Frontend: Next.js, Tailwind CSS, shadcn/ui
- Backend: Python, FastAPI
- Database: PostgreSQL with pgvector
- AI models: OpenAI (embeddings, text generation)

## Architecture

```mermaid
  graph TB
      subgraph "Offline Scripts"
          SCRIPTS[Data Collection<br/>& Embedding Scripts]
          BD[Bright Data API]
      end

      subgraph "Database"
          VEC[(Vector Database<br/>pgvector)]
          META[(Article Metadata<br/>PostgreSQL)]
      end

      subgraph "Backend (FastAPI)"
          API[REST API]
          RAG[RAG Pipeline]
          LLM[OpenAI LLM]
      end

      subgraph "Frontend (Next.js)"
          UI[Search Interface]
          DASH[Trend Dashboard]
          CHAT[AI Chat]
      end

      BD -->|Articles| SCRIPTS
      SCRIPTS -->|Store| META
      SCRIPTS -->|Embeddings| VEC

      UI --> API
      DASH --> API
      CHAT --> API

      API --> RAG
      RAG <-->|Search| VEC
      RAG -->|Query| META
      RAG -->|Generate| LLM
```

## Screenshot

![Dashboard](./screenshot1.png)
![Search](./screenshot2.png)

## Local Setup

1. Clone the repository:

```bash
git clone git@github.com:yukaty/tech-trend-tracker.git
cd tech-trend-tracker
```

2. Configure environment variables:

```bash
cp .env.example .env
```

3. Start backend services:

```bash
docker compose up --build
```

4. Run frontend development server:

```bash
cd frontend
npm install
npm run dev
```

- http://localhost:3000 for the web interface
- http://localhost:8000/docs for the API documentation

## Future Plans

- Additional data sources (RSS feeds, APIs)
- Enhanced search accuracy
- Advanced visualizations
- Performance optimization

## License

MIT License

_Feel free to open issues and pull requests. All feedback and contributions are welcome!_
