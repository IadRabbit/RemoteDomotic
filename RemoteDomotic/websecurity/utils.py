from requests import get
from wave import open as wav_open
from APIwebsecurity.utils import tapo
from RemoteDomotic.settings import BASE_DIR
from requests.exceptions import ConnectTimeout, ConnectionError

empty_wav = f"{BASE_DIR}/RemoteDomotic/static/img/empty.wav"
b_empty_wav = wav_open(empty_wav, "rb")
default_chunk = 2048
default_data = b_empty_wav.readframes(default_chunk)

def is_root(user):
	is_root = user.permissions.filter(permission = "root")

	data = {
		"is_root": is_root.exists()
	}

	return data

def gen_video(camera):
	while True:
		frame = camera.get_frame()

		yield(
			b"--frame\r\n"
			b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n"
		)

def gen_audio(audio, domain):
	while True:
		try:
			audio_frame = get(
				audio,
				timeout = 1,
				stream = True
			).iter_content(default_chunk)

			for chuck in audio_frame:
				yield chuck
		except (ConnectionError, ConnectTimeout):
			c_data = b_empty_wav.readframes(default_chunk)

			while c_data != b"":
				c_data = b_empty_wav.readframes(default_chunk)
				yield c_data

		#yield audio_frame

	"""
	yield audio.wav_header

	while True:
		try:
			data = audio.stream.read(audio.chunk)
			yield data
		except AttributeError:
			break
	"""

def get_url_webcam_audio(webcam):
	manufacturer = webcam.id_manufacturer
	protocol = manufacturer.protocol
	audio_path = manufacturer.audio_path

	if not webcam.user:
		url = f"{protocol}://{webcam.ip}:{webcam.port}/{audio_path}"
	else:
		url = f"{protocol}://{webcam.user}:{webcam.password}"
		url += f"@{webcam.ip}:{webcam.port}/{audio_path}"

	return url

def get_url_webcam(webcam):
	manufacturer = webcam.id_manufacturer
	protocol = manufacturer.protocol
	video_path = manufacturer.video_path

	if not webcam.user:
		url = f"{protocol}://{webcam.ip}:{webcam.port}/{video_path}"
	else:
		url = f"{protocol}://{webcam.user}:{webcam.password}"
		url += f"@{webcam.ip}:{webcam.port}/{video_path}"

	return url

def get_webcams_user(user, room = None):
	webcams = user.belongs.filter(id_category__category = "WebCam")

	if room:
		webcams = webcams.filter(id_room__room = room)

	return webcams

def get_rooms_user(user):
	user_belongs = user.belongs.all()
	rooms = []

	for room in user_belongs:
		name_room = room.id_room

		if not name_room in rooms:
			rooms.append(name_room)

	return rooms

def get_devices_user_by_room(user, room):
	user_belongs = user.belongs.filter(id_room__room = room)
	return user_belongs

def get_lamps_user(user, room = None):
	lamps = user.belongs.filter(id_category__category = "Lamp")

	if room:
		lamps = lamps.filter(id_room__room = room)

	for lamp in lamps:
		try:
			tap = tapo(lamp.ip, lamp.id_manufacturer)
			status, hue, brightness = tap.getStatus()
			lamp.is_on = status
			lamp.hue = hue
			lamp.brightness = brightness
		except (ConnectTimeout, ConnectionError):
			lamp.is_on = False
			lamp.hue = 0
			lamp.brightness = 0

	return lamps