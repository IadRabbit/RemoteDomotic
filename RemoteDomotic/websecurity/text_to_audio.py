from gtts import gTTS
from uuid import uuid4
from RemoteDomotic.settings import BASE_DIR

def transform(text, lang):
	gt = gTTS(text, lang = lang)
	wav = f"audios/{uuid4()}.mp3"
	gt.save(f"{BASE_DIR}/media/{wav}")
	return wav