# Coding Agent Test Spec — Team & Task Manager WebApp (Python)

---

## VERSION 1 — SIMPLE

Build a Flask web application to manage developers and their tasks.

**Stack:** Python 3.12+, Flask, SQLAlchemy, Jinja2, SQLite (dev), PostgreSQL (prod).  
**Port:** 8765  
**Login:** demo / demo (hardcoded session-based auth)

**What to build:**
- A login page. On success, redirect to the dashboard.
- A **Developers** page: list, add, edit, delete developers (name, email, role).
- A **Tasks** page: list, add, edit, delete tasks (title, description, status, assigned developer).
- Use SQLite for `dev` environment. Wire PostgreSQL for `prod` (via env var `DATABASE_URL`).
- All DB schema handled by SQLAlchemy with `db.create_all()` on startup.
- The app must start cleanly with `python app.py` on port 8765 and be fully usable in a browser.

**UI:** Dark mode throughout. Use Bootstrap 5 `data-bs-theme="dark"` on `<html>`.
Accent color: indigo/violet (`#6366f1`). Card-based layout. Font: Inter (Google Fonts).

**Acceptance:** App starts, login works, full CRUD on developers and tasks works, tasks can be assigned to a developer.

---

---

## VERSION 2 — NORMAL

### Goal
Build a production-grade Flask web application for managing a development team and their assigned tasks, following Clean Architecture, DDD, and TDD principles — with a polished, beautiful dark-mode UI.

---

### Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12+ |
| Framework | Flask 3.x |
| UI | Jinja2 + Bootstrap 5 (CDN) + custom dark theme CSS |
| Icons | Bootstrap Icons 1.11 (CDN) |
| ORM | SQLAlchemy 2.x + Flask-SQLAlchemy |
| Migrations | Flask-Migrate (Alembic) |
| Forms & Validation | WTForms + Flask-WTF |
| Auth | Flask-Login + Werkzeug password hashing |
| DB — dev | SQLite (file: `dev.db`) |
| DB — prod | PostgreSQL |
| Testing | pytest + pytest-flask + factory-boy |
| Package Manager | pip + `requirements.txt` (pre-installed on machine) |
| Port | **8765** |

---

### Project Structure

```
team_manager/
├── domain/
│   ├── models.py               # Pure Python dataclasses / value objects (no ORM)
│   └── repositories.py         # Abstract repository interfaces (ABC)
├── application/
│   └── services/
│       ├── developer_service.py
│       └── task_service.py
├── infrastructure/
│   ├── persistence/
│   │   ├── orm_models.py       # SQLAlchemy ORM models
│   │   └── repositories.py    # Concrete repo implementations
│   └── security/
│       └── auth.py             # Flask-Login user loader
├── presentation/
│   └── web/
│       ├── developers/
│       │   ├── __init__.py     # Blueprint
│       │   ├── routes.py
│       │   └── forms.py
│       ├── tasks/
│       │   ├── __init__.py
│       │   ├── routes.py
│       │   └── forms.py
│       └── auth/
│           ├── __init__.py
│           └── routes.py
├── static/
│   └── css/
│       └── theme.css           # Custom dark theme (required — see Design System)
├── templates/
│   ├── layout.html             # Sidebar layout base template
│   ├── macros.html             # Reusable Jinja2 macros (status badge, etc.)
│   ├── dashboard.html
│   ├── auth/login.html
│   ├── developers/
│   │   ├── list.html
│   │   ├── form.html           # Reused for create AND edit
│   │   └── confirm_delete.html
│   └── tasks/
│       ├── list.html
│       ├── form.html
│       └── confirm_delete.html
├── config.py
├── app.py                      # App factory entry point
└── tests/
    ├── conftest.py
    ├── unit/
    ├── integration/
    └── e2e/
```

**Layering rules:**
- **Domain layer**: zero Flask/SQLAlchemy imports — pure Python only.
- **Application services**: depend only on domain abstract interfaces.
- **Infrastructure**: adapters implement domain repository ABCs.
- **Controllers (routes)**: thin — delegate everything to application services.

---

### Domain Model

**Developer** (`domain/models.py` — plain dataclass)
- `id` (UUID)
- `name` (str, required, non-blank)
- `email` (str, required, unique, valid format)
- `role` (enum: `FRONTEND`, `BACKEND`, `FULLSTACK`, `DEVOPS`, `QA`)

**Task** (`domain/models.py`)
- `id` (UUID)
- `title` (str, required, non-blank)
- `description` (str, optional)
- `status` (enum: `TODO`, `IN_PROGRESS`, `DONE`)
- `assigned_developer_id` (UUID | None)
- `created_at` (datetime, auto-set)

**TaskStatus** and **DeveloperRole** are Python `enum.Enum` classes in the domain layer.

---

### Features & CRUD

#### Authentication
- Flask-Login with a single hardcoded user: **login `demo` / password `demo`**.
- Password stored hashed via `werkzeug.security.generate_password_hash`.
- All routes except `/login` require `@login_required`.
- On logout, redirect to `/login`.

#### Developer Management (`/developers`)
- List all developers in a styled table.
- Add new developer (WTForms with server-side validation).
- Edit existing developer.
- Delete developer (confirmation page; unassign tasks first, do **not** cascade-delete tasks).

#### Task Management (`/tasks`)
- List all tasks with developer name and a colored status badge.
- Filter by status and/or assigned developer (GET params, dropdown selects).
- Add / edit / delete tasks.

#### Dashboard (`/`)
- Stat cards: total developers, total tasks, counts per status.
- Recent tasks list (last 5 created).

---

### UI Design System — Dark Mode

This is a **first-class requirement**, not an afterthought. The UI must look clean, modern, and professional. Bootstrap alone is not enough — all overrides below are mandatory.

#### Color Palette

| Token | Hex | Usage |
|---|---|---|
| `--bg-base` | `#0f1117` | Page background |
| `--bg-surface` | `#1a1d27` | Cards, sidebar, panels |
| `--bg-elevated` | `#22263a` | Inputs, hovered rows, code blocks |
| `--accent` | `#6366f1` | Primary buttons, active nav links, focus rings |
| `--accent-hover` | `#4f46e5` | Hover state for accent elements |
| `--text-primary` | `#f1f5f9` | Headings and body text |
| `--text-muted` | `#94a3b8` | Labels, captions, secondary text |
| `--border` | `#2e3347` | Card borders, dividers, input borders |
| `--success` | `#22c55e` | Done status, success alerts |
| `--warning` | `#f59e0b` | In-progress status |
| `--danger` | `#ef4444` | Errors, delete buttons |
| `--info` | `#38bdf8` | Todo status, info alerts |

#### Typography
- Font family: **Inter** — load from Google Fonts (`weights: 400, 500, 600, 700`).
- Base size: `14px` for data-dense views, `15px` for forms.
- Headings: `font-weight: 600`, slight negative letter-spacing.

#### Layout
Use a **fixed sidebar + scrollable main content** layout. NOT a top navbar.

```
┌──────────────────────────────────────────────────────┐
│  SIDEBAR (240px, fixed) │  MAIN CONTENT              │
│                         │                            │
│  ◆ TeamManager          │  [Page Header + CTA btn]   │
│                         │                            │
│  ⬡ Dashboard            │  [Flash messages]          │
│  👥 Developers          │                            │
│  ✓  Tasks               │  [Page content — table     │
│                         │   or form or cards]        │
│  ─────────────────────  │                            │
│  👤 demo       [logout] │                            │
└──────────────────────────────────────────────────────┘
```

#### `static/css/theme.css` — Full Required CSS

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
  --bg-base:      #0f1117;
  --bg-surface:   #1a1d27;
  --bg-elevated:  #22263a;
  --accent:       #6366f1;
  --accent-hover: #4f46e5;
  --text-primary: #f1f5f9;
  --text-muted:   #94a3b8;
  --border:       #2e3347;
  --success:      #22c55e;
  --warning:      #f59e0b;
  --danger:       #ef4444;
  --info:         #38bdf8;
}

body {
  font-family: 'Inter', sans-serif;
  background-color: var(--bg-base);
  color: var(--text-primary);
  min-height: 100vh;
}

/* ── Sidebar ── */
.sidebar {
  width: 240px;
  min-height: 100vh;
  background: var(--bg-surface);
  border-right: 1px solid var(--border);
  padding: 1.5rem 1rem;
  position: fixed;
  top: 0; left: 0;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.sidebar .brand {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--text-primary);
  padding: 0.5rem 0.75rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.sidebar .brand i { color: var(--accent); }

.sidebar .nav-link {
  color: var(--text-muted);
  border-radius: 8px;
  padding: 0.55rem 0.75rem;
  font-size: 0.875rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.6rem;
  transition: all 0.15s ease;
  text-decoration: none;
}

.sidebar .nav-link:hover {
  background: var(--bg-elevated);
  color: var(--text-primary);
}

.sidebar .nav-link.active {
  background: rgba(99, 102, 241, 0.12);
  color: var(--accent);
}

.sidebar-footer {
  margin-top: auto;
  padding-top: 1rem;
  border-top: 1px solid var(--border);
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding-left: 0.5rem;
}

.sidebar-footer .avatar {
  width: 30px; height: 30px;
  border-radius: 50%;
  background: var(--accent);
  display: flex; align-items: center; justify-content: center;
  font-size: 0.75rem;
  font-weight: 700;
  flex-shrink: 0;
}

.sidebar-footer .username {
  font-size: 0.85rem;
  color: var(--text-muted);
  flex: 1;
}

.sidebar-footer a {
  color: var(--text-muted);
  font-size: 1rem;
}

.sidebar-footer a:hover { color: var(--danger); }

/* ── Main content ── */
.main-content {
  margin-left: 240px;
  padding: 2rem 2.5rem;
  min-height: 100vh;
}

/* ── Page header ── */
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.75rem;
}

.page-header h1 {
  font-size: 1.35rem;
  font-weight: 700;
  margin: 0;
}

/* ── Cards ── */
.card {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: 12px;
}

.card-header {
  background: transparent;
  border-bottom: 1px solid var(--border);
  padding: 0.9rem 1.25rem;
  font-weight: 600;
  font-size: 0.9rem;
}

/* ── Stat cards (dashboard) ── */
.stat-card {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.25rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stat-icon {
  width: 44px; height: 44px;
  border-radius: 10px;
  background: var(--bg-elevated);
  display: flex; align-items: center; justify-content: center;
  font-size: 1.2rem;
  color: var(--accent);
  flex-shrink: 0;
}

.stat-value {
  font-size: 1.65rem;
  font-weight: 700;
  line-height: 1;
  color: var(--text-primary);
}

.stat-label {
  font-size: 0.78rem;
  color: var(--text-muted);
  margin-top: 0.25rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  font-weight: 500;
}

/* ── Tables ── */
.table {
  color: var(--text-primary);
  border-color: var(--border);
}

.table thead th {
  background: var(--bg-elevated);
  color: var(--text-muted);
  font-size: 0.72rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  border-bottom: 1px solid var(--border);
  padding: 0.7rem 1rem;
}

.table tbody td {
  padding: 0.85rem 1rem;
  border-bottom: 1px solid var(--border);
  vertical-align: middle;
}

.table tbody tr:hover td {
  background: var(--bg-elevated);
}

.table tbody tr:last-child td { border-bottom: none; }

/* ── Form inputs ── */
.form-control, .form-select {
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  color: var(--text-primary);
  border-radius: 8px;
  font-size: 0.9rem;
}

.form-control::placeholder { color: var(--text-muted); opacity: 0.6; }

.form-control:focus, .form-select:focus {
  background: var(--bg-elevated);
  border-color: var(--accent);
  color: var(--text-primary);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.18);
}

.form-select option { background: var(--bg-elevated); }

.form-label {
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.4rem;
}

.invalid-feedback { font-size: 0.8rem; color: var(--danger); }
.is-invalid { border-color: var(--danger) !important; }

/* ── Buttons ── */
.btn-primary {
  background: var(--accent);
  border-color: var(--accent);
  font-weight: 500;
  font-size: 0.875rem;
  border-radius: 8px;
}

.btn-primary:hover, .btn-primary:focus {
  background: var(--accent-hover);
  border-color: var(--accent-hover);
}

.btn-outline-secondary {
  border-color: var(--border);
  color: var(--text-muted);
  border-radius: 8px;
  font-size: 0.875rem;
}

.btn-outline-secondary:hover {
  background: var(--bg-elevated);
  color: var(--text-primary);
  border-color: var(--border);
}

.btn-danger {
  background: transparent;
  border-color: var(--danger);
  color: var(--danger);
  border-radius: 8px;
  font-size: 0.875rem;
}

.btn-danger:hover {
  background: var(--danger);
  color: white;
}

/* ── Status badges ── */
.badge-todo {
  background: rgba(56, 189, 248, 0.12);
  color: var(--info);
  border-radius: 20px;
  padding: 3px 10px;
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.02em;
  white-space: nowrap;
}

.badge-in-progress {
  background: rgba(245, 158, 11, 0.12);
  color: var(--warning);
  border-radius: 20px;
  padding: 3px 10px;
  font-size: 0.72rem;
  font-weight: 600;
  white-space: nowrap;
}

.badge-done {
  background: rgba(34, 197, 94, 0.12);
  color: var(--success);
  border-radius: 20px;
  padding: 3px 10px;
  font-size: 0.72rem;
  font-weight: 600;
  white-space: nowrap;
}

.badge-role {
  background: rgba(99, 102, 241, 0.12);
  color: var(--accent);
  border-radius: 20px;
  padding: 3px 10px;
  font-size: 0.72rem;
  font-weight: 600;
}

/* ── Flash alerts ── */
.alert {
  border-radius: 10px;
  font-size: 0.875rem;
  font-weight: 500;
}

.alert-success {
  background: rgba(34, 197, 94, 0.1);
  border: 1px solid rgba(34, 197, 94, 0.25);
  color: var(--success);
}

.alert-danger {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.25);
  color: var(--danger);
}

.alert-info {
  background: rgba(56, 189, 248, 0.1);
  border: 1px solid rgba(56, 189, 248, 0.25);
  color: var(--info);
}

.btn-close { filter: invert(1) opacity(0.5); }

/* ── Login page ── */
.login-wrapper {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-base);
}

.login-card {
  width: 100%;
  max-width: 400px;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 2.5rem 2rem;
}

.login-logo {
  font-size: 1.4rem;
  font-weight: 700;
  color: var(--accent);
  text-align: center;
  margin-bottom: 0.4rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.login-subtitle {
  text-align: center;
  color: var(--text-muted);
  font-size: 0.875rem;
  margin-bottom: 2rem;
}

/* ── Empty state ── */
.empty-state {
  text-align: center;
  padding: 3.5rem 1rem;
  color: var(--text-muted);
}

.empty-state i {
  font-size: 2.5rem;
  display: block;
  margin-bottom: 0.75rem;
  opacity: 0.4;
}

.empty-state p {
  font-size: 0.9rem;
  margin-bottom: 1.25rem;
}

/* ── Confirm delete card ── */
.confirm-card {
  max-width: 480px;
  margin: 4rem auto;
}

.confirm-card .confirm-icon {
  width: 56px; height: 56px;
  border-radius: 50%;
  background: rgba(239, 68, 68, 0.12);
  display: flex; align-items: center; justify-content: center;
  font-size: 1.4rem;
  color: var(--danger);
  margin: 0 auto 1rem;
}
```

---

### Template Patterns

#### `layout.html`
```html
<!DOCTYPE html>
<html lang="en" data-bs-theme="dark">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{% block title %}TeamManager{% endblock %}</title>
  <link rel="stylesheet"
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"/>
  <link rel="stylesheet"
        href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css"/>
  <link rel="stylesheet" href="{{ url_for('static', filename='css/theme.css') }}"/>
</head>
<body>

{% if current_user.is_authenticated %}
<nav class="sidebar">
  <div class="brand">
    <i class="bi bi-diagram-3-fill"></i> TeamManager
  </div>

  <a href="{{ url_for('dashboard.index') }}"
     class="nav-link {% if request.endpoint == 'dashboard.index' %}active{% endif %}">
    <i class="bi bi-speedometer2"></i> Dashboard
  </a>
  <a href="{{ url_for('developers.list') }}"
     class="nav-link {% if 'developers' in (request.endpoint or '') %}active{% endif %}">
    <i class="bi bi-people"></i> Developers
  </a>
  <a href="{{ url_for('tasks.list') }}"
     class="nav-link {% if 'tasks' in (request.endpoint or '') %}active{% endif %}">
    <i class="bi bi-check2-square"></i> Tasks
  </a>

  <div class="sidebar-footer">
    <div class="avatar">D</div>
    <span class="username">demo</span>
    <a href="{{ url_for('auth.logout') }}" title="Logout">
      <i class="bi bi-box-arrow-right"></i>
    </a>
  </div>
</nav>

<div class="main-content">
  {% with messages = get_flashed_messages(with_categories=true) %}
    {% for category, message in messages %}
      <div class="alert alert-{{ category }} alert-dismissible mb-3" role="alert">
        <i class="bi {% if category == 'success' %}bi-check-circle{% else %}bi-exclamation-circle{% endif %} me-2"></i>
        {{ message }}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
      </div>
    {% endfor %}
  {% endwith %}

  {% block content %}{% endblock %}
</div>

{% else %}
{% block auth_content %}{% endblock %}
{% endif %}

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

#### `auth/login.html`
```html
{% extends "layout.html" %}
{% block auth_content %}
<div class="login-wrapper">
  <div class="login-card">
    <div class="login-logo">
      <i class="bi bi-diagram-3-fill"></i> TeamManager
    </div>
    <p class="login-subtitle">Sign in to your workspace</p>

    {% with messages = get_flashed_messages(with_categories=true) %}
      {% for category, message in messages %}
        <div class="alert alert-{{ category }} mb-3">{{ message }}</div>
      {% endfor %}
    {% endwith %}

    <form method="POST" action="{{ url_for('auth.login') }}">
      {{ form.hidden_tag() }}
      <div class="mb-3">
        <label class="form-label">Username</label>
        {{ form.username(class="form-control", placeholder="demo") }}
        {% for e in form.username.errors %}
          <div class="invalid-feedback d-block">{{ e }}</div>
        {% endfor %}
      </div>
      <div class="mb-4">
        <label class="form-label">Password</label>
        {{ form.password(class="form-control", placeholder="••••••••",
                         type="password") }}
        {% for e in form.password.errors %}
          <div class="invalid-feedback d-block">{{ e }}</div>
        {% endfor %}
      </div>
      <button type="submit" class="btn btn-primary w-100">
        <i class="bi bi-box-arrow-in-right me-1"></i> Sign in
      </button>
    </form>
  </div>
</div>
{% endblock %}
```

#### `macros.html` — Reusable badges
```html
{% macro status_badge(status) %}
  {% if status == 'TODO' %}
    <span class="badge-todo"><i class="bi bi-circle me-1"></i>Todo</span>
  {% elif status == 'IN_PROGRESS' %}
    <span class="badge-in-progress"><i class="bi bi-arrow-repeat me-1"></i>In Progress</span>
  {% elif status == 'DONE' %}
    <span class="badge-done"><i class="bi bi-check-circle me-1"></i>Done</span>
  {% endif %}
{% endmacro %}

{% macro role_badge(role) %}
  <span class="badge-role">{{ role }}</span>
{% endmacro %}
```

#### `dashboard.html`
```html
{% extends "layout.html" %}
{% block title %}Dashboard — TeamManager{% endblock %}
{% block content %}
<div class="page-header">
  <h1><i class="bi bi-speedometer2 me-2" style="color:var(--accent)"></i>Dashboard</h1>
</div>

<div class="row g-3 mb-4">
  <div class="col-md-3">
    <div class="stat-card">
      <div class="stat-icon"><i class="bi bi-people"></i></div>
      <div>
        <div class="stat-value">{{ stats.total_developers }}</div>
        <div class="stat-label">Developers</div>
      </div>
    </div>
  </div>
  <div class="col-md-3">
    <div class="stat-card">
      <div class="stat-icon"><i class="bi bi-list-task"></i></div>
      <div>
        <div class="stat-value">{{ stats.total_tasks }}</div>
        <div class="stat-label">Total Tasks</div>
      </div>
    </div>
  </div>
  <div class="col-md-3">
    <div class="stat-card">
      <div class="stat-icon" style="color:var(--warning)"><i class="bi bi-arrow-repeat"></i></div>
      <div>
        <div class="stat-value">{{ stats.in_progress }}</div>
        <div class="stat-label">In Progress</div>
      </div>
    </div>
  </div>
  <div class="col-md-3">
    <div class="stat-card">
      <div class="stat-icon" style="color:var(--success)"><i class="bi bi-check-circle"></i></div>
      <div>
        <div class="stat-value">{{ stats.done }}</div>
        <div class="stat-label">Done</div>
      </div>
    </div>
  </div>
</div>

<div class="card">
  <div class="card-header">Recent Tasks</div>
  <!-- recent tasks table -->
</div>
{% endblock %}
```

---

### Configuration

**`config.py`**
```python
import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]

config = {
    "dev": DevelopmentConfig,
    "prod": ProductionConfig,
}
```

**`app.py`**
```python
from flask import Flask
from config import config

def create_app(env="dev"):
    app = Flask(__name__)
    app.config.from_object(config[env])
    # init extensions, register blueprints
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(port=8765, debug=True)
```

---

### TDD Requirements

| Layer | Test Type | Tool | Examples |
|---|---|---|---|
| Domain models | Unit | pytest | Enum validation, dataclass constraints |
| Application services | Unit | pytest + `unittest.mock` | `DeveloperService.create()`, delete/unassign flow |
| Routes | Integration | `pytest-flask` test client | POST redirects, flash messages |
| ORM repos | Integration | pytest + SQLite in-memory | Queries, unique constraints |
| Full flow | E2E | `pytest-flask` | Login → create dev → create task → assign |

`tests/conftest.py` must provide `app`, `client`, and `logged_in_client` fixtures plus `factory-boy` factories.

```bash
pytest --tb=short -v
```

---

### `requirements.txt`

```
Flask>=3.0
Flask-SQLAlchemy>=3.1
Flask-Migrate>=4.0
Flask-Login>=0.6
Flask-WTF>=1.2
WTForms>=3.1
Werkzeug>=3.0
SQLAlchemy>=2.0
psycopg2-binary>=2.9
pytest>=8.0
pytest-flask>=1.3
factory-boy>=3.3
```

---

### Run Instructions

```bash
pip install -r requirements.txt

# Dev (SQLite)
python app.py

# Prod (PostgreSQL)
APP_ENV=prod DATABASE_URL=postgresql://user:pass@localhost/teamdb python app.py

# Migrations
flask db init && flask db migrate -m "initial" && flask db upgrade

# Tests
pytest
```

App: **http://localhost:8765**

---

### Acceptance Criteria

**Functional**
- [ ] `python app.py` starts on port **8765** with zero errors.
- [ ] Login with `demo` / `demo` works and shows the dashboard.
- [ ] Full CRUD works for Developers and Tasks.
- [ ] A task can be assigned / reassigned to a developer.
- [ ] Deleting a developer does not delete their tasks (tasks become unassigned).
- [ ] Form validation errors shown inline in red.
- [ ] Flash messages display after every create / update / delete.
- [ ] `pytest` passes with zero failures.

**UI / Dark Mode**
- [ ] All pages use dark background (`#0f1117`) — no white or light-grey panels anywhere.
- [ ] Sidebar layout is present on all authenticated pages (not a top navbar).
- [ ] Active sidebar link is highlighted in accent color (`#6366f1`).
- [ ] Font is Inter, loaded from Google Fonts.
- [ ] Status badges use the pill style with colored text (not plain Bootstrap badges).
- [ ] Dashboard shows four stat cards with icons.
- [ ] Login page is a centered card on a dark background.
- [ ] Empty states (no developers, no tasks) show a friendly icon + message.
- [ ] Delete confirmation page uses the `.confirm-card` layout.
- [ ] Tables have uppercase muted headers and subtle row hover effect.
- [ ] No raw Bootstrap default colors visible — all overridden by `theme.css`.
