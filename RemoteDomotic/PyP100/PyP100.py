from time import time
from uuid import uuid4
from hashlib import sha1
from requests import post
from base64 import b64decode
from Crypto.PublicKey import RSA
from .exceptions import TapoError
from Crypto.Cipher import PKCS1_v1_5
from .tp_link_cipher import TpLinkCipher

#Old Functions to get device list from tplinkcloud
def getToken(email, password):
	URL = "https://eu-wap.tplinkcloud.com"

	payload = {
		"method": "login",
		"params": {
			"appType": "Tapo_Ios",
			"cloudUserName": email,
			"cloudPassword": password,
			"terminalUUID": str(uuid4())#"0A950402-7224-46EB-A450-7362CDB902A2"
		}
	}

	json = post(URL, json = payload).json()
	token = json['result']['token']
	return token

def getDeviceList(email, password):
	token = getToken(email, password)
	URL = f"https://eu-wap.tplinkcloud.com?token={token}"

	payload = {
		"method": "getDeviceList",
	}

	json = post(URL, json = payload).json()
	return json

ERROR_CODES = {
	0: "Success",
	-1010: "Invalid Public Key Length",
	-1012: "Invalid terminalUUID",
	-1501: "Invalid Request or Credentials",
	-1008: "Incorrect Request",
	-1003: "JSON formatting error"
}

class P100():
	def __init__ (self, ipAddress, email, password):
		self.ipAddress = ipAddress
		self.terminalUUID = str(uuid4())
		self.email = email
		self.password = password
		self.errorCodes = ERROR_CODES
		self.encryptCredentials(email, password)
		self.createKeyPair()
		self.__handshake()
		self.__login()
		self.url_app = f"http://{self.ipAddress}/app?token={self.token}"

	def encryptCredentials(self, email, password):
		#Password Encoding
		self.encodedPassword = TpLinkCipher.mime_encoder(
			password.encode("utf-8")
		)

		#Email Encoding
		self.encodedEmail = self.sha_digest_username(email)
		self.encodedEmail = TpLinkCipher.mime_encoder(self.encodedEmail.encode("utf-8"))

	def createKeyPair(self):
		self.keys = RSA.generate(1024)

		self.privateKey = self.keys.exportKey("PEM")
		self.publicKey  = self.keys.publickey().export_key("PEM")

	def decode_handshake_key(self, key):
		decode: bytes = b64decode(key.encode("UTF-8"))
		decode2: bytes = self.privateKey

		cipher = PKCS1_v1_5.new(RSA.import_key(decode2))
		do_final = cipher.decrypt(decode, None)
		if do_final is None:
			raise ValueError("Decryption failed!")

		b_arr:bytearray = bytearray()
		b_arr2:bytearray = bytearray()

		for i in range(0, 16):
			b_arr.insert(i, do_final[i])
		for i in range(0, 16):
			b_arr2.insert(i, do_final[i + 16])

		return TpLinkCipher(b_arr, b_arr2)

	def sha_digest_username(self, data):
		b_arr = data.encode("UTF-8")
		digest = sha1(b_arr).digest()

		sb = ""
		for i in range(0, len(digest)):
			b = digest[i]
			hex_string = hex(b & 255).replace("0x", "")
			if len(hex_string) == 1:
				sb += "0"
				sb += hex_string
			else:
				sb += hex_string

		return sb

	def __handshake(self, timeout = 4):
		URL = f"http://{self.ipAddress}/app"

		payload = {
			"method":"handshake",
			"params":{
				"key": self.publicKey.decode(),
				"requestTimeMils": int(round(time() * 1000))
			}
		}

		r = post(URL, json = payload, timeout = timeout)

		encryptedKey = r.json()["result"]["key"]
		self.tpLinkCipher = self.decode_handshake_key(encryptedKey)

		try:
			self.cookie = r.headers["Set-Cookie"][:-13]
		except:
			errorCode = r.json()["error_code"]
			errorMessage = self.errorCodes[errorCode]
			raise TapoError(f"Error Code: {errorCode}, {errorMessage}")

	def __login(self):
		URL = f"http://{self.ipAddress}/app"

		payload = {
			"method":"login_device",
			"params":{
				"username": self.encodedEmail,
				"password": self.encodedPassword
			},
			"requestTimeMils": int(round(time() * 1000)),
		}

		self.headers = {
			"Cookie": self.cookie
		}

		EncryptedPayload = self.tpLinkCipher.encrypt(payload)

		SecurePassthroughPayload = {
			"method":"securePassthrough",
			"params":{
				"request": EncryptedPayload
			}
		}

		r = post(
			URL, json = SecurePassthroughPayload,
			headers = self.headers
		)

		decryptedResponse = self.tpLinkCipher.decrypt(
			r.json()["result"]["response"]
		)

		try:
			self.token = decryptedResponse["result"]["token"]
		except:
			errorCode = decryptedResponse["error_code"]
			errorMessage = self.errorCodes[errorCode]
			raise TapoError(f"Error Code: {errorCode}, {errorMessage}")

	def __exec_query(self, params, is_set = True):
		time_now = round(time() * 1000)

		if is_set:
			payload = {
				"method": "set_device_info",
				"params": params,
				"requestTimeMils": int(time_now),
				"terminalUUID": self.terminalUUID
			}
		else:
			payload = {
				"method": "get_device_info",
				"requestTimeMils": int(time_now),
			}
	
		encryptedPayload = self.tpLinkCipher.encrypt(payload)

		securePassthroughPayload = {
			"method": "securePassthrough",
			"params": {
				"request": encryptedPayload
			}
		}

		r = post(
			self.url_app,
			json = securePassthroughPayload,
			headers = self.headers
		)

		resp = r.json()["result"]["response"]
		decryptedResponse = self.tpLinkCipher.decrypt(resp)
		#print(decryptedResponse)

		if decryptedResponse["error_code"] != 0:
			errorCode = decryptedResponse["error_code"]
			errorMessage = self.errorCodes[errorCode]
			raise TapoError(f"Error Code: {errorCode}, {errorMessage}")

		return decryptedResponse

	def turnOn(self):
		params = {
			"device_on": True
		}

		self.__exec_query(params)

	def setBrightness(self, brightness):
		params = {
			"brightness": brightness
		}
			
		self.__exec_query(params)

	def turnOff(self):
		params = {
			"device_on": False
		}

		self.__exec_query(params)

	def getDeviceInfo(self):
		json = self.__exec_query(None, False)
		return json
	
	def getStatus(self):
		result = self.getDeviceInfo()['result']
		device_on = result['device_on']

		if not "hue" in result:
			result['hue'] = result['color_temp']

		hue = result['hue']
		brightness = result['brightness']
		return device_on, hue, brightness

	def setColor(self, brightness = 50, hue = 240, saturation = 100):
		params = {
			"hue": hue,
			"saturation": saturation,
			"brightness": brightness
		}

		self.__exec_query(params)

	def setLight(self, brightness = 50, color_temp = 2500):
		params = {
			"brightness": brightness,
			"color_temp": color_temp
		}

		self.__exec_query(params)