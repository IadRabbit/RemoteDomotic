from gtts.lang import tts_langs
from .camera import VideoCamera
from django.shortcuts import redirect, render
from APIwebsecurity.utils import get_audio_user
from .decorators import is_post, is_authenticated
from django.contrib.auth.decorators import login_required
from django.http.response import Http404, StreamingHttpResponse

from .utils import (
	get_url_webcam, is_root, gen_video, gen_audio,
	get_webcams_user, get_rooms_user,
	get_devices_user_by_room, get_lamps_user, get_url_webcam_audio
)

from APIwebsecurity.views import (
	auth as APIauth,
	logout as APIlogout,
	upload_audio as APIupload_audio,
	playaudio as APIplayaudio,
	del_audio as APIdel_audio,
	turn_lamp as APIturn_lamp,
	color_lamp as APIcolor_lamp,
	save_gtts as APIsave_gtts
)

@login_required
def index(request):
	user = request.user
	data = is_root(user)
	audios = get_audio_user(user)
	data['audios'] = audios
	data['commands'] = audios.filter(command__isnull = False)
	data['webcams'] = get_webcams_user(user)
	data['rooms'] = get_rooms_user(user)
	data['lamps'] = get_lamps_user(user)

	return render(
		request, "websecurity/index.html", data
	)

@is_authenticated
def login(request):
	return render(request, "websecurity/login.html")

@is_post
def auth(request):
	data = APIauth(request)
	return data

@login_required
def logout(request):
	APIlogout(request)
	return redirect(login)

@login_required
@is_post
def upload_audio(request):
	data = APIupload_audio(request)
	return data

@login_required
def records(request):
	user = request.user
	data = is_root(user)
	data['rooms'] = get_rooms_user(user)
	data['langs'] = tts_langs().items()
	data['lang'] = request.LANGUAGE_CODE

	return render(
		request, "websecurity/records.html", data
	)

@login_required
@is_post
def playaudio(request):
	data = APIplayaudio(request)
	return data

@login_required
def my_audios(request):
	user = request.user
	data = is_root(user)
	data['audios'] = get_audio_user(user)
	data['rooms'] = get_rooms_user(user)

	return render(
		request, "websecurity/my_audios.html", data
	)

@login_required
def video_feed(request, video):
	user = request.user
	webcams = get_webcams_user(user)
	is_belong = webcams.filter(device = video)

	if is_belong:
		video = get_url_webcam(is_belong[0])

	return StreamingHttpResponse(
		gen_video(
			VideoCamera(video, is_belong.exists())
		),
		content_type = "multipart/x-mixed-replace; boundary=frame"
	)

@login_required
@is_post
def del_audio(request):
	data = APIdel_audio(request)
	return data

@login_required
def audio_feed(request, audio):
	user = request.user
	webcams = get_webcams_user(user)
	is_belong = webcams.filter(device = audio)
	domain = request.META['HTTP_HOST']
	url = f"http://{domain}/media/audios/empty.wav"

	if is_belong:
		audio = get_url_webcam_audio(is_belong[0])

	return StreamingHttpResponse(
		gen_audio(audio, url),
		content_type = "audio/x-wav"
	)

@login_required
def room(request, room):
	user = request.user
	data = is_root(user)
	data['devices'] = get_devices_user_by_room(user, room)

	if len(data['devices']) == 0:
		raise Http404

	data['rooms'] = get_rooms_user(user)
	data['webcams'] = get_webcams_user(user, room)
	data['room'] = room
	data['lamps'] = get_lamps_user(user, room)

	return render(
		request, "websecurity/room.html", data
	)

@login_required
@is_post
def turn_lamp(request):
	data = APIturn_lamp(request)
	return data

@login_required
@is_post
def color_lamp(request):
	data = APIcolor_lamp(request)
	return data

@login_required
@is_post
def save_gtts(request):
	data = APIsave_gtts(request)
	return data