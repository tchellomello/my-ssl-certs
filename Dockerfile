FROM fedora:27
MAINTAINER Marcelo Moreira de Mello <tchello.mello@gmail.com>

ENV PORT 8000

# create django-app user
RUN useradd django-app

# update and install dependencies
RUN dnf clean all && \
    dnf -y update && \
    dnf -y install python3 python3-devel python3-pip git \
    python3-virtualenv sqlite openssl-devel && \
    dnf clean all


# create directory and mount sources there
ADD start.sh requirements.txt mysslcerts /home/django-app/code/ 
RUN chmod +x /home/django-app/code/start.sh
ADD .bashrc /home/django-app/
RUN chown django-app:django-app -R /home/django-app

# set user
USER django-app
RUN /usr/bin/py3-virtualenv -p python3.6 /home/django-app/.virtualenv

# set workdir
WORKDIR /home/django-app/code

# export volume
VOLUME /home/django-app/code

# expose 8000 port
EXPOSE ${PORT}

# define command to start container
ENTRYPOINT ["/bin/bash", "/home/django-app/code/start.sh"]
