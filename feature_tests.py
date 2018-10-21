from Audio_Processing.spectrum_extractor import *
import numpy as np
import scipy.io.wavfile as wavfile
import matplotlib.pyplot as plt


def test_spectogram(wav_file='Tests/METOAUNAMIGOENUNHOSPITALABANDONADO-vum0AvCJce8_preprocessed_frame_300.wav'):
	# Tests and displays class spectogram

	#Load test wav
	fm, wav_data = wavfile.read(wav_file)

	t=[x+=x for x in cos()]
	# Create feature ectractor
	extractor=Spectrum_Extractor(fm)
	features=extractor.extract(wav_data)
	#features = np.array(features).transpose()
	plt.imshow(np.transpose(20*np.log(features)), extent=[0,4.2,0,fm/2], cmap='jet',
	           vmin=-120, vmax=0, origin='lowest', aspect='auto')
	plt.colorbar()
	plt.show()


test_spectogram()