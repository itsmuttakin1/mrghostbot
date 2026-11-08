FROM python:3.11-slim

# Install system dependencies (ffmpeg is essential for yt-dlp)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose default web server port
EXPOSE 10000

# Start bot and web server
CMD ["python", "bot.py"]

