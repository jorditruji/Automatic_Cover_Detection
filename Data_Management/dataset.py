from __future__ import division
import numpy as np
from glob import glob



class Dataset(object):
	"""
	Loads dataset
	Param:
		path
	"""

	def __init__(self, path='/home/jordi/Desktop/coversongs/covers32k/'):
		self.path=path
		self.data, self.n_songs, self.n_samples =self.read_song_names()

	def read_song_names(self):
		# Loads paths for every song
		song_names=glob(self.path+"*/")
		n_songs=len(song_names)
		n_versions=len(glob(self.path+"*/*.mp3"))
		data_dict={}
		print " {} different songs, {} total songs".format(n_songs,n_versions)
		for song in song_names:
			song_name=song.split('/')[-2]
			data_dict[song_name]=glob(self.path+""+song_name+"/*.mp3")
		return data_dict,n_songs,n_versions






