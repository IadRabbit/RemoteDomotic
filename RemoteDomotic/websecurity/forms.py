from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import (
	Commands, Devices, Manufacturers,
	Permissions, Rooms, Users, Categories
)

class UserCreationForm(forms.ModelForm):
	name = forms.CharField(
		label = "Name",
		widget = forms.TextInput
	)

	surname = forms.CharField(
		label = "Surname",
		widget = forms.TextInput
	)

	username = forms.CharField(
		label = "Username",
		widget = forms.TextInput
	)

	password1 = forms.CharField(
		label = "Password",
		widget = forms.PasswordInput
	)

	password2 = forms.CharField(
		label = "Password confirmation",
		widget = forms.PasswordInput
	)

	class Meta:
		model = Users
		fields = ()

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")

		if (password1 and password2) and (password1 != password2):
			raise ValidationError("Passwords don't match")

		return password2

	def save(self, commit = True):
		user = super().save(commit = False)
		user.set_password(self.cleaned_data["password1"])

		if commit:
			user.save()

		return user

class UserChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField(
		help_text = (
			"The passwords are protected by hash "
			"you can't see them =) "
			"change password <a href=\"../password/\">HERE</a>."
		)
	)

	name = forms.CharField(
		label = "Name",
		widget = forms.TextInput
	)

	surname = forms.CharField(
		label = "Surname",
		widget = forms.TextInput
	)

	username = forms.CharField(
		label = "Username",
		widget = forms.TextInput
	)

	tries = forms.CharField(
		label = "Tries avalaible",
		widget = forms.NumberInput
	)

	class Meta:
		model = Users
		fields = ()

	def clean_password(self):
		return self.initial['password']

class PermissionForm(forms.ModelForm):
	description = forms.CharField(
		label = "Description",
		widget = forms.Textarea
	)

	permission = forms.CharField(
		label = "Permission",
		widget = forms.TextInput
	)

	class Meta:
		model = Permissions
		fields = ()

class ManufacturerForm(forms.ModelForm):
	email = forms.EmailField(
		label = "Email",
		widget = forms.EmailInput,
		required = False
	)

	password = forms.CharField(
		label = "Password",
		widget = forms.TextInput,
		required = False
	)

	video_path = forms.CharField(
		label = "Video Path",
		widget = forms.TextInput,
		required = False
	)

	audio_path = forms.CharField(
		label = "Audio Path",
		widget = forms.TextInput,
		required = False
	)

	class Meta:
		model = Manufacturers
		fields = ()

class RoomForm(forms.ModelForm):
	room = forms.CharField(
		label = "Room",
		widget = forms.TextInput
	)

	class Meta:
		model = Rooms
		fields = ()

class DeviceForm(forms.ModelForm):
	device = forms.CharField(
		label = "Device",
		widget = forms.TextInput
	)

	user = forms.CharField(
		label = "User",
		widget = forms.TextInput,
		required = False
	)

	password = forms.CharField(
		label = "Password",
		widget = forms.TextInput,
		required = False
	)

	class Meta:
		model = Devices
		fields = ()

class CommandForm(forms.ModelForm):
	description = forms.CharField(
		label = "Description",
		widget = forms.Textarea,
		max_length = 50
	)

	text = forms.CharField(
		label = "Text",
		widget = forms.Textarea,
		required = False,
		max_length = 50
	)

	class Meta:
		model = Commands
		fields = ()