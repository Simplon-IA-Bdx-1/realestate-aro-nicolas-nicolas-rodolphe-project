FROM python:3.7-buster

WORKDIR /app

ADD . /app
RUN pip install -r requirements.txt

EXPOSE 5000

CMD [ "gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "run:app"]