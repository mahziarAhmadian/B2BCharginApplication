# Dockerfiles/backend/Dockerfile

FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Copy the start script
COPY scripts/start.sh /app/scripts/start.sh

# Make the script executable
RUN chmod +x /app/scripts/start.sh

# Set the command to run the script
CMD ["/app/scripts/start.sh"]
