# syntax=docker/dockerfile:1
FROM python:3.11-slim-bookworm
RUN apt-get update && apt-get install -y apt-transport-https ca-certificates sqlite3
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["python3", "-m", "flask", "run"]