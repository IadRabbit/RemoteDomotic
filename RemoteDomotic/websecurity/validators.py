from uuid import uuid4
from magic import from_buffer
from RemoteDomotic.settings import MAX_FILE_SIZE
from django.core.exceptions import ValidationError

mime_types = ["audio/mpeg", "audio/x-wav"]

def get_mime_type(value):
	mime_type = from_buffer(
		value.file.read(2048),
		mime = True
	)

	return mime_type

def validate_file(value):
	value = value.file
	filesize = value.size
	mime_type = get_mime_type(value)

	if filesize > MAX_FILE_SIZE:
		raise ValidationError("The maximum file size that can be uploaded is 2MB")
	elif not mime_type in mime_types:
		raise ValidationError("The file is not a wav or mp3 audio")
	else:
		return value

def get_file_path(instance, filename):
	ext = filename.split(".")[-1]
	filename = f"{uuid4()}.{ext}"
	path = f"audios/{filename}"
	return path