# 🔗 URL Shortener with Analytics

A production-ready URL shortener built with **FastAPI**, featuring custom aliases, expiry support, Redis caching, rate limiting, and basic analytics.

---

## 🚀 Features

* 🔗 Shorten long URLs
* ✏️ Custom alias support
* ⏳ Expiry time for links
* ⚡ Redis caching (fast redirects)
* 🚫 Rate limiting (per IP)
* 📊 Analytics (click count, status, expiry)
* 🐳 Dockerized for easy deployment

---

## 🏗️ Tech Stack

* **Backend:** FastAPI (Python)
* **Database:** PostgreSQL (Supabase)
* **Cache:** Redis
* **ORM:** SQLAlchemy
* **Containerization:** Docker + Docker Compose

---

## 📁 Project Structure

```
PROJECT X/
│
├── app/
│   ├── main.py          # FastAPI app
│   ├── models.py        # DB models
│   ├── schemas.py       # Request/response schemas
│   ├── db.py            # DB connection
│   ├── utils.py         # Helper functions
│   ├── redis_client.py  # Redis connection
│   └── templates/       # Frontend (HTML)
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env                # Environment variables (NOT committed)
└── README.md
```

---

## ⚙️ Environment Variables

Create a `.env` file in the root directory:

```
DATABASE_URL=postgresql://<user>:<password>@aws-1-ap-south-1.pooler.supabase.com:6543/postgres
REDIS_HOST=redis
REDIS_PORT=6379
```

> ⚠️ Do NOT commit `.env` to GitHub.

---

# 🐳 Run with Docker (Recommended)

### 1. Prerequisites

* Install Docker Desktop
* Ensure Docker is running

---

### 2. Build & Run

```bash
docker-compose up --build
```

---

### 3. Access Application

```
http://localhost:8000
```

---

### 4. Stop Containers

```bash
docker-compose down
```

---

# 💻 Run Locally (Without Docker)

### 1. Create Virtual Environment

```bash
python -m venv xvenv
```

Activate:

* Windows:

```bash
xvenv\Scripts\activate
```

* Mac/Linux:

```bash
source xvenv/bin/activate
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Set Environment Variables

Create `.env` file (same as above)

---

### 4. Run Server

```bash
uvicorn app.main:app --reload
```

---

### 5. Open in Browser

```
http://127.0.0.1:8000
```

---

## 🔌 API Endpoints

### ➤ Shorten URL

```
POST /shorten
```

**Request Body:**

```json
{
  "url": "https://example.com",
  "custom_code": "myalias",
  "expiry_minutes": 10
}
```

---

### ➤ Redirect

```
GET /{short_code}
```

---

### ➤ Get Stats

```
GET /stats/{short_code}
```

**Response:**

```json
{
  "original_url": "...",
  "clicks": 10,
  "expiry": "...",
  "created_at": "...",
  "is_expired": false
}
```

---

## 📊 Analytics

* Total click count
* Expiry status (active/expired)
* Creation time
* (Optional extension: last accessed time)

---

## ⚠️ Notes

* Duplicate URLs reuse the same short code (unless custom alias is provided)
* Custom aliases must be unique
* Expired links are not reused
* Rate limiting prevents abuse (per IP)

---

## 🚀 Future Improvements

* 🌍 Country/device tracking
* 📈 Charts dashboard
* 🔐 User authentication
* 📅 Click history logs
* 🔗 QR code generation

---

## 👨‍💻 Author

Developed as a full-stack project demonstrating backend design, API development, caching, and deployment practices.

---
