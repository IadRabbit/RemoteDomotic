from django.contrib import messages
from django.utils.translation import ngettext

from .models import (
	Permissions, Categories, Rooms
)

def create_Permissions_actions():
	permissions_fields = [
		(obj.permission, "func_%s" % obj, obj.id)
		for obj in Permissions.objects.all()
	]

	def func_maker(value, categoria):
		def update_func(self, request, queryset):
			permission = Permissions.objects.get(id = value)
			times = 0

			for user in queryset:
				user.permissions.add(permission)
				times += 1

			self.message_user(
				request, ngettext(
					"%d USER GAINED THE PERMISSION %s",
					"%d USERS GAINED THE PERMISSION %s",
					times
				) % (
					times,
					categoria
				),
				messages.SUCCESS
			)

		return update_func

	actions = {}

	for permission, function_name, value in permissions_fields:
		func = func_maker(value, permission)
		name = "update_{}".format(function_name)

		actions[name] = (
			func, name,
			"ADD PERMISSION {} TO SELECTED USERS".format(permission)
		)

	return actions

def delete_Permissions_actions():
	permissions_fields = [
		(obj.permission, "func_%s" % obj, obj.id)
		for obj in Permissions.objects.all()
	]

	def func_maker(value, categoria):
		def update_func(self, request, queryset):
			permission = Permissions.objects.get(id = value)
			times = 0

			for user in queryset:
				user.permissions.remove(permission)
				times += 1

			self.message_user(
				request, ngettext(
					"%d USER LOST THE PERMISSION %s",
					"%d USERS LOST THE PERMISSION %s",
					times
				) % (
					times,
					categoria
				),
				messages.SUCCESS
			)

		return update_func

	actions = {}

	for permission, function_name, value in permissions_fields:
		func = func_maker(value, permission)
		name = "delete_{}".format(function_name)

		actions[name] = (
			func, name,
			"LOSE PERMISSION {} TO SELECTED USERS".format(permission)
		)

	return actions

def create_Devices_actions_category():
	devices_fields = [
		(obj.category, "func_%s" % obj, obj.id)
		for obj in Categories.objects.all()
	]

	def func_maker(value, category):
		def update_func(self, request, queryset):
			queryset = queryset.update(id_category = value)

			self.message_user(
				request, ngettext(
					"%d DEVICE CATEGORY CHANGED TO  %s",
					"%d DEVICES CATEGORY CHANGED TO  %s",
					queryset
				) % (
					queryset,
					category
				),
				messages.SUCCESS
			)

		return update_func

	actions = {}

	for category, function_name, value in devices_fields:
		func = func_maker(value, category)
		name = "update_{}".format(function_name)

		actions[name] = (
			func, name,
			"CHANGE CATEGORY TO {} TO SELECTED USERS".format(category)
		)

	return actions

def create_Devices_actions_room():
	devices_fields = [
		(obj.room, "func_%s" % obj, obj.id)
		for obj in Rooms.objects.all()
	]

	def func_maker(value, category):
		def update_func(self, request, queryset):
			queryset = queryset.update(id_room = value)

			self.message_user(
				request, ngettext(
					"%d DEVICE ROOM CHANGED TO  %s",
					"%d DEVICES ROOM CHANGED TO  %s",
					queryset
				) % (
					queryset,
					category
				),
				messages.SUCCESS
			)

		return update_func

	actions = {}

	for room, function_name, value in devices_fields:
		func = func_maker(value, room)
		name = "update_{}".format(function_name)

		actions[name] = (
			func, name,
			"CHANGE ROOM TO {} TO SELECTED USERS".format(room)
		)

	return actions