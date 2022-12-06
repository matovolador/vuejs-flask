FROM python:3.8.10


# set environment variables
ENV DEBIAN_FRONTEND noninteractive
ENV GECKODRIVER_VER v0.31.0
ENV FIREFOX_VER 97.0
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN set -x \
   && apt update \
   && apt upgrade -y \
   && apt install -y \
            nano

# Install cron
RUN set -x \
   && apt install -y cron

# Copy hello-cron file to the cron.d directory
COPY cron-jobs /etc/cron.d/cron-jobs
 
# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/cron-jobs

# Apply cron job
RUN crontab /etc/cron.d/cron-jobs
 
# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# set work directory
RUN mkdir /app
WORKDIR /app

# copy files
COPY . /app/

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN chmod +x ./start_app.sh
RUN chmod +x ./tests.sh
RUN chmod +x ./wait-for-it.sh


EXPOSE 5050