FROM ubuntu:xenial
RUN \
    apt-get update -qq --fix-missing && \
    apt-get install -qqy \
        wget \
        curl \
        git \
        bzip2 \
        httrack \
        libmemcached-dev \
        libpq-dev \
        libxslt1-dev \
        libxslt1.1 \
        libjpeg-dev \
        libffi-dev \
        libssl1.0.0 \
        libssl-dev \
        gettext \
        nano \
        python3 \
        python3-dev \
        python-distribute \
        python3-lxml \
        python3-openssl \
        python3-pip \
        supervisor \
        libfreetype6 \
        libfontconfig \
# for psql commandline tool
        postgresql-client-9.5 \
#        {more_packages} \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED 1
ENV C_FORCE_ROOT true
RUN mkdir /src
RUN mkdir /static
WORKDIR /src
ADD ./src /src
RUN pip3 install -r requirements.pip
CMD python3 manage.py collectstatic --no-input;python3 manage.py migrate; gunicorn  mydjango.wsgi -b 0.0.0.0:8000
#& celery worker --app=myapp.tasks
#https://github.com/jvranish/docker-https-ssh-tunnel