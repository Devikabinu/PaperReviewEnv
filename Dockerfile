FROM python:3.10-slim

WORKDIR /app

COPY . /app

# Run a simple HTTP server to keep the Docker container running and satisfy HF Spaces
EXPOSE 7860
CMD ["python", "-m", "http.server", "7860"]
