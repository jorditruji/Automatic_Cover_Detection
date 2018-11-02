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