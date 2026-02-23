# Use slim python base image
FROM python:3.12-slim

# Set working directory 
WORKDIR /app

# Prevent python from writing pyc files & enable stdout logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (only if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy entry point script (if you have one, adjust as needed)
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' entrypoint.sh  # Remove potential Windows line endings
RUN chmod +x entrypoint.sh

# Set entrypoint
ENTRYPOINT ["./entrypoint.sh"]

# Copy application code
COPY . .

# Expose port(change if needed)
EXPOSE 8000

#Default command to run the application (adjust if using a different server or command)
CMD ["python", "main.py"]