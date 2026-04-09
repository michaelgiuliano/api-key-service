# API Key Service

A backend service for managing users and API keys.

## Features

- User signup and login (JWT authentication)
- Protected routes with bearer token
- SQL database integration (SQLAlchemy)
- Clean service-layer architecture

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite (dev) / PostgreSQL (prod-ready)

## Run locally

```bash
uvicorn app.main:app --reload
```

## API Docs
http://localhost:8000/docs

## Auth

Use:
```
Authorization: Bearer <token>
```

### Example flow:

1. Login via /auth/login
2. Copy access_token
3. Click "Authorize" in Swagger
4. Paste: **`<token>`**

## Project Structure

```
api/        →   routes and dependencies  
core/       →   config and security  
db/         →   database setup  
models/     →   ORM models  
services/   →   business logic 
```