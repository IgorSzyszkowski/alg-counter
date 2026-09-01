FROM python:3.12-slim-bookworm

COPY --from=docker.io/astral/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project

COPY . .

RUN uv sync --frozen

ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["alg-counter"]