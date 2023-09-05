from django.http import JsonResponse

def is_post(function):
	def _function(request):
		if request.method != "POST":
			data = {
				"error": "NOT POST REQUEST"
			}

			return JsonResponse(data, status = 405)

		return function(request)

	return _function

def is_login(function):
	def _function(request):
		if not request.user.is_authenticated:
			data = {
				"error": "NOT LOGGED"
			}

			return JsonResponse(data, status = 401)

		return function(request)

	return _function

def is_file(function):
	params = ["description", "command"]

	def _function(request):
		if not "audio" in request.FILES:
			data = {
				"error": "NOT AUDIO",
				"msg": "No audio has been received"
			}

			return JsonResponse(data, status = 405)

		for param in params:
			if not param in request.POST:
				data = {
					"error": f"NOT {param.upper()}",
					"msg": f"No {param} has been received"
				}

				return JsonResponse(data, status = 405)

		return function(request)

	return _function

def is_audio(function):
	params = ["id_audio"]

	def _function(request):
		for param in params:
			if not param in request.POST:
				data = {
					"error": f"NOT {param.upper()}",
					"msg": f"No {param} has been received"
				}

				return JsonResponse(data, status = 405)

		return function(request)

	return _function

def is_command(function):
	params = ["command"]

	def _function(request):
		for param in params:
			if not param in request.POST:
				data = {
					"error": f"NOT {param.upper()}",
					"msg": f"No param {param} has been received"
				}

				return JsonResponse(data, status = 405)

		return function(request)

	return _function

def is_lamp(function):
	params = ["id_device"]

	def _function(request):
		for param in params:
			if not param in request.POST:
				data = {
					"error": f"NOT {param.upper()}",
					"msg": f"No param {param} has been received"
				}

				return JsonResponse(data, status = 405)

		return function(request)

	return _function

def is_hue(function):
	params = ["id_device", "hue", "brightness"]

	def _function(request):
		posts = request.POST

		for param in params:
			if not param in posts:
				data = {
					"error": f"NOT {param.upper()}",
					"msg": f"No param {param} has been received"
				}

				return JsonResponse(data, status = 405)

			if not posts[param].isdigit():
				data = {
					"error": f"INVALID {param.upper()}",
					"msg": f"The param {param} is invalid"
				}

				return JsonResponse(data, status = 405)

		return function(request)

	return _function

def is_gtts(function):
	params = [
		"audio_description", "audio_lang",
		"audio_text", "audio_command"
	]

	def _function(request):
		posts = request.POST

		for param in params:
			if not param in posts:
				data = {
					"error": f"NOT {param.upper()}",
					"msg": f"No param {param} has been received"
				}

				return JsonResponse(data, status = 405)

		return function(request)

	return _function