FROM nginx:1.22.1

RUN apt update
RUN apt install vim -y

WORKDIR /etc/nginx/

COPY docker_files/webserver_files/ .

WORKDIR /etc/nginx/conf.d/