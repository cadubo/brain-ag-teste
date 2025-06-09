FROM python:3.9-slim

WORKDIR /app

COPY app/ /app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

CMD ["gunicorn", "-c", "gunicorn.conf.py", "app:app"]
