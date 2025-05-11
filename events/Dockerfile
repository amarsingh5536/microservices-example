FROM python:3.10
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y supervisor
COPY supervisor/bootstrap.conf /etc/supervisor/conf.d/bootstrap.conf
COPY supervisor/start_subscriber.sh /etc/supervisor/conf.d/start_subscriber.sh
RUN chmod +rx /etc/supervisor/conf.d/start_subscriber.sh

RUN mkdir /code
WORKDIR /code
COPY . .
COPY requirements.txt /code/

# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt

EXPOSE 80
CMD [ "sh", "entrypoint.sh"]
