FROM python:3.12-slim

WORKDIR /emptyLeg

COPY requrements.txt .
RUN pip install --no-cache-dir -r requrements.txt

COPY . .

CMD ["python", "main.py"]