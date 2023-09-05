#!/usr/bin/python3

class TapoError(Exception):
	def __init__(self, msg):
		super().__init__(msg)