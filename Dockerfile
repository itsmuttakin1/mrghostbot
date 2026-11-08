FROM python:3.11-slim

# Install system dependencies:
# ffmpeg: audio/video merging and conversion
# curl: healthchecks and fetching
# nodejs: solves YouTube BotGuard PO (Proof of Origin) tokens on servers
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    curl \
    nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Start bot and web server
CMD ["python", "bot.py"]

