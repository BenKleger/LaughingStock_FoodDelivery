# Build
FROM python:3.11-slim
WORKDIR /app

# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy in the source code
COPY . .

EXPOSE 8080


# Setup an app user so the container doesn't run as the root user
RUN useradd app
USER app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

# compliments of https://docs.docker.com/get-started/docker-concepts/building-images/writing-a-dockerfile