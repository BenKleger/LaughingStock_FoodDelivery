# Build
FROM python:3.11
WORKDIR /app

# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy in the source code
COPY Backend ./backend
# COPY Frontend ./frontend
EXPOSE 8080

# Setup an app user so the container doesn't run as the root user
RUN useradd app
USER app

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]

# compliments of https://docs.docker.com/get-started/docker-concepts/building-images/writing-a-dockerfile/#:~:text=Next%20steps-,Explanation,%2C%20startup%20command%2C%20and%20more.