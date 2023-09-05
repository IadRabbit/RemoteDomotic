from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

def is_authenticated(function):
	def _function(request):
		user = request.user

		if user.is_authenticated:
			return redirect("/websecurity/index")

		return function(request)

	return _function

def is_post(function):
	def _function(request):
		if request.method != "POST":
			raise PermissionDenied()

		return function(request)

	return _function