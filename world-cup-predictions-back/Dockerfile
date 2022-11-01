FROM ubuntu:bionic
WORKDIR /app

RUN apt-get update && \
    apt-get install --no-install-recommends -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3.8 python3.8-distutils libmysqlclient-dev python3.8-dev python3-venv python3-markupsafe build-essential curl && \
    curl -k https://bootstrap.pypa.io/get-pip.py | python3.8 && \
    rm -rf /var/lib/apt/lists/* 

RUN pip3 install virtualenv

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN python3 -m pip install Cython 

ADD ./requirements.txt /app/requirements.txt
RUN pip3 install -r ./requirements.txt

RUN pip3 install numpy
RUN pip3 install pandas
RUN pip3 install scipy

ADD . /app
ENV DJANGO_SETTINGS_MODULE=world_cup_predictions.settings
EXPOSE 8000