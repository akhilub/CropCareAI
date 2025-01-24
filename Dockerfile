FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libhdf5-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Pillow for image processing
RUN pip install --no-cache-dir Pillow

# Update Flask, Jinja2, and MarkupSafe
RUN pip install --no-cache-dir --upgrade flask jinja2 markupsafe

# Create uploads directory and set permissions
RUN mkdir -p /app/uploads && chmod 777 /app/uploads

COPY . .

# CMD ["python", "app.py"]

EXPOSE 7860

CMD ["python", "-c", "import app; app.app.run(host='0.0.0.0', port=7860)"]



