# super tiny
FROM alpine

# Install python
RUN apk update && apk add python3

# copy code/templates to container
COPY ./ /opt/web

# switch to web dir
WORKDIR /opt/web

# install python deps
RUN pip3 install -r requirements.txt

# Expose the web port
EXPOSE 5000

# start the webserver
CMD python3 manager.py runserver -h 0.0.0.0
