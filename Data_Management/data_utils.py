import pickle
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from sklearn import preprocessing
import string


def split_dataset(data,labels, train_per=0.7, val_per=0.2):
	#Splits dataset in 2 or 3 partitions (if train%+val%<1 the rest goes to test)
	if train_per+val_per<1:
		x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=1-train_per)
		x_test, x_val, y_test, y_val = train_test_split(x_test, y_test, test_size=(val_per/(1-train_per)))
		return x_train, y_train, x_val, y_val, x_test, y_test
	else:
		x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=1-train_per)
		return x_train, y_train,x_test, y_test


def save_partition(data,labels,name):
	'''Saves matrixes intro numpy file'''
	data=[[x_sample, x_label] for x_sample, x_label in zip(data, name)]
	np.save(name, data, allow_pickle=True, fix_imports=True)