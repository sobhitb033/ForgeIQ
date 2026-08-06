# ForgeIQ

> **AI-powered Software Intelligence Platform that understands software architecture before generating AI insights.**

ForgeIQ is an intelligent software analysis platform designed to act as an **AI Software Architect** rather than a traditional AI coding assistant.

Instead of sending raw source code directly to a Large Language Model (LLM), ForgeIQ first performs comprehensive **static analysis** to understand the architecture, dependencies, complexity, maintainability, and overall quality of an entire software project.

The platform builds a structured understanding of a codebase before AI generates recommendations, enabling architecture-aware software engineering insights.

---

# Vision

Modern software projects often contain hundreds of files and thousands of lines of code. While existing AI coding assistants excel at generating and explaining code, they typically operate on individual files or small code snippets.

ForgeIQ bridges this gap by understanding an **entire software project** before involving AI.

Its goal is to become an **AI Software Architect** capable of reviewing complete projects, detecting design issues, analyzing architecture, identifying technical debt, and providing intelligent engineering recommendations.

---

# Current Features (v0.3.0)

## Authentication

- User Registration
- User Login
- JWT Authentication
- Secure Password Hashing
- Protected API Routes

---

## Project Management

- Upload Python Projects (.zip)
- Automatic ZIP Extraction
- Project Metadata Management

---

## File Discovery

- Recursive Python File Scanner
- Automatic File Filtering
- Project Module Indexing

---

## AST Analysis

ForgeIQ extracts detailed information from every Python file including:

- Imports
- Classes
- Base Classes
- Methods
- Functions
- Parameters
- Decorators
- Async Functions
- Docstrings
- Line Numbers

---

## Software Metrics

For every Python file ForgeIQ calculates:

- Total Lines
- Code Lines
- Blank Lines
- Comment Lines
- Number of Imports
- Number of Classes
- Number of Functions
- Number of Methods

---

## Dependency Analysis

ForgeIQ automatically detects:

- Internal Project Dependencies
- External Library Dependencies
- Module Dependency Graph
- Circular Dependencies
- Orphan Modules
- Most Connected Modules

---

## Complexity Analysis

For every function and method:

- Cyclomatic Complexity
- Risk Classification
- Decision Point Analysis

---

## Maintainability Analysis

For every Python file:

- Maintainability Index
- Maintainability Rating
- Overall Maintainability Score

---

## Project Summary

Generate project-wide statistics including:

- Total Files
- Total Lines
- Total Code Lines
- Total Imports
- Total Classes
- Total Functions
- Total Methods
- Overall Project Health

---

# Current Architecture

```text
                        User
                         │
                         ▼
                 JWT Authentication
                         │
                         ▼
                 Project Upload API
                         │
                         ▼
                  ZIP Extraction
                         │
                         ▼
                Python File Scanner
                         │
                         ▼
                  Module Indexer
                         │
                         ▼
                    AST Parser
                         │
         ┌───────────────┼────────────────┐
         ▼               ▼                ▼
 Metrics Engine   Dependency Analyzer   Complexity Analyzer
         │               │                │
         └───────────────┼────────────────┘
                         ▼
             Maintainability Analyzer
                         │
                         ▼
            Dependency Graph Builder
                         │
                         ▼
                 Graph Analyzer
                         │
                         ▼
                 Project Summary
                         │
                         ▼
               Structured JSON Response
```

---

# Technology Stack

## Backend

- FastAPI
- Python 3
- SQLAlchemy
- Alembic
- MySQL
- Pydantic

---

## Security

- JWT Authentication
- OAuth2
- Passlib
- bcrypt

---

## Static Analysis

- Python AST
- pathlib
- zipfile

---

## Upcoming AI Stack

- Scikit-learn
- NetworkX
- Hugging Face Transformers
- OpenAI API / LLM Integration

---

# Example API Response

```json
{
  "summary": {
    "total_files": 7,
    "total_lines": 79,
    "project_health": "Excellent"
  },
  "dependency_graph": {
    "main": [
      "utils.helper",
      "models.user"
    ]
  },
  "graph_analysis": {
    "most_connected_module": "main",
    "circular_dependencies": []
  },
  "analysis": [
    {
      "file": "main.py",
      "complexity": {
        "cyclomatic_complexity": 2,
        "risk": "Low"
      },
      "maintainability": {
        "index": 88,
        "rating": "Excellent"
      }
    }
  ]
}
```

---

# Project Roadmap

## ✅ v0.1.0 — Foundation

- JWT Authentication
- User Management
- MySQL Integration
- Project Upload
- ZIP Extraction

---

## ✅ v0.2.0 — Static Analysis

- Python File Scanner
- AST Parser
- Software Metrics Engine
- Project Summary

---

## ✅ v0.3.0 — Software Intelligence Core

- Dependency Analysis
- Internal & External Dependency Detection
- Dependency Graph
- Circular Dependency Detection
- Graph Analysis
- Cyclomatic Complexity
- Maintainability Index

---

## 🚧 v0.4.0 — Software Quality

- Code Smell Detection
- Technical Debt Detection
- Quality Score
- Engineering Priority Score

---

## 🚧 v0.5.0 — Architecture Intelligence

- Architecture Detection
- Layer Detection
- Design Pattern Detection
- SOLID Principle Analysis

---

## 🚧 v0.6.0 — AI Insights

- AI Project Summary
- Refactoring Recommendations
- Architecture Explanation
- Risk Assessment
- AI Engineering Chat

---

## 🚧 v1.0.0 — Complete Platform

- React Dashboard
- Interactive Dependency Graph
- Visual Analytics
- PDF Reports
- GitHub Integration
- VS Code Extension
- AI Software Architect

---

# How ForgeIQ Differs

Traditional AI coding assistants follow this workflow:

```text
Source Code
      │
      ▼
Large Language Model
      │
      ▼
Generated Response
```

ForgeIQ follows a software engineering pipeline:

```text
Source Code
      │
      ▼
Python AST
      │
      ▼
Software Metrics
      │
      ▼
Dependency Analysis
      │
      ▼
Complexity Analysis
      │
      ▼
Maintainability Analysis
      │
      ▼
Architecture Understanding
      │
      ▼
Artificial Intelligence
      │
      ▼
Engineering Insights
```

Instead of asking an AI model to understand thousands of lines of raw code, ForgeIQ first transforms the project into structured engineering knowledge. The AI then reasons over that structured understanding to provide more accurate, architecture-aware recommendations.

---

# Running ForgeIQ

```bash
git clone https://github.com/<your-username>/ForgeIQ.git

cd ForgeIQ

python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

Swagger Documentation:

```
http://127.0.0.1:8000/docs
```

---

# Project Status

**Current Version:** **v0.3.0**

**Status:** 🟢 Active Development

ForgeIQ currently includes a complete static analysis engine capable of understanding project structure, dependencies, complexity, maintainability, and software metrics. The next milestone focuses on software quality analysis through code smell detection and architecture intelligence.

---

# Future Vision

The long-term goal of ForgeIQ is to become an AI-powered Software Architect capable of:

- Understanding entire software systems
- Detecting architectural issues
- Explaining codebases
- Measuring software quality
- Prioritizing engineering work
- Assisting developers with intelligent, project-aware recommendations

Rather than replacing developers, ForgeIQ aims to become an engineering companion that understands software the way an experienced software architect would.

---

# License

MIT License