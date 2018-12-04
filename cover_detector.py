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



class Detector(object):
	"""
	Loads dataset
	Param:
		path
	"""

	def __init__(self, only_chroma = False, only_melody = False):


	def compare(self, feat_song, feat_query):
		# Let's look for alignment:
		D, wp = librosa.sequence.dtw(feat_song, feat_query, subseq=True)
		dist = get_dist(feat_song[wp[0,:]], feat_query[wp[1,:]])
		return dist

	def get_dist(x,y):
		# Efficient distance computation no loops ;) 
		return np.sqrt(np.dot(x, x) - 2 * np.dot(x, y) + np.dot(y, y))



# main pseudocode

1- feat1= np.load(fitxer1).item()
2- feat2 = np.load(fitxer2.npy).item()

melody_1=feat1['melody']
^ igual 



detector =Detector()

detector.compare(melody1, melody2)
print ^ 