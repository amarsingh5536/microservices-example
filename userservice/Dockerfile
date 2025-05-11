FROM python:3.10
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y supervisor
COPY supervisor/bootstrap.conf /etc/supervisor/conf.d/bootstrap.conf
COPY supervisor/start_subscriber.sh /etc/supervisor/conf.d/start_subscriber.sh
RUN chmod +rx /etc/supervisor/conf.d/start_subscriber.sh

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/

COPY . .

RUN pip install -r requirements.txt

RUN mkdir /static

EXPOSE 80
CMD [ "sh", "entrypoint.sh"]
