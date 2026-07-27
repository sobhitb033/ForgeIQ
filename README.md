# ForgeIQ

AI-powered software intelligence platform that analyzes software projects using Static Analysis, Machine Learning, and Large Language Models.

---

## Features

- User Authentication (JWT)
- Secure Password Hashing
- MySQL Database
- SQLAlchemy ORM
- Alembic Database Migrations
- FastAPI REST API
- Swagger Documentation

---

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- Alembic
- MySQL
- Pydantic

### Authentication
- JWT
- Passlib
- bcrypt

### AI (Upcoming)
- Python AST
- NetworkX
- Scikit-learn
- Transformers
- LLM Integration

---

## Project Structure

```text
ForgeIQ/
│
├── alembic/
├── app/
│   ├── api/
│   ├── core/
│   ├── database/
│   ├── dependencies/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── main.py
│
├── docs/
├── uploads/
├── reports/
├── tests/
├── requirements.txt
└── README.md
```

---

## Completed

- User Registration
- User Login
- JWT Authentication
- Database Migrations
- MySQL Integration

---

## Upcoming

- Protected Routes
- Project Upload
- Static Code Analysis
- Dependency Graph
- Engineering Priority Score
- AI Code Review
- Report Generation
- Dashboard

---

## Run

```bash
git clone <repo-url>

cd ForgeIQ

python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

---

MIT Licens# ForgeIQ

> **An AI-powered Software Analysis Platform that understands software architecture before generating AI insights.**

ForgeIQ is an intelligent software analysis platform designed to act as an **AI Software Architect** rather than a traditional AI chatbot. Instead of sending raw source code directly to a Large Language Model (LLM), ForgeIQ first performs comprehensive static analysis to understand the structure, architecture, and quality of an entire software project.

The platform extracts project-level knowledge such as classes, functions, imports, dependencies, and software metrics, creating a structured understanding of the codebase before AI generates insights.

---

# Vision

Modern software projects contain hundreds of files and thousands of lines of code, making them increasingly difficult to understand and maintain.

Existing AI coding assistants are excellent at generating and explaining code but primarily operate on individual files or small snippets.

ForgeIQ aims to bridge this gap by understanding the **entire project** before involving AI, enabling architecture-aware recommendations, project summaries, dependency analysis, and software quality insights.

---

# Current Features (v0.1.0)

## Authentication

- User Registration
- User Login
- JWT Authentication
- Secure Password Hashing

---

## Project Management

- Upload Python Projects (.zip)
- Automatic ZIP Extraction
- Project Metadata Management

---

## File Analysis

- Recursive Python File Discovery
- Automatic File Filtering
- Python AST Parsing

---

## AST Analysis

ForgeIQ currently extracts:

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

## Project Summary

Generate project-level statistics including:

- Total Files
- Total Lines
- Total Code Lines
- Total Imports
- Total Classes
- Total Functions
- Total Methods

---

# Current Architecture

```text
                    User Upload
                         │
                         ▼
                 Authentication
                         │
                         ▼
                   Upload Service
                         │
                         ▼
                  ZIP Extraction
                         │
                         ▼
                  Python File Scanner
                         │
                         ▼
                    AST Parser
                         │
                         ▼
                  Metrics Engine
                         │
                         ▼
                 Project Summary
                         │
                         ▼
                 Structured JSON API
```

---

# Technology Stack

### Backend

- FastAPI
- Python 3
- SQLAlchemy
- Alembic
- MySQL

### Security

- JWT Authentication
- OAuth2
- Password Hashing

### Static Analysis

- Python AST
- pathlib
- zipfile

---

# Example Response

```json
{
  "project": {
    "project_name": "Sample"
  },
  "summary": {
    "total_files": 4,
    "total_lines": 75,
    "total_classes": 2,
    "total_functions": 10
  },
  "analysis": [
    {
      "file": "models/user.py",
      "metrics": {
        "code_lines": 16
      }
    }
  ]
}
```

---

# Roadmap

## v0.1.0 ✅ Static Analysis Foundation

- JWT Authentication
- Project Upload
- ZIP Extraction
- AST Parser
- Metrics Engine
- Project Summary

---

## v0.2.0 🚧 Dependency Analysis

- Internal Module Graph
- External Dependency Detection
- Circular Import Detection
- Dependency Visualization

---

## v0.3.0 🚧 Complexity Analysis

- Cyclomatic Complexity
- Maintainability Metrics
- Function Complexity
- Class Complexity

---

## v0.4.0 🚧 Software Quality

- Code Smell Detection
- SOLID Principle Analysis
- Architecture Analysis
- Technical Debt Detection

---

## v0.5.0 🚧 AI Insights

- Project Understanding
- AI Project Summary
- Refactoring Recommendations
- Software Architecture Explanation
- Risk Analysis

---

## v1.0.0 🚧 Complete Platform

- React Dashboard
- Interactive Dependency Graphs
- GitHub Integration
- VS Code Extension
- AI Software Architect

---

# How ForgeIQ Differs

Traditional AI coding assistants typically follow this workflow:

```
Source Code
     │
     ▼
Large Language Model
     │
     ▼
Generated Response
```

ForgeIQ follows a software engineering pipeline:

```
Source Code
     │
     ▼
Static Analysis
     │
     ▼
AST Parsing
     │
     ▼
Software Metrics
     │
     ▼
Project Understanding
     │
     ▼
Dependency Analysis
     │
     ▼
Architecture Analysis
     │
     ▼
Artificial Intelligence
     │
     ▼
Engineering Insights
```

This enables AI to generate recommendations based on a structured understanding of the software rather than only the raw source code.

---

# Project Status

**Current Version:** `v0.1.0`

**Status:** 🟢 Active Development

Milestone 1 has been completed successfully. The project currently focuses on building a robust static analysis engine, which will serve as the foundation for dependency analysis, software quality assessment, and AI-powered engineering insights.

---

# License

This project is currently under development and is intended for educational and research purposes.e