from websecurity.models import Commands
from PyP100.PyP100 import P100 as tapo_lamp

def tapo(ip, manufacturer):
	email = manufacturer.email
	password = manufacturer.password
	device = tapo_lamp(ip, email, password)
	return device

def status_tapo(device):
	manufacturer = device.id_manufacturer
	device = tapo(device.ip, manufacturer)
	status, hue, brightness = device.getStatus()

	if status:
		device.turnOff()
	else:
		device.turnOn()

	return status, hue, brightness

def change_hue_tapo(device, hue, brightness):
	manufacturer = device.id_manufacturer
	device = tapo(device.ip, manufacturer)

	if 2500 <= hue <= 6500:
		device.setLight(
			color_temp = hue,
			brightness = brightness
		)
	else:
		device.setColor(
			hue = hue,
			brightness = brightness
		)

def get_audio_user(user):
	audios_user = Commands.objects.filter(id_user = user.id)
	return audios_user

def select_way(device, mode, hue = None, brightness = None):
	status = None
	which = device.id_manufacturer.manufacturer

	if which == "tapo":
		if mode == "status":
			status, hue, brightness = status_tapo(device)
		elif mode == "change_hue":
			change_hue_tapo(device, hue, brightness)

	return status, hue, brightness