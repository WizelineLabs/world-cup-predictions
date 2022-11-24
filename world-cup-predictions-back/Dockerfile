FROM ubuntu:bionic
WORKDIR /app
RUN apt-get update && \
    apt-get install --no-install-recommends -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3.7 python3.7-distutils python3.7-dev default-libmysqlclient-dev build-essential curl && \
    curl -k https://bootstrap.pypa.io/get-pip.py | python3.7 && \
    rm -rf /var/lib/apt/lists/* && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.7 2
ADD ./requirements.txt /app/requirements.txt
RUN pip install -r ./requirements.txt
RUN pip install mysqlclient

ADD . /app

ENV GOOGLE_OAUTH2_KEY=266500404779-69r7af0h79i0jck1l1vdsnjlqvs9i4s5.apps.googleusercontent.com
ENV GOOGLE_OAUTH2_SECRET=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

ENV DJANGO_SETTINGS_MODULE=world_cup_predictions.settings
EXPOSE 8000