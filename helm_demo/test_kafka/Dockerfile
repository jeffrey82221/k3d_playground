FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY test.py .
COPY producer.py .
# Run the producer
# Use -u flag for unbuffered output
CMD ["python", "-u", "producer.py"]