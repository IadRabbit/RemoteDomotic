from pyaudio import paInt16, PyAudio

def genHeader(sampleRate, bitsPerSample, channels):
	datasize = 102400
	o = bytes("RIFF", "ascii")
	o += (datasize + 36).to_bytes(4, "little")
	o += bytes("WAVE", "ascii")
	o += bytes("fmt ", "ascii")
	o += (16).to_bytes(4, "little")
	o += (1).to_bytes(2, "little")
	o += (channels).to_bytes(2, "little")
	o += (sampleRate).to_bytes(4, "little")
	o += (sampleRate * channels * bitsPerSample // 8).to_bytes(4, "little")
	o += (channels * bitsPerSample // 8).to_bytes(2, "little")
	o += (bitsPerSample).to_bytes(2, "little")
	o += bytes("data", "ascii")
	o += (datasize).to_bytes(4, "little")
	return o

class RecordAudio:
	def __init__(self, index):
		self.__format = paInt16
		self.chunk = 1024
		self.__rate = 44100
		self.__bitsPerSample = 16
		self.__channels = 1

		self.wav_header = genHeader(
			self.__rate, self.__bitsPerSample,
			self.__channels, self.chunk
		)

		self.__p = PyAudio()

		try:
			self.stream = self.__p.open(
				format = self.__format,
				channels = self.__channels,
				input_device_index = index,
				rate = self.__rate,
				input = True,
				frames_per_buffer = self.chunk
			)
		except OSError:
			pass