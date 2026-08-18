FROM python:3.12-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml .
COPY uv.lock .

RUN uv sync --frozen --no-dev

COPY ingestion/ ./ingestion/
COPY rag/ ./rag/
COPY api/ ./api/
COPY transform/ ./transform/

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]