# syntax=docker/dockerfile:1

FROM python:3.10.4

RUN mkdir -p /usr/scr/test_docker/
WORKDIR /usr/scr/test_docker/

COPY . /usr/scr/test_docker/
RUN pip install --no-cache-dir -r requirements.txt

COPY . . 

CMD ["python","main_bot.py"]