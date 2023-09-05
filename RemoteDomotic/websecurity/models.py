from time import sleep
from django.db import models
from gtts.lang import tts_langs
from .text_to_audio import transform
from django.dispatch.dispatcher import receiver
from django.core.exceptions import ValidationError
from RemoteDomotic.settings import iots, categories
from .validators import validate_file, get_file_path
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.db.models.signals import pre_save, post_delete

protocols_avalaibles = ["rtsp", "http", "https"]

protocols = [
	(protocol, protocol)
	for protocol in protocols_avalaibles
]

class Manufacturers(models.Model):
	class Meta:
		db_table = "manufacturers"
		verbose_name = "Manufacturer"
		verbose_name_plural = "Manufacturers"

	protocol = models.CharField(
		max_length = 8,
		choices = protocols,
		null = True,
		blank = True,
		unique = True
	)

	email = models.EmailField(
		max_length = 50,
		null = True,
		blank = True
	)

	password = models.CharField(
		max_length = 88,
		null = True,
		blank = True
	)

	video_path = models.CharField(
		max_length = 15,
		null = True,
		blank = True
	)

	audio_path = models.CharField(
		max_length = 15,
		null = True,
		blank = True
	)

	manufacturer =  models.CharField(
		max_length = 15,
		choices = iots,
		default = iots[0][0],
		unique = True
	)

	def __str__(self):
		return self.manufacturer

class Rooms(models.Model):
	class Meta:
		db_table = "rooms"
		verbose_name = "Room"
		verbose_name_plural = "Rooms"

	room = models.CharField(max_length = 15, unique = True)

	def __str__(self):
		return self.room

class Categories(models.Model):
	class Meta:
		db_table = "categories"
		verbose_name = "Category"
		verbose_name_plural = "Categories"

	category = models.CharField(
		max_length = 15,
		choices = categories,
		default = categories[0][0],
		unique = True
	)

	def __str__(self):
		return self.category

class Devices(models.Model):
	class Meta:
		db_table = "devices"
		verbose_name = "Device"
		verbose_name_plural = "Devices"

	id_category = ForeignKey(
		Categories,
		on_delete = models.CASCADE,
		verbose_name = "category",
		db_column = "id_category"
	)

	id_room = ForeignKey(
		Rooms,
		on_delete = models.CASCADE,
		verbose_name = "room",
		db_column = "id_room"
	)

	id_manufacturer = ForeignKey(
		Manufacturers,
		on_delete = models.CASCADE,
		verbose_name = "manufacturer",
		db_column = "id_manufacturer"
	)

	user = models.CharField(
		max_length = 50,
		null = True,
		blank = True
	)

	password = models.CharField(
		max_length = 88,
		null = True,
		blank = True
	)

	port = models.PositiveSmallIntegerField(blank = True, null = True)

	ip = models.GenericIPAddressField(
		unique = True,
		protocol = "IPv4"
	)

	device = models.CharField(max_length = 25, unique = True)

	def __str__(self):
		return self.device

class Permissions(models.Model):
	class Meta:
		db_table = "permissions"
		verbose_name = "Permission"
		verbose_name_plural = "Permissions"

	description = models.TextField(max_length = 200)
	permission = models.CharField(max_length = 15, unique = True)

	def __str__(self):
		return self.permission

class UsersManager(BaseUserManager):
	def create_user(self, name, surname, username, password):
		if not username:
			raise ValueError("The Username must be set")

		user = self.model(
			name = name,
			surname = surname,
			username = username
		)

		user.set_password(password)
		user.save(using = self._db)
		return user

	def create_superuser(self, name, surname, username, password):
		user = self.create_user(
			name = name,
			surname = surname,
			username = username,
			password = password
		)

		permission = Permissions.objects.get(permission = "root")
		user.permissions.add(permission)
		user.save(using = self._db)
		return user

class Users(AbstractBaseUser):
	class Meta:
		db_table = "users"
		verbose_name = "User"
		verbose_name_plural = "Users"

	name = models.CharField(max_length = 50)
	surname = models.CharField(max_length = 50)
	username = models.CharField(max_length = 50, unique = True)
	password = models.CharField(max_length = 88)
	tries = models.PositiveSmallIntegerField(default = 8)

	permissions = models.ManyToManyField(
		Permissions,
		verbose_name = "permission",
		through = "UP"
	)

	belongs = models.ManyToManyField(
		Devices,
		verbose_name = "device",
		through = "B"
	)

	USERNAME_FIELD = "username"
	REQUIRED_FIELDS = ["name", "surname"]

	def has_perm(self, perm, obj = None):
		return True

	def has_module_perms(self, app_label):
		return True

	@property
	def is_staff(self):
		permission = self.permissions.filter(
			permission = "root"
		)

		exist = permission.exists()
		return exist

	objects = UsersManager()

	def __str__(self):
		return "{} {}".format(self.name, self.surname)

class UP(models.Model):
	class Meta:
		db_table = "users_permissions"
		verbose_name = "User Permission"
		verbose_name_plural = "Users Permissions"
		unique_together = ("id_user", "id_permission")

	id_user = models.ForeignKey(
		Users,
		on_delete = models.CASCADE,
		verbose_name = "user",
		db_column = "id_user"
	)

	id_permission = models.ForeignKey(
		Permissions,
		on_delete = models.SET_DEFAULT,
		default = 1,
		verbose_name = "permission",
		db_column = "id_permission"
	)

	def __str__(self):
		permission = self.id_permission
		return permission.permission

class B(models.Model):
	class Meta:
		db_table = "belongs"
		verbose_name = "Belong"
		verbose_name_plural = "Belongs"
		unique_together = ("id_user", "id_device")

	id_user = models.ForeignKey(
		Users,
		on_delete = models.CASCADE,
		verbose_name = "user",
		db_column = "id_user"
	)

	id_device = models.ForeignKey(
		Devices,
		on_delete = models.CASCADE,
		verbose_name = "device",
		db_column = "id_device"
	)

	def __str__(self):
		device = self.id_device
		return device.device

class Commands(models.Model):
	class Meta:
		db_table = "commands"
		verbose_name = "Command"
		verbose_name_plural = "Commands"
		unique_together = ("id_user", "command")

	id_user = models.ForeignKey(
		Users,
		on_delete = models.CASCADE,
		db_column = "id_user",
		verbose_name = "user"
	)

	description = models.TextField(max_length = 200)

	language = models.CharField(
		max_length = 15,
		choices = tts_langs().items(),
		default = "it"
	)

	text = models.TextField(
		max_length = 50,
		null = True,
		blank = True
	)

	command = models.CharField(
		max_length = 20,
		null = True,
		blank = True
	)

	audio = models.FileField(
		upload_to = get_file_path,
		validators = [validate_file],
		blank = True
	)

	def __str__(self):
		return self.audio.name

	def clean(self):
		super().clean()

		if (not self.audio) and (not self.text):
			raise ValidationError("The field text and audio are both empty")

@receiver(post_delete, sender = Commands)
def audio_delete(sender, instance, **kwargs):
	instance.audio.delete(False)

@receiver(pre_save, sender = Commands)
def audio_remove_before(sender, instance, **kwargs):
	sleep(1)
	text = instance.text
	lang = instance.language
	id_audio = instance.id
	audio = instance.audio

	if text:
		audio.delete()
		audio = transform(text, lang)
		instance.audio = audio

	if id_audio:
		old_audio = (
			Commands
			.objects
			.get(id = id_audio)
		)

		old_audio_name = old_audio.audio

		if old_audio_name != audio:
			old_audio.delete()
	else:
		validate_file(instance.audio)