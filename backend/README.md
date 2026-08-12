# Health A-Z Backend API

A FastAPI backend for the Health A-Z mobile app with user auth, conditions database, and vitals history.

## Tech Stack
- **FastAPI** — Python web framework
- **SQLite** — Database (zero config, file-based)
- **SQLAlchemy** — ORM
- **JWT** — Authentication tokens
- **Bcrypt** — Password hashing

## Project Structure
```
health-az-backend/
├── main.py              # App entry point
├── database.py          # DB connection
├── auth_utils.py        # JWT + password helpers
├── seed.py              # Pre-populate conditions
├── requirements.txt
├── models/
│   └── models.py        # DB tables
├── schemas/
│   └── schemas.py       # Request/response shapes
└── routers/
    ├── auth.py          # /auth/register, /auth/login
    ├── users.py         # /users/me
    ├── conditions.py    # /conditions
    └── vitals.py        # /vitals
```

## Setup & Run

### 1. Install Python 3.10+
Download from https://python.org

### 2. Create virtual environment
```bash
cd health-az-backend
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the server
```bash
uvicorn main:app --reload
```

Server runs at: **http://localhost:8000**

Interactive API docs: **http://localhost:8000/docs**

---

## API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Create account |
| POST | `/auth/login` | Login, get token |

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users/me` | Get my profile |

### Conditions
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/conditions/` | All conditions (filter by `?category=` or `?search=`) |
| GET | `/conditions/categories` | List all categories |
| GET | `/conditions/{id}` | Single condition |

### Vitals (requires login)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/vitals/` | Save vitals reading |
| GET | `/vitals/` | My vitals history |
| DELETE | `/vitals/{id}` | Delete a record |

---

## Example: Register & Login

```bash
# Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Hima","email":"hima@example.com","password":"secret123"}'

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"hima@example.com","password":"secret123"}'
```

## Deploy (Free)
- **Railway**: https://railway.app — connect GitHub repo, auto-deploys
- **Render**: https://render.com — free tier available
- **Fly.io**: https://fly.io — free tier available
