FROM python:3.6
WORKDIR /app
ADD . /app
RUN apt-get update && apt-get -y install cron && pip install --requirement ./requirements.txt
COPY . ./
ENV DJANGO_SETTINGS_MODULE=world_cup_predictions.settings
RUN (crontab -l ; echo "00 22 * * * python update_users_scores.py") | crontab
CMD ["crond", "-f", "-d", "8"]
EXPOSE 8000