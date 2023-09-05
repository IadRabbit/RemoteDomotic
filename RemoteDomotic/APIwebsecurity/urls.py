from . import views
from django.urls import path

urlpatterns = [
	path(
		"auth/", views.auth,
		name = "auth"
	),

	path(
		"logout/", views.logout_view,
		name = "logout"
	),

	path(
		"upload_audio_command/", views.upload_audio,
		name = "upload_audio"
	),

	path(
		"playaudio/", views.playaudio,
		name = "playaudio"
	),

	path(
		"del_audio/", views.del_audio,
		name = "del_audio"
	),

	path(
		"get_audios/", views.get_audios,
		name = "get_audios"
	),

	path(
		"play_command/", views.play_command,
		name = "play_command"
	),

	path(
		"turn_lamp/", views.turn_lamp,
		name = "turn_lamp"
	),

	path(
		"color_lamp/", views.color_lamp,
		name = "color_lamp"
	),

	path(
		"save_gtts/", views.save_gtts,
		name = "save_gtts"
	)
]