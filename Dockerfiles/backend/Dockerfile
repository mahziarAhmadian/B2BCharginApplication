# Dockerfiles/backend/Dockerfile

FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/
#COPY ./Dockerfiles/backend/scripts.sh /app/scripts.sh
RUN chmod +x ./Dockerfiles/backend/scripts.sh
ENTRYPOINT ["./Dockerfiles/backend/scripts.sh"]
