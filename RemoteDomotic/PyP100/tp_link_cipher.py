import json
from pkcs7 import PKCS7Encoder
from base64 import b64encode, b64decode

from json import (
	dumps as js_dumps,
	loads as js_loads
)

from Crypto.Cipher.AES import (
	new as AESnew,
	MODE_CBC
)

class TpLinkCipher:
	def __init__(self, b_arr, b_arr2):
		self.iv = b_arr2
		self.key = b_arr

	def mime_encoder(to_encode):
		encoded_list = list(
			b64encode(to_encode).decode()
		)

		count = 0
	
		for i in range(76, len(encoded_list), 76):
			encoded_list.insert(i + count, '\r\n')
			count += 1
	
		return "".join(encoded_list)

	def encrypt(self, data):
		data = js_dumps(data)
		data = PKCS7Encoder().encode(data)
		cipher = AESnew(self.key, MODE_CBC, self.iv)

		encrypted = cipher.encrypt(
			data.encode()
		)

		data = TpLinkCipher.mime_encoder(encrypted).replace("\r\n","")
		return data

	def decrypt(self, data):
		aes = AESnew(self.key, MODE_CBC, self.iv)

		pad_text = aes.decrypt(
			b64decode(
				data.encode()
			)
		).decode()

		decrypted = PKCS7Encoder().decode(pad_text)
		json = js_loads(decrypted)
		return json