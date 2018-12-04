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
		self.only_chroma = only_chroma
		self.only_melody = only_melody

	def compare(self, feat_song, feat_query, subseq):
		# Let's look for alignment:

		#For melodies, subseq= True
		#For chromas, subseq = False
		D, wp = librosa.sequence.dtw(feat_song[1000:2000], feat_query[1000:2000], subseq=subseq)
		#print('feat song shape:', feat_song.shape)
		#print('query song shape:', feat_query.shape)
		#print('wp shape:', wp.shape)
		if subseq == True: #melodies
			feat_song = np.expand_dims(feat_song, axis=1)
			feat_query = np.expand_dims(feat_query, axis=1)
			dist = self.get_dist(feat_song[wp[0,:]], feat_query[wp[1,:]])
		if subseq == False: #chromas
			dist = self.get_dist(feat_song[:,wp[:,0]], feat_query[:,wp[:,1]])
		return dist

	def get_dist(self, x, y):
		# Efficient distance computation no loops ;)
		#return np.sqrt(np.dot(x, x) - 2 * np.dot(x, y) + np.dot(y, y))
		dist = -2 * np.dot(x, y.T) + np.sum(x**2, axis=1) + np.sum(y**2, axis=1)
		dist = np.sum(dist)
		return dist




# main pseudocode
#load file 1
data_1 = np.load('Tests/creedence_clearwater_revival+Live_in_Europe+10-Proud_Mary.npy').item()
melody_1 = data_1['melody']
chroma_1 = data_1['chroma']

#load file 1
data_2 = np.load('Tests/creedence_clearwater_revival+Live_in_Europe+10-Proud_Mary.npy').item()
melody_2 = data_2['melody']
chroma_2 = data_2['chroma']

#'Tests/lloyd_cole_and_the_commotions+Rattlesnakes+03-Rattlesnakes.npy'
detector =Detector()

#Comparing chromas
dist_chroma = detector.compare(chroma_1, chroma_2, subseq = False)
print('distancia chroma:', dist_chroma)
#Comparing melodies
dist_melody = detector.compare(melody_1, melody_2, subseq = True)
print('distancia melody:', dist_melody)


