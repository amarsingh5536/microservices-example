# Use the official Python image
FROM python:3.10

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

COPY . .

COPY requirements.txt /code/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD [ "sh", "entrypoint.sh"]
