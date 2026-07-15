FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY sender.py .

COPY users.csv .

CMD ["python","sender.py"]
