from .playsound import play_sound
from django.http import JsonResponse
from PyP100.exceptions import TapoError
from json.decoder import JSONDecodeError
from .utils import get_audio_user, select_way
from websecurity.models import Commands, Users
from django.core.exceptions import ValidationError
from requests.exceptions import ConnectTimeout, ConnectionError

from django.contrib.auth import (
	authenticate, login, logout
)

from .decorators import (
	is_post, is_login,
	is_file, is_audio,
	is_command, is_lamp,
	is_hue, is_gtts
)

@is_post
def auth(request):
	data = {}
	params = request.POST
	username = params['username']
	password = params['password']

	exist = Users.objects.filter(
		username = username,
		tries__gt = 0
	)

	if not exist:
		data['success'] = False
		status = 401
	else:
		user = authenticate(
			request,
			username = username,
			password = password
		)

		if user:
			login(request, user)
			data['success'] = True

			if "next" in params:
				redirection = params['next']
			else:
				redirection = "/websecurity/index/"

			data['redirect'] = redirection
			status = 200
		else:
			tries = exist[0].tries - 1
			exist.update(tries = tries)
			data['tries_available'] = tries
			data['success'] = False
			status = 401

	return JsonResponse(data, status = status)

@is_login
def logout_view(request):
	logout(request)

	data = {
		"success": True
	}

	return JsonResponse(data, status = 200)

@is_login
@is_post
@is_file
def upload_audio(request):
	posts = request.POST
	description = posts['description']
	command = posts['command']
	file = request.FILES['audio']
	user = request.user

	exist = Commands.objects.filter(
		id_user = user,
		command = command
	)

	data = {
		"success": False
	}

	if exist:
		status = 406
		c_command = exist[0].command
		data['msg'] = f"The command \"{c_command}\" is already assigned to another"
		return JsonResponse(data, status = status)

	audio = Commands(
		id_user = user,
		description = description,
		command = command,
		audio = file
	)

	try:
		audio.save()
		data['success'] = True
		status = 200
	except ValidationError as msg:
		data['msg'] = msg.message
		status = 403

	return JsonResponse(data, status = status)

@is_login
@is_post
@is_audio
def playaudio(request):
	id_audio = request.POST['id_audio']
	user = request.user

	audio = get_audio_user(user).filter(
		id = id_audio
	)

	data = {}

	if audio:
		audio_play = audio[0].audio
		audio_path = audio_play.path
		play_sound(audio_path)
		data['success'] = True
		status = 200
	else:
		data['success'] = False
		data['msg'] = "WHAT ARE YOU TRYING TO DO? =)"
		status = 403

	return JsonResponse(data, status = status)

@is_login
@is_post
@is_audio
def del_audio(request):
	id_audio = request.POST['id_audio']
	user = request.user

	audio = get_audio_user(user).filter(
		id = id_audio
	)

	data = {}

	if audio:
		audio_play = audio[0]
		audio_play.delete()
		data['success'] = True
		status = 200
	else:
		data['success'] = False
		data['msg'] = "WHAT ARE YOU TRYING TO DO? =)"
		status = 403

	return JsonResponse(data, status = status)

@is_login
def get_audios(request):
	user = request.user
	commandss = get_audio_user(user)

	data = {
		"results": {
			"commands": [],
			"commands_list": []
		}
	}

	results = data['results']
	commands = results['commands']
	commands_list = results['commands_list']

	for command in commandss:
		com = command.command

		c_data = {
			"description": command.description,
			"language": command.language,
			"text": command.text,
			"command": com,
			"audio": command.audio.url
		}

		if com:
			commands_list.append(com)

		commands.append(c_data)

	status = 200
	return JsonResponse(data, status = status)

@is_login
@is_post
@is_command
def play_command(request):
	command = request.POST['command']
	user = request.user

	audio = get_audio_user(user).filter(
		command = command
	)

	data = {}

	if audio:
		audio_play = audio[0].audio
		audio_path = audio_play.path
		play_sound(audio_path)
		data['success'] = True
		status = 200
	else:
		data['success'] = False
		data['msg'] = "WHAT ARE YOU TRYING TO DO? =)"
		status = 403

	return JsonResponse(data, status = status)

@is_login
@is_post
@is_lamp
def turn_lamp(request):
	id_device = request.POST['id_device']
	user = request.user

	device = user.belongs.filter(
		id = id_device,
		id_category__category = "Lamp"
	)

	data = {
		"success": False
	}

	if device:
		device = device[0]

		try:
			status, hue, brightness = select_way(device, "status")
			data['success'] = True

			if status:
				msg = "OFF"
			else:
				msg = "ON"

			data['msg'] = f"THE {device.device} HAS BEEN TURNED {msg}"
			data['status'] = status
			status = 200
		except (ConnectTimeout, ConnectionError):
			data['msg'] = "THE DEVICE IS OFFLINE AT THE MOMENT"
			status = 404
	else:
		data['msg'] = "WHAT ARE YOU TRYING TO DO? =)"
		status = 403

	return JsonResponse(data, status = status)

@is_login
@is_post
@is_hue
def color_lamp(request):
	posts = request.POST
	id_device = posts['id_device']
	hue = int(posts['hue'])
	brightness = int(posts['brightness'])
	user = request.user

	device = user.belongs.filter(
		id = id_device,
		id_category__category = "Lamp"
	)

	data = {
		"success": False
	}

	if device:
		device = device[0]

		try:
			select_way(device, "change_hue", hue, brightness)
			data['success'] = True
			data['msg'] = "COLOR CHANGED"
			status = 200
		except JSONDecodeError:
			data['msg'] = "RETRY IN A FEW SECONDS"
			status = 403
		except TapoError:
			data['msg'] = "INVALID PARAMS"
			status = 405
		except (ConnectTimeout, ConnectionError):
			data['msg'] = "THE DEVICE IS OFFLINE AT THE MOMENT"
			status = 404
	else:
		data['msg'] = "WHAT ARE YOU TRYING TO DO? =)"
		status = 403

	return JsonResponse(data, status = status)

@is_login
@is_post
@is_gtts
def save_gtts(request):
	posts = request.POST
	description = posts['audio_description']
	language = posts['audio_lang']
	text = posts['audio_text']
	command = posts['audio_command']
	user = request.user

	exist = Commands.objects.filter(
		id_user = user,
		command = command
	)

	data = {
		"success": False
	}

	if exist:
		status = 406
		c_command = exist[0].command
		data['msg'] = f"The command \"{c_command}\" is already assigned to another"
		return JsonResponse(data, status = status)

	audio = Commands(
		id_user = user,
		description = description,
		language = language,
		text = text,
		command = command,
	)

	try:
		audio.save()
		data['success'] = True
		data['path'] = audio.audio.url
		status = 200
	except ValidationError as msg:
		data['msg'] = msg.message
		status = 403

	return JsonResponse(data, status = status)