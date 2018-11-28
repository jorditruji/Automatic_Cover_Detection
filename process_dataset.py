from Audio_Processing.cqt_chroma_extractor import CQT_Chroma_Extractor
from Audio_Processing.melody_extractor import Melody_Extractor
import librosa
import librosa.display
import numpy as np
import scipy.io.wavfile as wavfile
import matplotlib.pyplot as plt
from scipy import signal
from Audio_Processing.audio_utils import *
import time
import matplotlib.pyplot as plt
from Data_Management.dataset import *
import subprocess
import os.path

def mp3_to_wav(file):
	output= file.replace('mp3', 'wav')
	cmd= "ffmpeg -i {} {} ".format(file, output)
	if os.path.isfile(output):
		return
	subprocess.call(cmd, shell=True)

# Create dataset instance and feature extractor
dataset = Dataset()

for song in dataset.data.keys():

	# Load song
	paths = dataset.data[song]

	for path in paths:
		feature_object={}
		mp3_to_wav(path)
		path_bo=path.replace('mp3','wav')
		fs, audio =  wavfile.read(str(path_bo))
		audio = abs_normalize_wave_minmax(audio)
		# Update extractor fs
		mel_extractor = Melody_Extractor(fs)
		chroma_extract = CQT_Chroma_Extractor(fs)

		# Extract Features
		melody , times = mel_extractor.extract(audio)
		chroma = chroma_extract.extract(audio)

		# Save features
		feature_object['melody'] = melody
		feature_object['chroma'] = chroma
		name=path.replace('.mp3','')
		np.save(name, feature_object, allow_pickle=True, fix_imports=True)


