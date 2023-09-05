from vlc import MediaPlayer
from threading import Thread
#from pydub.playback import play as py_play
#from pydub.audio_segment import AudioSegment

def play_sound(audio_path):
	#play(audio_path)
	Thread(
		target = play,
		args = (audio_path, )
	).start()

def play(audio_path):
	#if audio_path.endswith(".wav"):
	#	media = AudioSegment.from_wav(audio_path)
	#elif audio_path.endswith(".mp3"):
	#	media = AudioSegment.from_mp3(audio_path)

	a = MediaPlayer(audio_path)
	a.play()
	#py_play(media)