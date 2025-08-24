FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y build-essential cargo rustc libffi-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /emptyLeg

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]