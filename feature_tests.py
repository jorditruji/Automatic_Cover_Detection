from Audio_Processing.spectrum_extractor import *
from Audio_Processing.chroma_extractor import *
import librosa
import librosa.display
import numpy as np
import scipy.io.wavfile as wavfile
import matplotlib.pyplot as plt
from scipy import signal
from Audio_Processing.audio_utils import *
from sklearn.manifold import TSNE


def test_spectogram(wav_file='Tests/Amy_Winehouse_-_You_re_Wondering_Now-9b3lo5a3iEk.wav'):
	# Tests and displays class spectogram

	#Load test wav
	fm, wav_data = wavfile.read(wav_file)
	samples=int(0.025*fm)
	#wav_data=wav_data[0:20*fm]

	plt.figure()

	# Create feature ectractor
	extractor=Spectrum_Extractor(fm)
	features=extractor.extract(wav_data)
	#features = np.array(features).transpose()

	plt.imshow(10*np.transpose(np.log(features)), extent=[0,4.2,0,fm/2], cmap='jet',
	           vmin=np.min(10*np.transpose(np.log(features))), vmax=np.max(10*np.transpose(np.log(features))), origin='lowest', aspect='auto')
	plt.colorbar()


def test_chroma(wav_file='Tests/Amy_Winehouse_-_You_re_Wondering_Now-9b3lo5a3iEk.wav'):
	# Tests and displays class spectogram

	#Load test wav
	fm, wav_data = wavfile.read(wav_file)
	#plt.figure()
	samples=int(0.025*fm)
	#Pxx, freqs, bins, im =plt.specgram(wav_data, NFFT=1024, Fs=fm, noverlap=int(0.01*fm))
	#STEREOOOOO
	wav_data = np.mean(wav_data, axis=1)
	# Create feature ectractor
	print wav_data.shape

	extractor=Chroma_Extractor(fm)
	features=extractor.extract(wav_data)
	features= features.squeeze()
	print features.shape
	max_chord=np.max(features, axis=0)
	plt.figure()
	#features = np.array(features).transpose()
	librosa.display.specshow(features, y_axis='chroma', x_axis='time')
	plt.colorbar() 
	plt.title('Chromagram')
	new_chromas=[]
	for chroma in features:
		max_c=np.max(chroma)
		# cuidadoo, si fas new=chroma segueixen sent el mateix objecte(punters...) 
		new=np.copy(chroma)
		new[new<max_c]=0
		new_chromas.append(new)
	new_chromas=np.array(new_chromas)
	plt.figure()
	#features = np.array(features).transpose()
	librosa.display.specshow(new_chromas, y_axis='chroma', x_axis='time')
	plt.colorbar() 
	plt.title('Chromagram main chords')

	#plt.tight_layout()


def test_beat_chroma(wav_file='Tests/Amy_Winehouse_-_You_re_Wondering_Now-9b3lo5a3iEk.wav'):
	# NO FUNCIONAAAAA
	#Load test wav
	fm, wav_data = wavfile.read(wav_file)
	#plt.figure()
	samples=int(0.025*fm)
	#Pxx, freqs, bins, im =plt.specgram(wav_data, NFFT=1024, Fs=fm, noverlap=int(0.01*fm))
	#STEREOOOOO
	wav_data = np.mean(wav_data, axis=1)
	# Create feature ectractor
	print wav_data.shape
	beat=int(static_tempo(wav_data,fm))
	extractor=Chroma_Extractor(fm,beat_based=True,beat=beat)
	features=extractor.extract(wav_data)
	features= features.squeeze()



	print features.shape
	plt.figure()
	#features = np.array(features).transpose()
	librosa.display.specshow(features, y_axis='chroma', x_axis='time')
	plt.colorbar() 
	plt.title('Beat based Chromagram')


def test_beats(wav_file='Tests/Amy_Winehouse_-_You_re_Wondering_Now-9b3lo5a3iEk.wav'):
	fm, wav_data = wavfile.read(wav_file)
	#plt.figure()
	samples=int(0.025*fm)
	#Pxx, freqs, bins, im =plt.specgram(wav_data, NFFT=1024, Fs=fm, noverlap=int(0.01*fm))
	wav_data = np.mean(wav_data, axis=1)
	tempo=static_tempo(wav_data,fm)
	tempo_vec=dynamic_tempo(wav_data,fm)
	print "static: {}\n".format(tempo)
	print "dynamic: {}\n".format(tempo_vec)
	plt.plot(tempo_vec)
	plt.plot(tempo*np.ones(len(tempo_vec)))
	plt.title("Beat evolution over time vs static beat")


def test_projection_TSNE(wav_file='Tests/Amy_Winehouse_-_You_re_Wondering_Now-9b3lo5a3iEk.wav'):
	# Mirat https://medium.com/@luckylwk/visualising-high-dimensional-datasets-using-pca-and-t-sne-in-python-8ef87e7915b
	#Load test wav
	fm, wav_data = wavfile.read(wav_file)
	#plt.figure()
	samples=int(0.025*fm)
	#Pxx, freqs, bins, im =plt.specgram(wav_data, NFFT=1024, Fs=fm, noverlap=int(0.01*fm))
	#STEREOOOOO
	wav_data = np.mean(wav_data, axis=1)
	# Create feature ectractor


	extractor=Chroma_Extractor(fm)
	features=extractor.extract(wav_data)
	features= features.squeeze()
	print features.shape
	tsne = TSNE(n_components=2, verbose=1, perplexity=40, n_iter=300)
	tsne_results = tsne.fit_transform(np.transpose(features))
	print tsne_results


#test_spectogram()
#test_beats()
#test_beat_chroma()
test_projection_TSNE()

