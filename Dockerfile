FROM python:3.6
WORKDIR /app
ADD . /app
RUN pip install --requirement ./requirements.txt
COPY . ./
ENV DJANGO_SETTINGS_MODULE=world_cup_predictions.settings
EXPOSE 8000