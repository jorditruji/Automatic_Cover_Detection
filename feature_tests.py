from Audio_Processing.spectrum_extractor import *
from Audio_Processing.chroma_extractor import *
import librosa
import librosa.display
import numpy as np
import scipy.io.wavfile as wavfile
import matplotlib.pyplot as plt
from scipy import signal

def test_spectogram(wav_file='Tests/METOAUNAMIGOENUNHOSPITALABANDONADO-vum0AvCJce8_preprocessed_frame_300.wav'):
	# Tests and displays class spectogram

	#Load test wav
	fm, wav_data = wavfile.read(wav_file)
	plt.figure()
	samples=int(0.025*fm)
	Pxx, freqs, bins, im =plt.specgram(wav_data, NFFT=1024, Fs=fm, noverlap=int(0.01*fm))

	plt.figure()

	# Create feature ectractor
	extractor=Spectrum_Extractor(fm)
	features=extractor.extract(wav_data)
	#features = np.array(features).transpose()

	plt.imshow(10*np.transpose(np.log(features)), extent=[0,4.2,0,fm/2], cmap='jet',
	           vmin=np.min(10*np.transpose(np.log(features))), vmax=np.max(10*np.transpose(np.log(features))), origin='lowest', aspect='auto')
	plt.colorbar()
	plt.show()


def test_chroma(wav_file='Tests/METOAUNAMIGOENUNHOSPITALABANDONADO-vum0AvCJce8_preprocessed_frame_300.wav'):
	# Tests and displays class spectogram

	#Load test wav
	fm, wav_data = wavfile.read(wav_file)
	#plt.figure()
	samples=int(0.025*fm)
	#Pxx, freqs, bins, im =plt.specgram(wav_data, NFFT=1024, Fs=fm, noverlap=int(0.01*fm))


	# Create feature ectractor
	extractor=Chroma_Extractor(fm)
	features=extractor.extract(wav_data)
	features= features.squeeze()
	#features = np.array(features).transpose()
	librosa.display.specshow(features, y_axis='chroma', x_axis='time')
	plt.colorbar() 
	plt.title('Chromagram')
	#plt.tight_layout()
	plt.show()


plt.show()
test_chroma()