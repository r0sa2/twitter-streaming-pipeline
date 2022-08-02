FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt main.py tokenizer.pickle model.hdf5 ./

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "main.py"]