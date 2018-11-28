from Audio_Processing.cqt_chroma_extractor import CQT_Chroma_Extractor
from Audio_Processing.melody_extractor import Melody_Extractor
import librosa
import librosa.display
import numpy as np
import scipy.io.wavfile as wavfile
import matplotlib.pyplot as plt
from scipy import signal
from Audio_Processing.audio_utils import *
import time
import matplotlib.pyplot as plt

# Load test songs:

wav_files=['Tests/Amy_Winehouse_-_You_re_Wondering_Now-9b3lo5a3iEk.wav','Tests/The_Specials_-_You_re_Wondering_Now-xEPfSWk0Lsw.wav']
#Version 1 and 2 load
fm1, wav_data1  = wavfile.read(wav_files[0])
fm2, wav_data2 = wavfile.read(wav_files[1])

wav_data1 = abs_normalize_wave_minmax(wav_data1)
wav_data2 = abs_normalize_wave_minmax(wav_data2)

if fm1==fm2:
	fm=fm1

#Create chroma and melody extractors:
#chroma_extractor= CQT_Chroma_Extractor(fm)
melody_extractor= Melody_Extractor(fm)

# Feature extraction
melody_1,times1=melody_extractor.extract(wav_data1)
#chroma_1=chroma_extractor.extract(wav_data1)

melody_2, times2 =melody_extractor.extract(wav_data2)
#chroma_2=chroma_extractor.extract(wav_data2)

#Plot Melodies
plt.figure()
plt.subplot(2, 1, 1)
plt.plot(times1, melody_1)
plt.xlabel('Time (s)')
plt.ylabel('Frequency (cents relative to 55 Hz)')

plt.subplot(2, 1, 2)
plt.plot(times2, melody_2)
plt.xlabel('Time (s)')
plt.ylabel('Frequency (cents relative to 55 Hz)')


plt.figure()
D, wp = librosa.sequence.dtw(melody_1,melody_2, subseq=True)
plt.subplot(2, 1, 1)
librosa.display.specshow(D, x_axis='frames', y_axis='frames')
plt.title('Database excerpt')
plt.plot(wp[:, 1], wp[:, 0], label='Optimal path', color='y')
plt.legend()
plt.subplot(2, 1, 2)
print (D[-1, :] / wp.shape[0]).shape
plt.plot(D[-1, :] / wp.shape[0])
#plt.xlim([0, Y.shape[1]])
plt.ylim([0, 2])
plt.title('Matching cost function')
plt.tight_layout()
plt.show()
