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

MIT License