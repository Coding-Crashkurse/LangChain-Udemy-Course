FROM python:3.13-slim

# Copy the uv binary from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# install postgresql client (psql is used by wait-for-postgres.sh)
RUN apt-get update && apt-get install -y --no-install-recommends postgresql-client && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Install the locked dependencies first (psycopg[binary] ships libpq)
COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --locked --no-install-project

COPY . /app

ENV PATH="/app/.venv/bin:$PATH"

# Copy wait-for-postgres.sh and make it executable
COPY ./wait-for-postgres.sh /wait-for-postgres.sh
RUN sed -i 's/\r$//' /wait-for-postgres.sh && chmod +x /wait-for-postgres.sh

EXPOSE 80

CMD ["/wait-for-postgres.sh", "postgres", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
