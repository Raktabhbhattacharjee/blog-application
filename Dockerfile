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

# Install dependencies into virtual environment (excluding dev dependencies)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# -------------------------------------------------------------------
# Application Code & Setup
# -------------------------------------------------------------------
# Copy project files
COPY . .

# Final sync to install the project itself if package
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Create media and static directories with proper permissions
RUN mkdir -p /app/media /app/static

# Expose port
EXPOSE 8000

# Default startup command (runs migrations, collects static, starts server)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
