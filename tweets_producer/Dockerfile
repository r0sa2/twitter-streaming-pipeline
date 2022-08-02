FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt main.py ./

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "main.py"]