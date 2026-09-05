# -------------------------------------------------------------------
# Base Image with uv pre-installed (Python 3.13 slim)
# -------------------------------------------------------------------
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS base

# Set working directory
WORKDIR /app

# Configure Python and uv environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

# -------------------------------------------------------------------
# Dependency Installation (Layer caching)
# -------------------------------------------------------------------
# Copy dependency manifests first
COPY pyproject.toml uv.lock ./

# Install dependencies into virtual environment
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# -------------------------------------------------------------------
# Application Code & Setup
# -------------------------------------------------------------------
# Copy project files
COPY . .

# Final sync to install the project itself if packaged
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Create media and static directories
RUN mkdir -p /app/media /app/static

# Collect static files for WhiteNoise/production serving
RUN python manage.py collectstatic --noinput

# Expose port 8000
EXPOSE 8000

# Production startup command using Gunicorn WSGI server
CMD ["gunicorn", "blog_main.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
