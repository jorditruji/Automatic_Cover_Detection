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
		mel_dist.append(dist[0][0])
		chroma_dist.append(dist[1])
	return mel_dist, chroma_dist



intra_dist_mel,intra_dist_chroma = load_dist('no_oder_intra/*.npy')
inter_dist_mel, inter_dist_chroma = load_dist('no_oder_inter/*.npy')

max_ = np.max(np.concatenate((np.array(inter_dist_mel),np.array(intra_dist_mel)), axis = 0))
min_ = np.min(np.concatenate((np.array(inter_dist_mel),np.array(intra_dist_mel)), axis = 0))
margin = max_ - min_
n_bins=34
bins = np.arange(min_, max_,margin/n_bins )
plt.figure()
plt.hist(inter_dist_mel,  bins=bins, alpha=0.5,color = 'red' ,label='inter-class')
plt.hist(intra_dist_mel, bins=bins, alpha=0.5, label='intra-class', color = 'blue')

plt.legend(loc='upper right')

plt.title("melody dist distribution (n_pairs = 160)")

plt.show()

'''
plt.subplot(2, 1, 1)
plt.hist(intra_dist_mel, bins=24, alpha=0.5, label='intra-class', color = 'blue')
plt.legend(loc='upper right')
plt.title("Intra-class 2nd order distance distribution (n_pairs = 40)")

plt.subplot(2, 1, 2)
plt.hist(inter_dist_mel,  bins=24, alpha=0.5,color = 'red' ,label='inter-class')
plt.legend(loc='upper right')
plt.title("Inter-class 2nd order distance distribution (n_pairs = 40)")

plt.show()

'''