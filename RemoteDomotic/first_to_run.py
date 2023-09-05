#!/usr/bin/python3

from websecurity.models import Permissions

perm = Permissions(
	description = "root",
	permission = "root"
)

perm.save()

perm = Permissions(
	description = "guest",
	permission = "guest"
)

perm.save()