from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .admin_commands import (
	create_Permissions_actions, delete_Permissions_actions,
	create_Devices_actions_category, create_Devices_actions_room
)

from .models import (
	Devices, Manufacturers, Rooms, Users,
	Permissions, Categories, Commands
)

from .forms import (
	DeviceForm, ManufacturerForm, RoomForm,
	UserCreationForm, UserChangeForm,
	PermissionForm, CommandForm
)

class PermissionsInline(admin.TabularInline):
	model = Users.permissions.through
	extra = 0

class DevicesInline(admin.TabularInline):
	model = Users.belongs.through
	extra = 0

@admin.register(Users)
class UserAdmin(BaseUserAdmin):
	form = UserChangeForm
	add_form = UserCreationForm
	list_display = ("name", "surname", "username", "tries")
	list_filter = ()

	fieldsets = (
		(
			"User", {
				"fields": (
					"name", "surname",
					"username", "tries", "password"
				)
			}
		),
	)

	inlines = (PermissionsInline, DevicesInline)

	add_fieldsets = (
		(
			"Add User", {
				"classes": ("wide", ),
				"fields": (
					"name", "surname",
					"username", "password1", "password2"
				)
			}
		),
	)

	search_fields = ("name", "surname", "username", "permissions__permission")
	ordering = ("username", )
	filter_horizontal = ()

	def get_actions(self, request):
		actions = super().get_actions(request)

		actions.update(
			create_Permissions_actions()
		)

		actions.update(
			delete_Permissions_actions()
		)

		return actions

@admin.register(Permissions)
class PermissionAdmin(admin.ModelAdmin):
	form = PermissionForm
	list_display = ("description", "permission")
	list_filter = ()

	fieldsets = (
		(
			"Permission", {
				"fields": (
					"description", "permission"
				)
			}
		),
	)

	inlines = (PermissionsInline, )
	search_fields = ("description", "permission")
	ordering = ()
	filter_horizontal = ()

@admin.register(Manufacturers)
class ManufacturerAdmin(admin.ModelAdmin):
	form = ManufacturerForm
	list_display = ("manufacturer", )
	list_filter = ()

	fieldsets = (
		(
			"Manufacturer", {
				"fields": (
					"protocol", "manufacturer",
					"email", "password",
					"video_path", "audio_path"
				)
			}
		),
	)

	search_fields = ("manufacturer", "email")
	ordering = ()
	filter_horizontal = ()

@admin.register(Rooms)
class RoomAdmin(admin.ModelAdmin):
	form = RoomForm
	list_display = ("room", )
	list_filter = ()

	fieldsets = (
		(
			"Room", {
				"fields": (
					"room",
				)
			}
		),
	)

	search_fields = ("room", )
	ordering = ()
	filter_horizontal = ()

@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ("category", )
	list_filter = ()

	fieldsets = (
		(
			"Category", {
				"fields": (
					"category",
				)
			}
		),
	)

	search_fields = ("category", )
	ordering = ()
	filter_horizontal = ()

@admin.register(Devices)
class DeviceAdmin(admin.ModelAdmin):
	form = DeviceForm
	list_display = ("id_category", "id_room", "device")
	list_filter = ()

	fieldsets = (
		(
			"Device", {
				"fields": (
					"id_category", "id_room",
					"id_manufacturer", "user", "password",
					"port", "ip", "device"
				)
			}
		),
	)

	inlines = (DevicesInline, )

	search_fields = (
		"id_category__category", "id_room__room", 
		"id_manufacturer__manufacturer",
		"user", "ip", "device"
	)

	ordering = ()
	filter_horizontal = ()

	def get_actions(self, request):
		actions = super().get_actions(request)

		actions.update(
			create_Devices_actions_category()
		)

		actions.update(
			create_Devices_actions_room()
		)

		return actions

@admin.register(Commands)
class CommandAdmin(admin.ModelAdmin):
	form = CommandForm
	list_display = ("id_user", "username", "audio")
	list_filter = ()

	def username(self, obj):
		username = obj.id_user.username
		return username

	fieldsets = (
		(
			"Audio", {
				"fields": (
					"id_user", "description", "language",
					"text", "command", "audio"
				)
			}
		),
	)

	search_fields = ("id_user__name", "id_user__surname", "id_user__username")
	ordering = ()
	filter_horizontal = ()

admin.site.unregister(Group)
admin.site.site_header = "RemoteDomotic Admin"
admin.site.site_title = "RemoteDomotic Admin Portal"
admin.site.index_title = "Welcome to RemoteDomotic Amministration"