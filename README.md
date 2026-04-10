# API Key Service

A backend service for managing users and API keys.

## Features

- User signup and login (JWT authentication)
- Protected routes with bearer token
- API key management:
  - Create API keys (returned once)
  - List API keys
  - Revoke API keys
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

## API Keys

### Create API key

```
POST /api-keys
```

- Returns:
  - API key metadata
  - Full API key (shown only once)

### List API keys

```
GET /api-keys
```

- Returns all keys (without secrets)

### Revoke API key

```
DELETE /api-keys/{id}
```

- Soft delete (key becomes inactive)

## Project Structure

```
api/        →   routes and dependencies  
core/       →   config and security  
db/         →   database setup  
models/     →   ORM models  
services/   →   business logic 
```

## Notes

- API keys are stored securely using hashing (bcrypt)
- Full API keys are never stored and cannot be retrieved after creation
- Current version focuses on core functionality; authentication via API keys will be introduced in the next version