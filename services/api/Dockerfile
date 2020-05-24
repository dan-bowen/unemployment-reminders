FROM python:3.7.4-buster

# Port for Flask
EXPOSE 5000

RUN mkdir -p /usr/local/src/reminders
WORKDIR /usr/local/src/reminders

RUN apt-get update && \
      apt-get -y install sudo

# Install Node
RUN curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash - && \
    sudo apt-get install -y nodejs

# Install local NPM dependencies
COPY package.json ./
RUN npm install

# Install serverless
RUN npm install -g serverless

# Install core dependencies
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

# Install Dev dependencies
COPY requirements-dev.txt ./
RUN pip3 install -r requirements-dev.txt

ENV FLASK_APP=api

# Copy source code
COPY . .

CMD [ "./docker-entrypoint.sh" ]