from . import views
from django.urls import path

urlpatterns = [
	path(
		"", views.index,
		name = "index"
	),

	path(
		"index/", views.index,
		name = "index"
	),

	path(
		"login/", views.login,
		name = "login"
	),

	path(
		"auth/", views.auth,
		name = "auth"
	),

	path(
		"logout/", views.logout,
		name = "logout"
	),

	path(
		"upload_audio_command/", views.upload_audio,
		name = "upload_audio"
	),

	path(
		"records/", views.records,
		name = "records"
	),

	path(
		"playaudio/", views.playaudio,
		name = "playaudio"
	),

	path(
		"my_audios/", views.my_audios,
		name = "my_audios"
	),

	path(
		"video_feed/<video>/", views.video_feed,
		name = "video_feed"
	),

	path(
		"del_audio/", views.del_audio,
		name = "del_audio"
	),

	path(
		"audio_feed/<audio>/", views.audio_feed,
		name = "audio_feed"
	),

	path(
		"room/<room>/", views.room,
		name = "room"
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