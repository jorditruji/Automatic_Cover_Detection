import librosa
import numpy as np


def static_tempo(signal, fs):
	# Static beat:
	onset_env = librosa.onset.onset_strength(signal, sr=fs)
	tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=fs)
	return tempo


def dynamic_tempo(signal, fs):
	# Static beat:
	onset_env = librosa.onset.onset_strength(signal, sr=fs)
	tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=fs,aggregate=None)
	return tempo


def abs_normalize_wave_minmax(wavdata):
	'''normalize'''
	x = wavdata.astype(np.float)
	imax = np.max(np.abs(x))
	try:
		x_n = x / imax
		return x_n
	except:
		return