FROM python:3.10
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y supervisor && apt-get -y install cron

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/

COPY . .

RUN pip install -r requirements.txt

RUN mkdir /static

EXPOSE 80
CMD [ "sh", "entrypoint.sh"]
