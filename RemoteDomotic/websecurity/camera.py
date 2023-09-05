from time import sleep
from RemoteDomotic.settings import BASE_DIR

from cv2.cv2 import (
	VideoCapture, flip, imencode
)

img = f"{BASE_DIR}/RemoteDomotic/static/img/offlinecam.jpg"
not_found = open(img, "rb")
not_found_bytes = not_found.read()
not_found.close()

class VideoCamera:
	def __init__(self, index, is_belong):
		self.__is_belong = is_belong
		self.__index = index
		self.__retry = 5
		self.__is_off = False
		self.__start()

	def __start(self):
		sleep(1)
		self.__video = VideoCapture(self.__index)

	def __del__(self):
		self.__video.release()

	def get_frame(self):
		if not self.__is_belong:
			return not_found_bytes

		if (self.__is_off) and (self.__retry >= 0):
			self.__retry -= 1
			return not_found_bytes
		elif (self.__is_off) and (self.__retry == -1):
			self.__retry = 5
			self.__is_off = False
			self.__start()
			return not_found_bytes

		success, image = self.__video.read()

		if not success:
			self.__del__()
			self.__is_off = True
			return not_found_bytes

		#image = detect_face(image)
		#frame_flip = flip(image, 1)
		ret, jpeg = imencode(".jpg", image)
		return jpeg.tobytes()