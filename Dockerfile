FROM python:3-slim

ENV PORT=443

COPY . /flask-gpt
WORKDIR /flask-gpt

RUN pip install -r requirements.txt

EXPOSE $PORT

CMD gunicorn app:app -b 0.0.0.0:$PORT