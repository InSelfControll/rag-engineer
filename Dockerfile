FROM python:3.12-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install dependencies
COPY . .
RUN uv pip install -r requirements.txt --no-cache --system

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "main.py"]
