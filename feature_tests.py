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
	plt.title("Spectogram")



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


def compare_wondering(wav_files=['Tests/Amy_Winehouse_-_You_re_Wondering_Now-9b3lo5a3iEk.wav','Tests/The_Specials_-_You_re_Wondering_Now-xEPfSWk0Lsw.wav']):
	#Version 1 and 2 load
	fm1, wav_data1 = wavfile.read(wav_files[0])
	fm2, wav_data2 = wavfile.read(wav_files[1])
	
	if wav_data1.ndim > 1:
		print "INFO: Input signal has more than 1 channel; the channels will be averaged."
		wav_data1 = mean(wav_data1, axis=1)
	if wav_data2.ndim > 1:
		print "INFO: Input signal has more than 1 channel; the channels will be averaged."
		wav_data2 = mean(wav_data2, axis=1)

	wav_data1=abs_normalize_wave_minmax(wav_data1)
	wav_data2=abs_normalize_wave_minmax(wav_data2)
	plt.figure()
	# Spectograms
	# Create feature ectractor
	extractor1=Spectrum_Extractor(fm1)
	features1=extractor1.extract(wav_data1)
	plt.subplot(2, 1, 1)
	plt.imshow(10*np.transpose(np.log(features1)), extent=[0,4.2,0,fm1/2], cmap='jet',
	           vmin=np.min(10*np.transpose(np.log(features1))), vmax=np.max(10*np.transpose(np.log(features1))), origin='lowest', aspect='auto')
	plt.colorbar()
	plt.ylabel('Amy Winehouse')
	extractor2=Spectrum_Extractor(fm2)
	features2=extractor2.extract(wav_data2)

	plt.subplot(2, 1, 2)
	plt.imshow(10*np.transpose(np.log(features2)), extent=[0,4.2,0,fm2/2], cmap='jet',
	           vmin=np.min(10*np.transpose(np.log(features2))), vmax=np.max(10*np.transpose(np.log(features2))), origin='lowest', aspect='auto')
	plt.colorbar()
	plt.ylabel('The Specials')


	# Chromas
	extractor1=Chroma_Extractor(fm1)
	features1=extractor1.extract(wav_data1)
	features1= features1.squeeze()
	max_chord1=np.max(features1, axis=0)
	plt.figure()
	plt.subplot(2, 1, 1)
	plt.title("Chromas")

	#features = np.array(features).transpose()
	librosa.display.specshow(features1, y_axis='chroma', x_axis='time')
	extractor2=Chroma_Extractor(fm2)
	features2=extractor2.extract(wav_data2)
	features2= features2.squeeze()
	max_chord2=np.max(features2, axis=0)
	plt.subplot(2, 1, 2)
	#features = np.array(features).transpose()

	librosa.display.specshow(features2, y_axis='chroma', x_axis='time')



	# Dominant chord chromas
	new_chromas1=[]
	for chroma in features1:
		max_c=np.max(chroma)
		# cuidadoo, si fas new=chroma segueixen sent el mateix objecte(punters...) 
		new=np.copy(chroma)
		new[new<max_c]=0
		new_chromas1.append(new)
	new_chroma1=np.array(new_chromas1)

	new_chromas2=[]
	for chroma in features2:
		max_c=np.max(chroma)
		# cuidadoo, si fas new=chroma segueixen sent el mateix objecte(punters...) 
		new=np.copy(chroma)
		new[new<max_c]=0
		new_chromas2.append(new)

	new_chroma2=np.array(new_chromas2)
	plt.figure()
	plt.subplot(2, 1, 1)
	librosa.display.specshow(new_chroma1, y_axis='chroma', x_axis='time')
	plt.colorbar()
	plt.title("Dominant chord chromas")


	plt.subplot(2, 1, 2)
	librosa.display.specshow(new_chroma2, y_axis='chroma', x_axis='time')
	plt.colorbar()

	# Tempos
	tempo1=static_tempo(wav_data1,fm1)
	tempo_vec1=dynamic_tempo(wav_data1,fm1)
	print "static: {}\n".format(tempo1)
	print "dynamic: {}\n".format(tempo_vec1)
	plt.figure()
	plt.subplot(2, 1, 1)
	plt.plot(tempo_vec1)
	plt.plot(tempo1*np.ones(len(tempo_vec1)))
	plt.title("Beat evolution over time vs static beat")
	
	tempo2=static_tempo(wav_data2,fm2)
	tempo_vec2=dynamic_tempo(wav_data2,fm2)
	print "static: {}\n".format(tempo2)
	print "dynamic: {}\n".format(tempo_vec2)
	plt.subplot(2, 1, 2)
	plt.plot(tempo_vec2)

	plt.plot(tempo2*np.ones(len(tempo_vec2)))

	plt.plot(tempo2*np.ones(len(tempo_vec2)))	
#test_spectogram()
#test_beats()
#test_beat_chroma()
#test_projection_TSNE()
compare_wondering()
plt.show()
