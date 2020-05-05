FROM python:buster

RUN mkdir -p /data
RUN apt update && apt -y upgrade && apt install -y socat

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD /app/docker_entrypoint.sh
