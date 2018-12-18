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
from Data_Management.dataset import Dataset


# Centering:
def crop(melody):
	print melody.shape
	if melody.shape>40000:
		return melody[0:40000]
	else:
		return melody

# Centering:
def center_mel(melody):
	samples = melody.shape[1]
	middle = samples/2
	print "0's",melody[melody[:]==0].shape
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
		print " input 1 shape: {} \n".format(feat_song.shape)
		print " input 2 shape: {}\n".format(feat_query.shape)
		if subseq:
			D, wp = librosa.sequence.dtw(feat_song, feat_query, subseq=subseq)
			dist=np.sum(paired_euclidean_distances(feat_song[:,wp[:,0]], feat_query[:,wp[:,1]]))
			D = 0
			wp = 0
		else:
			feat_song = np.transpose(feat_song)
			feat_query = np.transpose(feat_query)
			D, wp = librosa.sequence.dtw(feat_song, feat_query, subseq=True)
			dist = self.get_dist(feat_song[:,wp[:,0]], feat_query[:,wp[:,1]])/feat_song[:,wp[:,0]].shape[1]
			print feat_song[:,wp[:,0]].shape
			D = 0
			wp = 0
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
		return np.divide(np.sum(dist),np.squeeze(x).shape)



# Instantiate main support classes
dataset = Dataset()
detector = Detector()

# Sample data, not really shuffled ;)
true_samples, false_samples = dataset.shuffle_data()

count = 0
# Intra class distances:
for song_1,song_2 in true_samples:
	# Load features 1
	data_1 = np.load(song_1).item()
	melody_1 = center_mel(np.expand_dims(data_1['melody'],axis=0))
	# Load features 2
	data_2 = np.load(song_2).item()
	melody_2 = center_mel(np.expand_dims(data_2['melody'],axis=0))

	# Comparing melodies
	# Normalization
	melody_1 = crop(np.divide(melody_1-np.mean(melody_1),np.std(melody_1)))
	melody_2 = crop(np.divide(melody_2-np.mean(melody_2),np.std(melody_2)))

	dist_melody = detector.compare(np.expand_dims(melody_1,axis=1),np.expand_dims(melody_2,axis=1), subseq = False)
	print('distancia melody:', dist_melody)
	# Chromas
	chroma_1 = data_1['chroma']
	chroma_2 = data_2['chroma']
	dist_chroma = detector.compare(chroma_1, chroma_2, subseq = True)
	print('distancia chroma:', dist_chroma)
	np.save('intra_'+str(count), [dist_melody, dist_chroma])
	count+=1
	print count



count = 0
# Inter class distances:
for song_1,song_2 in false_samples:
	# Load features 1
	data_1 = np.load(song_1).item()
	melody_1 = center_mel(np.expand_dims(data_1['melody'],axis=0))
	chroma_1 = data_1['chroma']
	# Load features 2
	data_2 = np.load(song_2).item()
	melody_2 = center_mel(np.expand_dims(data_2['melody'],axis=0))
	chroma_2 = data_2['chroma']

	# Comparing melodies
	# Normalization
	melody_1 = crop(np.divide(melody_1-np.mean(melody_1),np.std(melody_1)))
	melody_2 = crop(np.divide(melody_2-np.mean(melody_2),np.std(melody_2)))

	dist_melody = detector.compare(np.expand_dims(melody_1,axis=1),np.expand_dims(melody_2,axis=1), subseq = False)
	print('distancia melody:', dist_melody)

	dist_chroma = detector.compare(chroma_1, chroma_2, subseq = True)
	print('distancia chroma:', dist_chroma)
	np.save('inter'+str(count), [dist_melody, dist_chroma])
	count+=1

'''

# main pseudocode
#load file 1

data_1 = np.load('../coversongs/covers32k/Rattlesnakes/tori_amos+Strange_Little_Girls+06-Rattlesnakes.npy').item()
melody_1 = center_mel(np.expand_dims(data_1['melody'],axis=0))
chroma_1 = data_1['chroma']


data_2 = np.load('../coversongs/covers32k/Abracadabra/steve_miller_band+Steve_Miller_Band_Live_+09-Abracadabra.npy').item()
melody_2 = center_mel(np.expand_dims(data_2['melody'],axis=0))
chroma_2 = data_2['chroma']




#'Tests/lloyd_cole_and_the_commotions+Rattlesnakes+03-Rattlesnakes.npy'
detector =Detector()
#Comparing chromas
#dist_chroma = detector.compare(chroma_1, chroma_2, subseq = False)
#print('distancia chroma:', dist_chroma)
#Comparing melodies
melody_1 = np.divide(melody_1-np.mean(melody_1),np.std(melody_1))
melody_2 = np.divide(melody_2-np.mean(melody_2),np.std(melody_2))



dist_melody = detector.compare(np.expand_dims(melody_1,axis=1),np.expand_dims(melody_1,axis=1), subseq = False)
print('distancia melody:', dist_melody)


dist_melody = detector.compare(chroma_1, chroma_1, subseq = True)
print('distancia chroma:', dist_melody)

'''
'''

0,1,0,0
1,0,0,0
0,1,1,1


1,0
0,0
1,1

'''