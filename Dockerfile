FROM fedora
MAINTAINER http://fedoraproject.org/wiki/Cloud

RUN dnf clean all && \
    dnf -y update && \
    dnf -y install python3 python3-devel python3-pip git \
    python3-virtualenv sqlite python-psycopg2 \
    openssl-devel && dnf clean all

COPY mysslcerts /code  
RUN pip install -r /code/mysslcerts/requirements.txt

# create directory /code and mount sources there
RUN mkdir /code
WORKDIR /code
VOLUME /code

EXPOSE 8000

CMD python mysslcerts/manage.py runserver 0.0.0.0:8000
