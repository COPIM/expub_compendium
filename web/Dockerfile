# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster
RUN apt update && apt install -y apt-transport-https ca-certificates sqlite3
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["python3", "-m", "flask", "run"]
