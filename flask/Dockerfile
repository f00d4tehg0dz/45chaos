FROM ubuntu

# Install deps
RUN apt-get update
RUN apt-get -y install python3 python3-pip python3-dev build-essential apache2 apache2-dev

# copy code/templates to container
COPY ./ /opt/web

# switch to web dir
WORKDIR /opt/web

# install extra python deps
RUN pip3 install -r requirements.txt
RUN pip3 install uwsgi mod_wsgi

# Expose the web port
EXPOSE 5000

# start the webserver
CMD uwsgi mooches.ini
