FROM python:3.9.13-buster

# Port for Flask
EXPOSE 5000

RUN mkdir -p /usr/local/src/reminders
WORKDIR /usr/local/src/reminders

RUN apt-get update && \
      apt-get -y install sudo

# Install core dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Install Dev dependencies
COPY requirements-dev.txt .
RUN pip3 install -r requirements-dev.txt

ENV FLASK_APP=src/api

# Copy source code
COPY . .

CMD [ "./docker-entrypoint.sh" ]