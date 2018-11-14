import numpy as np
import matplotlib.pyplot as plt
import librosa.display

y, sry = librosa.load('C:\Users\janna\Downloads\Automatic_Cover_Detection-master\Automatic_Cover_Detection-master\Tests\Amy_Winehouse_-_You_re_Wondering_Now-9b3lo5a3iEk.wav')
Y = librosa.feature.chroma_cens(y=y, sr=sry)
x, srx = librosa.load('C:\Users\janna\Downloads\Automatic_Cover_Detection-master\Automatic_Cover_Detection-master\Tests\The_Specials_-_You_re_Wondering_Now-xEPfSWk0Lsw.wav')
X = librosa.feature.chroma_cens(y=x, sr=srx)
D, wp = librosa.sequence.dtw(X, Y, subseq=True)
plt.subplot(2, 1, 1)
librosa.display.specshow(D, x_axis='frames', y_axis='frames')
plt.title('Database excerpt')
plt.plot(wp[:, 1], wp[:, 0], label='Optimal path', color='y')
plt.legend()
plt.subplot(2, 1, 2)
plt.plot(D[-1, :] / wp.shape[0])
plt.xlim([0, Y.shape[1]])
plt.ylim([0, 2])
plt.title('Matching cost function')
plt.tight_layout()
