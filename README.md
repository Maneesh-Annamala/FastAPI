# 🚀 FastAPI Blog Application — Daily Learning Project

A full-stack asynchronous Blog application built with **FastAPI**, **SQLAlchemy 2.0 (Async)**, **Pydantic v2**, **Jinja2 Templates**, **Pillow (Image Processing)**, and **JWT Authentication**. 

> 📌 **Learning Journey**: This repository records my daily progress as I learn and master FastAPI, moving from fundamental concepts to advanced asynchronous patterns, clean architecture, and full-stack web development.

---

## ✨ Features Built So Far

- **⚡ Asynchronous Database Architecture**: Fully async database interactions using **SQLAlchemy 2.0**, `aiosqlite`, and FastAPI `lifespan` context manager.
- **🔐 Secure Authentication & Authorization**:
  - JWT Access Token generation & verification using `PyJWT`.
  - Secure password hashing using **Argon2** via `pwdlib`.
  - OAuth2 Password Bearer flow for API authentication.
- **🖼️ Profile Picture Upload & Processing**:
  - **Pillow (PIL)** integration for background thread image manipulation (`run_in_threadpool`).
  - Automatic EXIF orientation correction, square crop & resize to 300x300, RGB mode conversion, and JPEG compression optimization.
  - Unique UUID-based filename generation & secure storage under `/media/profile_pics`.
  - Automatic cleanup & deletion of previous avatar files when updated or removed.
  - Fallback default avatar system via model property (`image_path`).
- **📝 Post & User Management**:
  - Relational Database Models with `Users` and `Posts` mapped via SQLAlchemy ORM.
  - Eager loading with `selectinload` for optimized N+1 query prevention.
- **🎨 Hybrid Layout (Web UI + REST API)**:
  - **Jinja2 Templates**: Dynamic server-side rendering for `Home`, `Login`, `Register`, `Account`, `Post detail`, and `User Posts` pages.
  - **Interactive Client Features**: Live image preview, AJAX multipart profile upload, and dynamic UI authentication state updates.
  - **API Endpoints**: Modularized router architecture under `/routers`.
- **🛠️ Smart Exception Handling**:
  - Dual response system handling errors gracefully: returning JSON for `/api` requests and custom styled HTML (`error.html`) for browser requests.

---

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **Backend Framework** | [FastAPI](https://fastapi.tiangolo.com/) |
| **Language** | Python 3.13+ |
| **Database & ORM** | SQLite + `aiosqlite` with [SQLAlchemy 2.0](https://www.sqlalchemy.org/) |
| **Validation & Settings** | [Pydantic v2](https://docs.pydantic.dev/) & `pydantic-settings` |
| **Auth & Security** | `PyJWT`, `pwdlib` (Argon2) |
| **Image Processing** | [Pillow (PIL)](https://python-pillow.org/) |
| **Templating** | Jinja2 Templates + HTML/CSS Static Files |
| **Package Manager** | [`uv`](https://github.com/astral-sh/uv) |

---

## 📂 Project Structure

```text
project_blogs/
├── core/
│   └── config.py          # Environment settings using pydantic-settings
├── media/
│   └── profile_pics/      # User-uploaded & processed profile avatars
├── routers/
│   ├── posts.py           # API routes for blog post operations
│   └── users.py           # API routes for authentication, user profile & picture uploads
├── static/                # CSS, JS, icons, default avatar images
├── templates/             # Jinja2 HTML templates (layout, home, login, account, etc.)
├── auth.py                # Password hashing & JWT token verification helpers
├── database.py            # Async engine setup & session dependency injection
├── image_utils.py         # Pillow image cropping, resizing, optimization & deletion utils
├── main.py                # App entrypoint, lifespan manager, Jinja rendering & error handlers
├── models.py              # SQLAlchemy ORM models (Users, Posts with image_path property)
├── schemas.py             # Pydantic schemas for request/response validation
├── .env.example           # Template for environment configuration
├── .gitignore             # Ignored files (secrets, venv, sqlite DB)
├── pyproject.toml         # Dependency definitions managed by uv
└── uv.lock                # Lockfile for reproducible builds
```

---

## ⚙️ Getting Started

### Prerequisites
- **Python 3.13+**
- **uv** package manager installed (Recommended: `pip install uv` or `curl -LsSf https://astral.sh/uv/install.sh | sh`)

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
   *(Optionally generate a custom `SECRET_KEY` in `.env`)*

4. **Run the FastAPI Development Server**:
   ```bash
   uv run uvicorn main:app --reload
   ```

5. **Access the Application**:
   - 🌐 **Web Interface**: `http://127.0.0.1:8000/`
   - 📚 **Swagger Interactive API Docs**: `http://127.0.0.1:8000/docs`

---

## 📅 Daily Learning Log

| Day | Date | Key Highlights / Progress |
| :---: | :---: | :--- |
| **Day 1** | Initial Commit | Set up FastAPI application structure, async SQLAlchemy database engine (`aiosqlite`), ORM models (`Users`, `Posts`), JWT authentication with Argon2 hashing, modular routers, Jinja2 template rendering, and error handlers. |
| **Day 2** | Profile Picture Feature | Integrated **Pillow (PIL)** for avatar upload processing (300x300 cropping, EXIF rotation, optimization), UUID file management, media mounting, dynamic frontend previews, and user picture upload/delete endpoints. |

---

## 🛡️ License

This project is open-source and available under the [MIT License](LICENSE).

