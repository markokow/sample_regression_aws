# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements_prod.txt .

# Install the dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements_prod.txt

# Copy the rest of the application code into the container
COPY . .

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/app/src

# CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
