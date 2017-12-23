FROM python:3.6.2-alpine3.6


COPY requirements.txt .
COPY download.py .
COPY upload.py .

RUN apk add --no-cache gcc musl-dev linux-headers && pip install -r requirements.txt


CMD python download.py
