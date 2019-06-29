FROM ubuntu:16.04

MAINTAINER Your Name "hardord.sheen@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

COPY ./requirements.txt /hashen/requirements.txt

WORKDIR /hashen

RUN pip install -r requirements.txt

COPY . /hashen

ENTRYPOINT [ "bash" ]

CMD [ "run.sh" ]
