from .settings import BASE_DIR
from websecurity.models import Commands
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

wav = f"{BASE_DIR}/RemoteDomotic/static/img/empty.wav"
f = open(wav, "rb")
empty_content = f.read()
f.close()
empty_resp = HttpResponse()
empty_resp.write(empty_content)
empty_resp['Content-Type'] = "audio/wav"

def index(request):
	return redirect("/websecurity")

def empty_wav():
	return empty_resp

@login_required
def audio_manage(request, audio):
	if audio == "empty.wav":
		return empty_wav()

	path = "audios/%s" % audio
	audio = Commands.objects.filter(audio = path)

	if not audio:
		raise PermissionDenied

	audio = audio[0]
	audio_user = audio.id_user
	audio_user_id = audio_user.id
	logged_user = request.user
	logged_user_id = logged_user.id
	permissions = logged_user.permissions
	is_able = permissions.filter(permission = "root")

	if (is_able) or (logged_user_id == audio_user_id):
		audio_play = audio.audio
		audio_path = audio_play.path
		f = open(audio_path, "rb")
		content = f.read()
		f.close()
		resp = HttpResponse()
		resp.write(content)
		resp['Content-Type'] = "audio/wav"
	else:
		raise PermissionDenied

	return resp

def error_403(request, exception):
	return render(request, "error_403.html")

def error_404(request, exception):
	return render(request, "error_404.html")