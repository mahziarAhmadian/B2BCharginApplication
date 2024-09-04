# Dockerfiles/backend/Dockerfile

FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Set the command to run the project
CMD ["python","manage.py","runserver","0.0.0.0:6565"]
