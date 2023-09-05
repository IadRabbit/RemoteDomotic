FROM python:3.9
RUN apt update
RUN apt install vim portaudio19-dev python3-opencv alsa-utils vlc python3-pip apache2 libapache2-mod-wsgi-py3 -y

WORKDIR /app
COPY RemoteDomotic .
RUN pip install --no-cache-dir -r req.txt