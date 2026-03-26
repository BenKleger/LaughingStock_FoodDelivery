# Build
FROM python:3.11
WORKDIR /app/backend

# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy in the source code
COPY Backend ./backend
# COPY Frontend ./frontend
EXPOSE 8080

CMD ["python", "backend/main.py"]

# compliments of https://docs.docker.com/get-started/docker-concepts/building-images/writing-a-dockerfile/#:~:text=Next%20steps-,Explanation,%2C%20startup%20command%2C%20and%20more.