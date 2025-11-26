# WEC Backend Technical Challenge
Short description: A minimal REST API that authenticates a predefined user with JWT and allows storing and querying numbers associated with that user.

This API was made with the purpose of applying to a backend developer role at WEC.

## Table of contents
- [Project status](#project-status)  
- [Tech stack](#tech-stack)  
- [Prerequisites](#prerequisites)  
- [Installation & run (local)](#installation--run-local)  
- [Environment variables](#environment-variables)  
- [API: Authentication & Endpoints](#api-authentication--endpoints)  
- [Optional features implemented](#optional-features-implemented)  
- [Submission checklist](#submission-checklist)  
- [Contact](#contact)

---

## Project status
- **Status:** `Complete (As for the requirements)`  
- **Run port:** `8080` (required by the challenge)  
- **Predefined user:** `user: admin / password: 1234` (see Authentication section)

---

## Tech stack
- **Language / Framework:** `Python 3.13.6` + `FastAPI`
- **DB:** `TinyDB`
- **Auth:** JWT (access token expiry: 15 minutes)  
- **Docs:** OpenAPI (Swagger UI) available at `/docs`

---

## Prerequisites
- Python 3.10+  
- Docker
- `pip install -r requirements.txt`

---

## Installation & run (local)

1. Clone:
```bash
git clone https://github.com/SrZafkiell/wec-backend-technical-challenge
cd wec-backend-technical-challenge
```

2. Create `.env` (see [Environment variables](#environment-variables)).

3. Install:
```bash
Step 1: 
python -m venv .venv

Step 2:
# mac/linux
source .venv/bin/activate
# windows (powershell)
.venv\Scripts\Activate.ps1

Step 3:
pip install -r requirements.txt
```

4. Run:
```bash
python -m src.main
```

5. API docs:
**Swagger UI**: `http://localhost:8080/docs`  

---

## Environment variables (example `.env`)
**Note**: Inside the repository you will find a `.env.example` that you can rename and use.
```
JWT_SECRET=change_this_secret
JWT_EXPIRE_MINUTES=15
TINYDB_PATH=data/db.json
```

---

## API — Authentication & Endpoints

### Authentication
**Fixed user**
```json
{
  "username": "admin",
  "password": "1234"
}
```

**Login**
- `POST /login`
- Body:
```json
{ "username": "admin", "password": "1234" }
```
- Success response:
```json
{ "access_token": "<jwt_token>", "token_type": "bearer" }
```
- Token expiry: 15 minutes.

Protect other endpoints using `Authorization: Bearer <token>`.

---

### Endpoints summary
| Method | Endpoint | Permission | Description |
|--------|----------|------------|-------------|
| POST |`'/numbers'`|`'numbers:'`| Create a number |
| GET |`'/numbers'`|`'numbers:'`| List all numbers |
| GET |`'/numbers'`|`'numbers:'`| Get statistics |
| GET |`'/numbers'`|`'numbers:'`| Get specific number |
| GET |`'/numbers'`|`'numbers:'`| Update a number |
| GET |`'/numbers'`|`'numbers:'`| Delete a number |
| GET | `/stats` | `numbers:read` | Get user stats (count, avg, max, min) |
| POST | `/login` | - | Get JWT token |
| POST | `/logout` | - | (optional: blacklist token) |

---

## Optional features
- [x] Global error middleware (recommended) — describe file path.
- [x] Data validation (e.g., number > 0).
- [x] Roles or custom claims in JWT.
- [ ] Dockerfile and docker-compose.
- [x] DELETE /numbers/{id}, PUT /numbers/{id}, GET /numbers/{id}.
- [x] `/stats` endpoint with `count`, `avg`, `max`, `min`.
- [x] `/logout` with token invalidation.

---
## Submission checklist
- [x] App listens on port `8080`.  
- [x] Predefined user `admin:1234` works.  
- [x] JWT tokens expire in 15 minutes.  
- [x] `POST /numbers` & `GET /numbers` implemented.  
- [x] README completed with run instructions and examples.  
- [x] Swagger UI or Postman collection included.  
- [x] Optional extras: All but Dockerfile (For now)

---

## Contact
Name: `Alejandro Ceron`  
[`@SrZafkiell`](https://github.com/SrZafkiell) (GitHub) » for code related talks.
[`@SrZafkiell`](https://co.linkedin.com/in/srzafkiell) (LinkedIn) for job offers.