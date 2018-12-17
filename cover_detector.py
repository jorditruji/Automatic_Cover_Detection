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
from sklearn.metrics.pairwise import euclidean_distances


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
		D, wp = librosa.sequence.dtw(feat_song[1000:12000], feat_query[1000:12000], subseq=subseq)
		#print('feat song shape:', feat_song.shape)
		#print('query song shape:', feat_query.shape)
		#print('wp shape:', wp.shape)
		if subseq == True: #melodies
			#feat_song = np.expand_dims(feat_song, axis=1)
			#feat_query = np.expand_dims(feat_query, axis=1)
			dist = self.get_dist(feat_song[wp[0,:]], feat_query[wp[1,:]])
		if subseq == False: #chromas
			dist = self.get_dist(feat_song[:,wp[:,0]], feat_query[:,wp[:,1]])
		return dist

	def get_dist(self, x, y):
		print x[0].shape
		# Efficient distance computation no loops ;)
		#return np.sqrt(np.dot(x, x) - 2 * np.dot(x, y) + np.dot(y, y))
		'''
		dist = -2 * np.sum(np.dot(x, y.T),axis=1) + np.sum(x**2, axis=1) + np.sum(y**2, axis=1)
		print np.dot(x, y.T).shape

		dist = np.sum(dist)
		'''
		dist = euclidean_distances(x,y)
		return dist




# main pseudocode
#load file 1
data_1 = np.load('/home/jordi/Desktop/coversongs/covers32k/Rattlesnakes/tori_amos+Strange_Little_Girls+06-Rattlesnakes.npy').item()
melody_1 = data_1['melody']
chroma_1 = data_1['chroma']


data_2 = np.load('Tests/lloyd_cole_and_the_commotions+Rattlesnakes+03-Rattlesnakes.npy').item()
melody_2 = data_2['melody']
chroma_2 = data_2['chroma']

#'Tests/lloyd_cole_and_the_commotions+Rattlesnakes+03-Rattlesnakes.npy'
detector =Detector()
plt.plot(melody_2)
plt.show()
#Comparing chromas
dist_chroma = detector.compare(chroma_1, chroma_2, subseq = False)
print('distancia chroma:', dist_chroma)
#Comparing melodies
dist_melody = detector.compare(melody_1, melody_2, subseq = True)
print('distancia melody:', dist_melody)


