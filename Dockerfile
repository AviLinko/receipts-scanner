
FROM python:3.9-slim


ENV PYTHONUNBUFFERED=1


WORKDIR /app


COPY requirements.txt /app/requirements.txt


RUN pip install --no-cache-dir -r requirements.txt


COPY . /app


ENV GOOGLE_VISION_KEY_PATH=/app/services/google-vision-key.json


EXPOSE 5000


CMD ["python", "app.py"]
