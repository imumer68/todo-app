# Use official slim Python runtime
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy dependency list and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port App Runner will use
EXPOSE 5000

# Start the Flask app
CMD ["python", "application.py"]
