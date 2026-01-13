FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements_web.txt .
RUN pip install --no-cache-dir -r requirements_web.txt

# Copy app files
COPY . .

# Create config if not exists
RUN echo '{"video_url": "", "amount_of_boosts": 100, "type": "views"}' > config.json

EXPOSE $PORT

CMD ["python", "app.py"]