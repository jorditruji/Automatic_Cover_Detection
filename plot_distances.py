import matplotlib.pyplot as plt
import numpy as np
from glob import glob

def load_dist (path):
	# Loads dist results from file
	mel_dist = []
	chroma_dist = []
	distances_files=glob(path)
	for file in distances_files:
		dist = np.load(file)
		mel_dist.append(dist[0])
		chroma_dist.append(dist[1])
	return mel_dist, chroma_dist



intra_dist_mel,intra_dist_chroma = load_dist('intra_dist/*.npy')
inter_dist_mel, inter_dist_chroma = load_dist('inter_dist/*.npy')

print intra_dist_chroma


plt.hist(intra_dist_mel, bins=24, alpha=0.5, label='intra-class', color = 'blue')
plt.hist(inter_dist_mel+0*np.ones(len(inter_dist_mel)),  bins=24, alpha=0.5,color = 'red' ,label='inter-class')
plt.legend(loc='upper right')
plt.show()

