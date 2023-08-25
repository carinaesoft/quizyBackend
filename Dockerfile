# Use Python 3.11
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    zlib1g-dev \
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app/

# Install required packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application using gunicorn
CMD ["gunicorn", "quizyBackend.wsgi:application", "--bind", "0.0.0.0:8000"]
