# 🚀 DevChronicle — Modern Publishing & Editorial Platform

[![Django](https://img.shields.io/badge/Django-6.1-0C4B33?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Tailwind CSS v4](https://img.shields.io/badge/Tailwind_CSS-v4.3.3-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/Database-SQLite%20%2F%20Postgres-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

> A production-grade, modular monolithic publication and editorial platform built with **Django 6.1** and **Tailwind CSS v4**. Featuring role-based workspaces, complete article & category CRUD lifecycles, interactive community discussion threads, 1-click reaction systems, and zero-N+1 query optimizations.

---

## 📹 Video Walkthrough & Demo
> 🎥 **Watch the full application walkthrough & feature demo:**  
> **[DevChronicle Video Walkthrough & Feature Demo](https://youtube.com)** *(Click to view video demo)*

---

## ✨ Key Features

### 🏛️ 1. Public Reader Portal
- **Dynamic Homepage**: Hero featured publications, category-filtered articles, and recent post feed.
- **Article Reader Experience**: Prose typography, lead summaries, cover images, author meta badges, and reading breadcrumbs.
- **Category Archives & Full-Text Search**: Filter by taxonomy topics and search across titles, summaries, body text, and category names.
- **Author & About Section**: Dynamic bio and active social media channels.

### ✍️ 2. Authoring Studio & Workspace (`/dashboard/`)
- **Isolated Author Workspaces**: Authors only see and manage their own submissions with personal metric cards (Total Posts, Published, Drafts, Featured).
- **Article Authoring Studio (`/dashboard/posts/add/`)**:
  - Image upload support with multi-part encoding.
  - Automatic unique slug generation from article titles.
  - Automatic author assignment (`post.author = request.user`).
- **Ownership-Protected Editing (`/dashboard/posts/edit/<id>/`)**: Pre-filled content, current cover image thumbnail preview, and ownership validation.
- **1-Click Status Toggling (`/dashboard/posts/toggle-status/<id>/`)**: Instant switch between `Draft` ↔ `Published`.
- **Safe Deletion**: Article deletion with confirmation dialogs.

### 📊 3. Staff & Admin Analytics Overview (`/dashboard/admin-overview/`)
- **Platform Analytics**: Total articles, published count, drafts count, registered users, and active social channels.
- **Category Distribution Breakdown**: Visual Tailwind CSS progress bars displaying percentage share across all publication topics.
- **Recent Activity Feed**: Real-time cross-author publication activity log with author avatars and timestamps.

### 💬 4. Community Engagement & Social System
- **Discussion Threads**: Interactive comment submission form for authenticated readers, and login prompts for visitors.
- **Author Badges**: Highlighted `"Author"` badge when article creators participate in discussions.
- **1-Click Like / Unlike Reactions**: Instant heart reaction toggle with live like counters.
- **Social Indicators on Cards**: Real-time like and comment counters on homepage and archive cards.

### ⚡ 5. Performance & Security
- **Zero N+1 Queries**: Optimized database queries utilizing `select_related('category', 'author')` and `.annotate(total_likes=Count('likes'), total_comments=Count('comments'))` to load full pages in a single database query.
- **Role-Based Access Control (RBAC)**: Distinct permissions for Superusers, Staff Editors, Authors, and Readers.
- **Security Hardening**: `@login_required` decorators, CSRF token validation on all forms, and automated redirects for authenticated users on auth pages.

---

## 🛠️ Architecture & Tech Stack

```
DevChronicle/
├── blog_main/                 # ⚙️ ROOT PROJECT CONFIGURATION
│   ├── settings.py            # Global settings (Auth redirects, Installed apps)
│   ├── urls.py                # Primary URL router & static media handler
│   └── static/css/site.css    # Compiled standalone Tailwind CSS v4 bundle
│
├── blogs/                     # 🏛️ CORE BUSINESS DOMAIN
│   ├── models.py              # Category, Blog (with likes M2M), Comment, SocialLink, About
│   ├── forms.py               # CommentForm & CategoryForm
│   ├── views.py               # Public controllers, comments handler & toggle_like
│   ├── context_processors.py  # Global categories and social links injectors
│   └── urls.py                # Public category and search routes
│
├── dashboard/                 # 🛠️ EDITORIAL & RBAC MANAGEMENT
│   ├── forms.py               # CategoryForm & BlogPostForm with Tailwind widgets
│   ├── views.py               # Author workspace, Admin overview, Post & Category CRUD
│   └── urls.py                # Protected /dashboard/* routes
│
└── templates/                 # 🎨 TAILWIND CSS PRESENTATION LAYER
    ├── base.html              # Master layout (Header, Nav, Flash alerts, Footer)
    ├── components/            # Reusable partials (Cards, Navbars, Stat widgets)
    └── pages/                 # Full pages (Author Dashboard, Admin Overview, Detail, Home)
```

---

## 🚀 Quickstart & Local Setup

### 1. Clone & Setup Virtual Environment
```bash
git clone https://github.com/Raktabhbhattacharjee/blog-application.git
cd blog-application

# Create and activate virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 2. Install Dependencies & Apply Migrations
```bash
pip install -r requirements.txt  # Or install django pillow
python manage.py migrate
```

### 3. Tailwind CSS Workflow (Standalone Binary — No Node.js Required)
The project uses the **Tailwind standalone CLI binary** in `tools/tailwindcss.exe`:

* **Watch Mode (Development)**:
  ```bash
  tools/tailwindcss.exe -i blog_main/static_src/input.css -o blog_main/static/css/site.css --watch
  ```
* **Production Build**:
  ```bash
  tools/tailwindcss.exe -i blog_main/static_src/input.css -o blog_main/static/css/site.css --minify
  ```

### 4. Run Development Server
```bash
python manage.py runserver
```
Visit **`http://127.0.0.1:8000/`** in your browser!

---

## 👥 Verified Test Accounts

| Role | Username | Password | Access Scope |
| :--- | :--- | :--- | :--- |
| **Superuser** | `rishi` | `admin123` | Full System Access, Django Admin (`/admin/`), Admin Overview & Author Studio |
| **Staff Editor** | `staff_editor` | `staff123` | Admin Overview (`/dashboard/admin-overview/`), Author Workspace, Global Post Editing |
| **Author** | `alex_dev` | `password123` | Author Workspace (`/dashboard/`) — Strictly own articles & drafts |
| **Author #2** | `animefan` | `pass123` | Author Workspace (`/dashboard/`) — Strictly own articles & drafts |
| **Reader** | `john_reader` | `reader123` | Public browsing, commenting, and liking |

---

## 🚢 Deployment Readiness Checklist
- [x] Static files configured for `collectstatic` with minified Tailwind bundle.
- [x] Media root and URLs configured for article cover image uploads.
- [x] CSRF protection and `@login_required` decorators active across all mutating routes.
- [x] Database indexes and ForeignKey cascades configured.
- [x] N+1 query elimination via `select_related` and `.annotate(Count(...))`.

---

## 📄 License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
