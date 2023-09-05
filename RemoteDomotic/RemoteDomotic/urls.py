from . import views
from django.contrib import admin
from django.urls import path, include

handler404 = "RemoteDomotic.views.error_404"
handler403 = "RemoteDomotic.views.error_403"

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
		"media/audios/<audio>/", views.audio_manage,
		name = "audio_manage"
	),

	path(
		"websecurity/", include("websecurity.urls")
	),

	path(
		"APIwebsecurity/", include("APIwebsecurity.urls")
	),

	path(
		"rootAcsPan/", admin.site.urls
	),
]