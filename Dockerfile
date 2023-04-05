FROM python:3.10.10-slim-buster

RUN mkdir /code

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

#CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=443", "--ssl-keyfile=./ahris-ninja-key.pem", "--ssl-certfile=./ahris-ninja-cert.pem"]

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=5000"]
