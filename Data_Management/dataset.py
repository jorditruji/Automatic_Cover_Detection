from __future__ import division
import numpy as np
from glob import glob
from itertools import tee, izip

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

class Dataset(object):
	"""
	Loads dataset
	Param:
		path
	"""

	def __init__(self, path='/work/jmorera/coversongs/covers32k/'):
		self.path=path
		self.data, self.n_songs, self.n_samples =self.read_song_names()

	def read_song_names(self):
		# Loads paths for every song
		song_names=glob(self.path+"*/")
		n_songs=len(song_names)
		n_versions=len(glob(self.path+"*/*.npy"))
		print n_versions
		data_dict={}
		print " {} different songs, {} total songs".format(n_songs,n_versions)
		for song in song_names:
			song_name=song.split('/')[-2]
			data_dict[song_name]=glob(self.path+""+song_name+"/*.npy")
		return data_dict,n_songs,n_versions


	def shuffle_data(self):
		true_samples = []
		false_samples = []
		for son in pairwise(self.data.keys()):
			true_samples.append(self.data[son[0]][0:2])
			false_samples.append([self.data[son[1]][0], self.data[son[0]][0]])

		return true_samples, false_samples



