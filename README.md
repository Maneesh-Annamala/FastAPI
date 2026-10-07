# 🚀 FastAPI Blog Application — Daily Learning Project

A full-stack asynchronous Blog application built with **FastAPI**, **SQLAlchemy 2.0 (Async)**, **PostgreSQL (`asyncpg`)**, **Alembic (Database Migrations)**, **Pydantic v2**, **Jinja2 Templates**, **Pillow (Image Processing)**, **aiosmtplib (Email System)**, and **JWT Authentication**. 

> 📌 **Learning Journey**: This repository records my daily progress as I learn and master FastAPI, moving from fundamental concepts to advanced asynchronous patterns, clean architecture, and full-stack web development.

---

## ✨ Features Built So Far

- **⚡ Asynchronous Database Architecture**: Fully async database interactions powered by **PostgreSQL**, `asyncpg`, **SQLAlchemy 2.0**, and FastAPI `lifespan` context manager.
- **🔄 Database Schema Migrations (Alembic)**: 
  - Version-controlled schema migrations with **Alembic**.
  - Async migration execution configured in `alembic/env.py` loading database credentials dynamically from Pydantic `Settings`.
  - Auto-generation of migration scripts (`alembic revision --autogenerate`) for seamless schema evolution and rollbacks (`alembic upgrade / downgrade`).
- **🔐 Secure Authentication & Authorization**:
  - JWT Access Token generation & verification using `PyJWT`.
  - Secure password hashing using **Argon2** via `pwdlib`.
  - OAuth2 Password Bearer flow for API authentication.
- **🔑 Password Reset & Email Integration**:
  - Secure token generation via `secrets.token_urlsafe(32)` with SHA-256 token hashing stored in `PasswordResetToken` table model.
  - Asynchronous SMTP email dispatching powered by **`aiosmtplib`** integrated with FastAPI `BackgroundTasks`.
  - Responsive Jinja2 HTML email template (`templates/email/password_reset.html`) with customizable reset URLs and automatic 30-minute token expiration.
  - Comprehensive API Endpoints:
    - `POST /api/users/forgot-password`: Generates reset token and triggers async email delivery (with generic anti-enumeration response).
    - `POST /api/users/reset-password`: Validates token, hashes new password, and invalidates used reset token.
    - `PATCH /api/users/me/password`: Authenticated password change endpoint with immediate reset token cleanup.
- **🖼️ Profile Picture Upload & Processing**:
  - **Pillow (PIL)** integration for background thread image manipulation (`run_in_threadpool`).
  - Automatic EXIF orientation correction, square crop & resize to 300x300, RGB mode conversion, and JPEG compression optimization.
  - Unique UUID-based filename generation & secure storage under `/media/profile_pics`.
  - Automatic cleanup & deletion of previous avatar files when updated or removed.
  - Fallback default avatar system via model property (`image_path`).
- **📄 Posts & User Posts Pagination**:
  - **Paginated API Endpoints**: `/api/posts` and `/api/users/{user_id}/posts` support `skip` and `limit` query parameters, returning a `PaginatedPostsResponse` schema (`total`, `skip`, `limit`, `has_more`, `posts`).
  - **Interactive "Load More" Feed**: Client-side async pagination on Home and User Posts pages via JavaScript Fetch API and dynamic DOM injection.
  - **Database Efficiency**: Optimized count and slice queries using SQLAlchemy `func.count()`, `offset()`, and `limit()`.
- **📝 Post & User Management**:
  - Relational Database Models with `Users`, `Posts`, and `PasswordResetToken` mapped via SQLAlchemy ORM.
  - Eager loading with `selectinload` for optimized N+1 query prevention.
- **🎨 Hybrid Layout (Web UI + REST API)**:
  - **Jinja2 Templates**: Dynamic server-side rendering for `Home`, `Login`, `Register`, `Account`, `Post detail`, and `User Posts` pages.
  - **Interactive Client Features**: Live image preview, AJAX multipart profile upload, dynamic UI authentication state updates, and async load-more feeds.
  - **API Endpoints**: Modularized router architecture under `/routers`.
- **🛠️ Smart Exception Handling**:
  - Dual response system handling errors gracefully: returning JSON for `/api` requests and custom styled HTML (`error.html`) for browser requests.

---

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **Backend Framework** | [FastAPI](https://fastapi.tiangolo.com/) |
| **Language** | Python 3.13+ |
| **Database** | [PostgreSQL](https://www.postgresql.org/) |
| **Async DB Driver & ORM** | `asyncpg` + [SQLAlchemy 2.0](https://www.sqlalchemy.org/) |
| **Database Migrations** | [Alembic](https://alembic.sqlalchemy.org/) |
| **Validation & Settings** | [Pydantic v2](https://docs.pydantic.dev/) & `pydantic-settings` |
| **Auth & Security** | `PyJWT`, `pwdlib` (Argon2), `hashlib`, `secrets` |
| **Email & Async SMTP** | `aiosmtplib`, Jinja2 HTML Templates |
| **Image Processing** | [Pillow (PIL)](https://python-pillow.org/) |
| **Templating** | Jinja2 Templates + HTML/CSS Static Files |
| **Package Manager** | [`uv`](https://github.com/astral-sh/uv) |

---

## 📂 Project Structure

```text
project_blogs/
├── alembic/
│   ├── versions/          # Database revision scripts (schema migrations)
│   ├── env.py             # Alembic migration environment (async config & SQLAlchemy metadata)
│   └── script.py.mako     # Migration template script
├── core/
│   └── config.py          # Environment settings using pydantic-settings (DATABASE_URL, SecretStr, SMTP)
├── media/
│   └── profile_pics/      # User-uploaded & processed profile avatars
├── routers/
│   ├── posts.py           # API routes for blog post operations with pagination
│   └── users.py           # API routes for auth, password reset, user profiles & paginated user posts
├── static/                # CSS, JS, icons, default avatar images
├── templates/             # Jinja2 HTML templates (layout, home, login, user_posts, etc.)
│   └── email/
│       └── password_reset.html # Responsive HTML email template for password reset
├── alembic.ini            # Alembic configuration settings
├── auth.py                # Password hashing, JWT access token & SHA-256 reset token utilities
├── database.py            # Async PostgreSQL engine setup & session dependency injection
├── email_utils.py         # Async SMTP email dispatching via aiosmtplib & Jinja2 rendering
├── image_utils.py         # Pillow image cropping, resizing, optimization & deletion utils
├── main.py                # App entrypoint, lifespan manager, Jinja rendering & error handlers
├── models.py              # SQLAlchemy ORM models (Users, Posts, PasswordResetToken)
├── populates_db.py        # Database seed script for test users, posts, and profile images
├── schemas.py             # Pydantic schemas (UserCreate, ForgetPasswordRequest, ResetPasswordRequest, etc.)
├── .env.example           # Template for environment configuration including PostgreSQL DATABASE_URL
├── .gitignore             # Ignored files (secrets, venv, media cache)
├── pyproject.toml         # Dependency definitions managed by uv
└── uv.lock                # Lockfile for reproducible builds
```

---

## ⚙️ Getting Started

### Prerequisites
- **Python 3.13+**
- **PostgreSQL Database** running locally or remotely
- **uv** package manager installed (`pip install uv` or `curl -LsSf https://astral.sh/uv/install.sh | sh`)

### Installation & Local Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/project_blogs.git
   cd project_blogs
   ```

2. **Sync virtual environment & dependencies with `uv`**:
   ```bash
   uv sync
   ```

3. **Configure Environment Variables**:
   Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
   *(Set your PostgreSQL connection string `DATABASE_URL` in `.env`, e.g., `postgresql+asyncpg://user:password@localhost:5432/blog_db`, along with your `SECRET_KEY` and SMTP email settings)*

4. **Run Database Migrations with Alembic**:
   Apply all schema migrations to create database tables in PostgreSQL:
   ```bash
   uv run alembic upgrade head
   ```

5. **(Optional) Populate Sample Seed Data**:
   Populate the database with initial users, blog posts, and avatars:
   ```bash
   uv run python populates_db.py
   ```

6. **Run the FastAPI Development Server**:
   ```bash
   uv run uvicorn main:app --reload
   ```

7. **Access the Application**:
   - 🌐 **Web Interface**: `http://127.0.0.1:8000/`
   - 📚 **Swagger Interactive API Docs**: `http://127.0.0.1:8000/docs`

---

## 🔄 Useful Alembic Migration Commands

- **Create a new migration after updating SQLAlchemy models**:
  ```bash
  uv run alembic revision --autogenerate -m "description of changes"
  ```
- **Apply pending migrations**:
  ```bash
  uv run alembic upgrade head
  ```
- **Roll back the last migration**:
  ```bash
  uv run alembic downgrade -1
  ```
- **Check current migration status**:
  ```bash
  uv run alembic current
  ```

---

## 📅 Daily Learning Log

| Day | Date | Key Highlights / Progress |
| :---: | :---: | :--- |
| **Day 1** | Initial Commit | Set up FastAPI application structure, async SQLAlchemy database engine (`aiosqlite`), ORM models (`Users`, `Posts`), JWT authentication with Argon2 hashing, modular routers, Jinja2 template rendering, and error handlers. |
| **Day 2** | Profile Picture Feature | Integrated **Pillow (PIL)** for avatar upload processing (300x300 cropping, EXIF rotation, optimization), UUID file management, media mounting, dynamic frontend previews, and user picture upload/delete endpoints. |
| **Day 3** | Posts & User Posts Pagination | Added offset & limit pagination to `/api/posts` and `/api/users/{user_id}/posts` with `PaginatedPostsResponse` schema, total post counting via `func.count()`, and interactive "Load More Posts" AJAX feeds on Home and User Posts pages. |
| **Day 4** | Password Reset & Email Integration | Built asynchronous backend password reset flow (`/forgot-password`, `/reset-password`, `/me/password`), `PasswordResetToken` table model with SHA-256 token hashing, `aiosmtplib` async SMTP background email delivery, and HTML email templates. |
| **Day 5** | PostgreSQL & Alembic Migrations | Upgraded database architecture from SQLite to **PostgreSQL** (`postgresql+asyncpg`). Integrated **Alembic** schema migrations with async database connection support (`alembic/env.py`). Created baseline schema migration and initial schema updates (`likes` column on `posts`). |

---

## 🛡️ License

This project is open-source and available under the [MIT License](LICENSE).
