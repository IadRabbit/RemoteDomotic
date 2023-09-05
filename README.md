# RemoteDomotic

## Story
This repository contain the project I needed to realize & present to the examination board in June 2021. This is one of my favourite project I ever made that made me spark during my exam. The board (my teachers included) was very happy to see such project made by one of their pupils. Theoretically the max score I could achieve was 99/100, but gave the success of my presentation (I think helped also presenting it in english instead of italian). I achieved & fulfilled by high school with 100/100. Wonderful.

## Currently
I wanted to publish this project on GitHub long time ago, but never found the time for writing a proper README.
The original configuration is a bit more intricate, for this I realized a Docker Compose file (working only for linux due some audio stuff) that deploy faster the webapp & webserver. Instead of manually transfer folders & fixing possible webserver configuration & enviroment configs.

## Info
Inside `docs/` folder there are some images I used to write the project paper.
This is a simple webapp wrote using Django Framework, with some REST API and basic HTML/JS/CSS.
The main purpose of this app is managing IoT devices inside your home network Wi-Fi. I managed to integrate [Tapo Bulbs](https://www.amazon.it/TP-Link-Intelligente-Multicolore-Tapo-L530E/dp/B08GDC99PX/ref=sr_1_1?qid=1693932179&refinements=p_89%3ATP-Link&s=lighting&sr=1-1) & Camera Streaming using [IP Webcam](https://play.google.com/store/apps/details?id=com.pas.webcam&hl=it&gl=US) app.
The DB is a simple SQLite. There is also a scammy 'feature' that allow talking directly with Alexa. The only thing is for doing that uses a rough method that at the time in my mind looked very cool. In the end Alexa just need to hear his name pronounced, so why don't make pronounce 'Alexa' from a PC speaker? :). I also think that this is a very cool method to scare a possible thief entering in your house that you saw from the Surveillance Camera. You can do this by recording your voice from the webapp or write some text that after is gonna be converted in audio.

## Configuration
```bash
git clone https://github.com/iadrabbit/RemoteDomotic
```

Then

```bash
cd RemoteDomotic && docker compose up
```

If is the first time that you UP the compose, we need to create an user & some permissions

```bash
docker compose exec -it remotedomotic_webapp /bin/bash
```

then

```bash
python3 manage.py shell < first_to_run.py && python3 manage.py createsuperuser
```

Go at http://localhost:8000/. I hope you find it cool