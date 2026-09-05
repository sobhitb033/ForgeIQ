# ForgeIQ

## AI Software Architect for Codebase Analysis

ForgeIQ is a full-stack platform that analyzes Python projects and turns
source code into **architectural, dependency, quality, health, impact,
and engineering insights**.

Instead of sending raw code directly to an AI, ForgeIQ first builds a
structured understanding of the project through static analysis and then
uses that context for AI-powered architectural guidance.

### What ForgeIQ does

-   🔐 User authentication with JWT and Google login
-   📦 Upload Python projects as ZIP files
-   🌳 Parse Python code using AST
-   📊 Calculate code and maintainability metrics
-   🧹 Detect code smells
-   🔗 Analyze internal and external dependencies
-   🕸️ Build and analyze dependency graphs
-   🔄 Detect circular dependencies
-   🎯 Calculate module impact and change blast radius
-   🏗️ Infer project architecture
-   ❤️ Calculate project health
-   🚨 Rank engineering priorities and recommendations
-   🤖 Ask the AI Architect questions about the analyzed codebase
-   💬 Continue conversations and focus questions on specific files or
    recommendations
-   💾 Store project history and analysis results in MySQL

### Analysis pipeline

``` text
Python Project
      ↓
AST + Static Analysis
      ↓
Metrics + Code Smells
      ↓
Dependencies + Dependency Graph
      ↓
Impact + Architecture Analysis
      ↓
Project Health + Recommendations
      ↓
Structured Project Context
      ↓
AI Architect
```

## Tech Stack

**Backend:** Python 3.12, FastAPI, SQLAlchemy, MySQL 8, Pydantic, JWT

**Frontend:** React, Vite, JavaScript, CSS

**Infrastructure:** Docker, Docker Compose

**AI:** Gemini through an OpenAI-compatible API

## Run ForgeIQ Locally

### Prerequisites

Install **Git** and **Docker Desktop**.

### 1. Clone the repository

``` bash
git clone <your-repository-url>
cd ForgeIQ
```

### 2. Configure the environment

Configure the backend environment file used by Docker:

``` text
.env.docker
```

To enable the AI Architect, add:

``` env
AI_ENABLED=true
AI_API_KEY=your_gemini_api_key
AI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai
AI_MODEL=your_gemini_model
```

**Never commit real API keys, passwords, or JWT secrets to Git.**

### 3. Start ForgeIQ

``` bash
docker compose up -d --build
```

Check the services:

``` bash
docker compose ps
```

### 4. Open the application

-   Frontend: `http://localhost:5173`
-   Backend: `http://localhost:8000`
-   Swagger: `http://localhost:8000/docs`
-   Health check: `http://localhost:8000/health`

Create an account, log in, upload a Python ZIP project, and ForgeIQ will
analyze it.

### Stop ForgeIQ

``` bash
docker compose down
```

To also remove the local MySQL data:

``` bash
docker compose down -v
```

> `docker compose down -v` deletes the Docker MySQL volume and its
> stored data.

## Future Plans

-   🌐 Multi-language support for Java, C++, JavaScript, TypeScript, Go,
    and more
-   🧠 Advanced AST and code-flow analysis
-   🕸️ Richer dependency and knowledge-graph intelligence
-   🏗️ Architecture drift and layer-violation detection
-   🧪 Deeper code-quality and testing analysis
-   🐙 Direct GitHub repository analysis
-   ⚙️ CI/CD and pull-request analysis
-   📄 Automated architecture and engineering reports
-   🤖 More advanced AI-assisted refactoring and migration planning

## Vision

> **ForgeIQ turns source code into an understanding of the software
> system --- and helps engineers decide what to do next.**
