from aubio import source as au_source
from RemoteDomotic.settings import BASE_DIR
from requests.exceptions import ConnectTimeout, ConnectionError

default_chunk = 2048
wav = f"{BASE_DIR}/RemoteDomotic/static/img/empty.wav"
#not_found = au_source(wav, "rb")
#not_found_bytes = not_found.readframes(default_chunk)

class Microphone:
	def __init__(self, index, is_belong):
		self.__is_belong = is_belong
		self.__index = index
		self.__retry = 5
		self.__is_off = False
		self.__start()

	def empty_buffer(self):
		data = not_found_bytes

		while data != b"":
			data = not_found.readframes(default_chunk)
			yield data

	def __start(self):
		try:
			self.__audio_frame = r_get(
				self.__index,
				timeout = 2,
				stream = True
			).iter_content(2048)

			for chunk in self.__audio_frame:
				yield chunk
		except (ConnectTimeout, ConnectionError):
			self.__is_off = True
			yield self.__empty_buffer()

	def get_frame(self):
		if not self.__is_belong:
			yield self.__empty_buffer()
		else:
			if (self.__is_off) and (self.__retry >= 0):
				self.__retry -= 1
				yield self.__empty_buffer()
			elif (self.__is_off) and (self.__retry == -1):
				self.__retry = 5
				self.__is_off = False
				self.__start()
				yield self.__empty_buffer()
			else:
				yield self.__start()