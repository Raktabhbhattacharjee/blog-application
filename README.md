# 🚀 DevChronicle — Modern Publishing & Editorial Platform

[![Django](https://img.shields.io/badge/Django-6.1-0C4B33?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![uv](https://img.shields.io/badge/Package%20Manager-uv-DE5FE9?style=for-the-badge&logo=astral&logoColor=white)](https://docs.astral.sh/uv/)
[![Tailwind CSS v4](https://img.shields.io/badge/Tailwind_CSS-v4.3.3-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Database](https://img.shields.io/badge/Database-Postgres%20%7C%20SQLite-003B57?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

> A production-ready, high-performance publication and editorial platform built with **Django 6.1**, **Gunicorn**, **WhiteNoise**, and **Tailwind CSS v4**. Featuring role-based workspaces, full article & category lifecycles, real-time reactions, discussions, and zero-N+1 database query optimizations.

---


---

## ✨ Key Features

### 🏛️ 1. Public Reader Portal
- **Dynamic Homepage**: Hero featured publications, category-filtered articles, and recent post feed.
- **Article Reader Experience**: Prose typography, lead summaries, cover images, author meta badges, and reading breadcrumbs.
- **Category Archives & Full-Text Search**: Filter by taxonomy topics and search across titles, summaries, body text, and category names.
- **Author & About Section**: Dynamic author bio and active social media links.

### ✍️ 2. Authoring Studio & Workspace (`/dashboard/`)
- **Isolated Author Workspaces**: Authors only see and manage their own submissions with metric cards (Total Posts, Published, Drafts, Featured).
- **Article Authoring Studio (`/dashboard/posts/add/`)**:
  - Image upload support with multi-part encoding.
  - Automatic unique slug generation from article titles.
  - Automatic author assignment (`post.author = request.user`).
- **Ownership-Protected Editing (`/dashboard/posts/edit/<id>/`)**: Pre-filled content, current cover image preview, and strict ownership validation.
- **1-Click Status Toggling (`/dashboard/posts/toggle-status/<id>/`)**: Instant switch between `Draft` ↔ `Published`.
- **Safe Deletion**: Article deletion with confirmation modals.

### 📊 3. Staff & Admin Analytics Overview (`/dashboard/admin-overview/`)
- **Platform Analytics**: Total articles, published count, drafts count, registered users, and active social channels.
- **Category Distribution Breakdown**: Visual Tailwind CSS progress bars displaying percentage share across publication topics.
- **Recent Activity Feed**: Cross-author publication activity log with author avatars and timestamps.

### 💬 4. Community Engagement & Social System
- **Discussion Threads**: Interactive comment submission form for authenticated readers, and login prompts for visitors.
- **Author Badges**: Highlighted `"Author"` badge when article creators participate in discussions.
- **1-Click Like Reactions**: Instant heart reaction toggle with live counter updates.
- **Card Social Indicators**: Like and comment counters displayed on homepage and archive cards.

### ⚡ 5. Performance & Security
- **Zero N+1 Queries**: Optimized queries using `select_related('category', 'author')` and `.annotate(total_likes=Count('likes'), total_comments=Count('comments'))`.
- **WhiteNoise Static Delivery**: Pre-compressed and cache-busted static asset serving.
- **Role-Based Access Control (RBAC)**: Distinct permissions for Superusers, Staff Editors, Authors, and Readers.
- **Security Hardening**: Dynamic `SECRET_KEY`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, and `@login_required` decorators.

---

## 🛠️ Tech Stack & Architecture

```
DevChronicle/
├── blog_main/                 # ⚙️ ROOT PROJECT CONFIGURATION
│   ├── settings.py            # Production settings (WhiteNoise, Postgres/SQLite fallback)
│   ├── urls.py                # Primary URL routing & media handlers
│   ├── wsgi.py                # WSGI entrypoint for Gunicorn
│   └── static/css/site.css    # Compiled Tailwind CSS v4 bundle
│
├── blogs/                     # 🏛️ CORE BUSINESS DOMAIN
│   ├── models.py              # Category, Blog, Comment, SocialLink, About models
│   ├── forms.py               # CommentForm & CategoryForm
│   ├── views.py               # Public controllers, comments handler & toggle_like
│   ├── context_processors.py  # Global categories and social links injectors
│   └── urls.py                # Category and search routes
│
├── dashboard/                 # 🛠️ EDITORIAL & RBAC MANAGEMENT
│   ├── forms.py               # CategoryForm & BlogPostForm with Tailwind widgets
│   ├── views.py               # Author workspace, Admin overview, Post & Category CRUD
│   └── urls.py                # Protected /dashboard/* routes
│
├── templates/                 # 🎨 TAILWIND CSS PRESENTATION LAYER
│   ├── base.html              # Master layout
│   ├── components/            # Reusable partials (Cards, Navbars, Stat widgets)
│   └── pages/                 # Full pages (Author Dashboard, Admin Overview, Detail, Home)
│
├── nginx/                     # 🛡️ NGINX REVERSE PROXY
│   └── default.conf           # Static/media serving & Gunicorn proxy rules
│
├── Dockerfile                 # Multi-stage production container definition (uv + Python 3.13)
├── docker-compose.yml         # Production multi-service orchestration (Web + PostgreSQL + Nginx)
└── pyproject.toml             # uv package manifest and project metadata
```

---

## 🚢 Production Deployment Guide

### Option A: Cloud PaaS (Render / Railway / Fly.io) — Recommended

1. **Push to GitHub**: Push your latest code to your GitHub repository.
2. **Create Web Service**:
   * Connect your repository in [Render](https://render.com) or [Railway](https://railway.app).
   * Select **Docker** environment (it automatically detects `Dockerfile`).
3. **Attach a PostgreSQL Database**:
   * Create a managed PostgreSQL instance in the dashboard.
4. **Configure Environment Variables**:
   Set the following variables in the Cloud dashboard:
   ```env
   DEBUG=False
   SECRET_KEY=your-generated-super-secret-key
   ALLOWED_HOSTS=.onrender.com,yourdomain.com
   CSRF_TRUSTED_ORIGINS=https://*.onrender.com,https://yourdomain.com
   DATABASE_URL=postgresql://user:password@host:5432/dbname
   ```
5. **Mount a Persistent Disk for Uploads**:
   * Mount path: `/app/media` (ensures user-uploaded blog covers are never lost on restart).
6. **Deploy**: Trigger deployment! Your app is live with SSL automatically enabled.

---

### Option B: Docker Compose with Nginx (VPS: AWS EC2 / DigitalOcean / Hetzner)

The project includes an **Nginx Reverse Proxy** container that:
- Listens on port `80` (HTTP entrypoint).
- Serves static assets (`/static/`) and media uploads (`/media/`) directly via shared Docker volumes at high speed.
- Proxies all dynamic requests to Gunicorn (`web:8000`).

1. Clone the repository on your server:
   ```bash
   git clone https://github.com/Raktabhbhattacharjee/blog-application.git
   cd blog-application
   ```

2. Create your `.env` file from the template:
   ```bash
   cp .env.example .env
   # Edit .env with your production credentials
   nano .env
   ```

3. Launch the full production stack (Django + Postgres + Nginx):
   ```bash
   docker compose up -d --build
   ```

4. Create an admin superuser inside the container:
   ```bash
   docker compose exec web python manage.py createsuperuser
   ```

5. Visit `http://your-server-ip` or `http://localhost` (no port number needed, Nginx serves on default HTTP port 80).

Your application is now running with Nginx, Gunicorn, and PostgreSQL!

---

## 💻 Local Development Setup

### Method 1: Using `uv` (Recommended)

```bash
# 1. Clone repository
git clone https://github.com/Raktabhbhattacharjee/blog-application.git
cd blog-application

# 2. Sync dependencies
uv sync

# 3. Apply migrations
uv run python manage.py migrate

# 4. Run development server
uv run python manage.py runserver
```

---

### Method 2: Using Docker Locally

```bash
# Build the Docker image
docker build -t blog-app .

# Run container with volume persistence for SQLite and Media
docker run -d -p 8000:8000 --name my-blog \
  -v ${PWD}/db.sqlite3:/app/db.sqlite3 \
  -v ${PWD}/media:/app/media \
  blog-app
```

Open **`http://localhost:8000`** in your browser!

---

## 🎨 Tailwind CSS Workflow

The project uses the **Tailwind standalone CLI binary** (No Node.js / npm required):

* **Watch Mode (Development)**:
  ```bash
  tools\tailwindcss.exe -i blog_main\static_src\input.css -o blog_main\static\css\site.css --watch
  ```
* **Production Build & Minify**:
  ```bash
  tools\tailwindcss.exe -i blog_main\static_src\input.css -o blog_main\static\css\site.css --minify
  ```

---

## 🔐 Environment Variables Reference

| Variable | Required | Default | Description |
| :--- | :--- | :--- | :--- |
| `DEBUG` | No | `False` | Toggle Django debug mode (`True`/`False`) |
| `SECRET_KEY` | **Yes (Prod)** | Dev Insecure Key | Cryptographic key for session/cookie security |
| `ALLOWED_HOSTS` | **Yes (Prod)** | `*` | Comma-separated list of host/domain names |
| `CSRF_TRUSTED_ORIGINS` | **Yes (Prod)** | `""` | Comma-separated trusted origins for HTTPS POST requests |
| `POSTGRES_DB` | No | SQLite fallback | PostgreSQL Database name |
| `POSTGRES_USER` | No | `postgres` | PostgreSQL Username |
| `POSTGRES_PASSWORD` | No | `""` | PostgreSQL Password |
| `POSTGRES_HOST` | No | `postgres` | PostgreSQL Hostname |
| `POSTGRES_PORT` | No | `5432` | PostgreSQL Port |

---

## 👥 Verified Test Accounts

| Role | Username | Password | Access Scope |
| :--- | :--- | :--- | :--- |
| **Superuser** | `rishi` | `admin123` | Full System Access, Django Admin (`/admin/`), Admin Overview & Author Studio |
| **Staff Editor** | `staff_editor` | `staff123` | Admin Overview (`/dashboard/admin-overview/`), Author Workspace, Global Editing |
| **Author** | `alex_dev` | `password123` | Author Workspace (`/dashboard/`) — Strictly own articles & drafts |
| **Author #2** | `animefan` | `pass123` | Author Workspace (`/dashboard/`) — Strictly own articles & drafts |
| **Reader** | `john_reader` | `reader123` | Public browsing, commenting, and liking |

---

## 📄 License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
