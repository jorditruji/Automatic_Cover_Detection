#from Audio_Processing.cqt_chroma_extractor import CQT_Chroma_Extractor
#from Audio_Processing.melody_extractor import Melody_Extractor
#import librosa
#import librosa.display
import numpy as np
import scipy.io.wavfile as wavfile
import matplotlib.pyplot as plt
from scipy import signal
from Audio_Processing.audio_utils import *
import time
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import euclidean_distances, paired_euclidean_distances
from sklearn import preprocessing
from scipy.spatial import distance
# Centering:
def center_mel2(melody):
	samples = melody.shape[1]
	middle = samples/2
	return melody[:,middle-6000:middle+6000]

# Centering:
def center_mel(melody):
	samples = melody.shape[1]
	middle = samples/2
	return melody[melody[:]!=0]
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

		#For melodies, subseq= False
		#For chromas, subseq = True

		if subseq:
			D, wp = librosa.sequence.dtw(feat_song, feat_query, subseq=subseq)
			print('feat song shape:', np.max(feat_song,axis=1).shape)
			print('query song shape:', np.max(feat_query,axis=1).shape)
			print('feat song shape:', np.max(feat_song,axis=1))
			print('query song shape:', np.max(feat_query,axis=1))
			dist=np.sum(paired_euclidean_distances(feat_song[:,wp[:,0]], feat_query[:,wp[:,1]]))
		else:
			feat_song=preprocessing.scale(feat_song)
			feat_query=preprocessing.scale(feat_query)
			D, wp = librosa.sequence.dtw(feat_song, feat_query, subseq=subseq)
			print('feat song shape:', np.max(feat_song,axis=0).shape)
			print('query song shape:', np.max(feat_query,axis=0).shape)
			print('feat song shape:', np.max(feat_song,axis=0))
			print('query song shape:', np.max(feat_query,axis=0))
			dist = self.get_dist(feat_song[:,wp[:,0]], feat_query[:,wp[:,1]])
		return dist

	def get_dist(self, x, y,):
		print x == y
		print x.shape
		# Efficient distance computation no loops ;)
		#return np.sqrt(np.dot(x, x) - 2 * np.dot(x, y) + np.dot(y, y))
		'''
		dist = -2 * np.sum(np.dot(x, y.T),axis=1) + np.sum(x**2, axis=1) + np.sum(y**2, axis=1)
		print np.dot(x, y.T).shape

		dist = np.sum(dist)
		'''

		dist = distance.euclidean(np.squeeze(x),np.squeeze(y))
		print dist
		return np.sum(dist)




# main pseudocode
#load file 1

data_1 = np.load('../coversongs/covers32k/Rattlesnakes/tori_amos+Strange_Little_Girls+06-Rattlesnakes.npy').item()
melody_1 = center_mel(np.expand_dims(data_1['melody'],axis=0))
chroma_1 = data_1['chroma']


data_2 = np.load('../coversongs/covers32k/Rattlesnakes/lloyd_cole_and_the_commotions+Rattlesnakes+03-Rattlesnakes.npy').item()
melody_2 = center_mel(np.expand_dims(data_2['melody'],axis=0))
chroma_2 = data_2['chroma']




#'Tests/lloyd_cole_and_the_commotions+Rattlesnakes+03-Rattlesnakes.npy'
detector =Detector()
#Comparing chromas
#dist_chroma = detector.compare(chroma_1, chroma_2, subseq = False)
#print('distancia chroma:', dist_chroma)
#Comparing melodies

dist_melody = detector.compare(np.expand_dims(melody_1,axis=0),np.expand_dims(melody_1,axis=0), subseq = False)
print('distancia melody:', dist_melody)


dist_melody = detector.compare(chroma_1, chroma_2, subseq = True)
print('distancia chroma:', dist_melody)


'''

0,1,0,0
1,0,0,0
0,1,1,1


1,0
0,0
1,1

'''