<<<<<<< HEAD
from __future__ import division

=======
>>>>>>> 411f71b0e3852d4ca5e979dc3fccf64df52a6212
from numpy import *
import librosa


<<<<<<< HEAD
=======

>>>>>>> 411f71b0e3852d4ca5e979dc3fccf64df52a6212
class Chroma_Extractor(object):
    """
    Returns the spectrum of an audio file
    Param:
        fs= sampling freq
        win_length_ms = lenght of the hamming window
        win_shift = shift of the window
        FFT_size = FFT points 
        n_bands = bands used chroma filterbank
        mel = Convert to mel scale
        normalize = normalize each freq bin aling frames
    """
<<<<<<< HEAD
    def __init__(self, fs, win_length_ms=25, win_shift_ms=10, FFT_SIZE=512, n_bands=12,mel=False, normalize=True, beat_based=False,beat=0):
=======
    def __init__(self, fs, win_length_ms=25, win_shift_ms=10, FFT_SIZE=512, n_bands=12,mel=False, normalize=True):
>>>>>>> 411f71b0e3852d4ca5e979dc3fccf64df52a6212
        self.fs = fs
        self.FFT_SIZE = FFT_SIZE
        self.FRAME_LEN = int(float(win_length_ms) / 1000 * fs)
        self.FRAME_SHIFT = int(float(win_shift_ms) / 1000 * fs)
        self.window = hamming(self.FRAME_LEN)
        self.n_bands = n_bands
        self.normalize = normalize
<<<<<<< HEAD
        self.beat_based=beat_based
        self.beat=beat
=======
>>>>>>> 411f71b0e3852d4ca5e979dc3fccf64df52a6212


    def extract(self, signal):
        """
        Extract Chromas of the sound x in numpy array format.
        """
        if signal.ndim > 1:
            print "INFO: Input signal has more than 1 channel; the channels will be averaged."
            signal = mean(signal, axis=1)
<<<<<<< HEAD
        if self.beat_based:
            beat_samples= int(self.fs/self.beat)*60
            print beat_samples
            s_2=abs(librosa.stft(signal, n_fft=beat_samples, hop_length=1, win_length=beat_samples,window=hamming(beat_samples)))**2
            chroma = librosa.feature.chroma_stft(S=s_2, sr=self.fs)
            print chroma.shape
            feature=chroma
            return feature
        else:
            s_2=abs(librosa.stft(signal, n_fft=4096, hop_length=self.FRAME_SHIFT, win_length=self.FRAME_LEN,window=self.window))**2
            chroma = librosa.feature.chroma_stft(S=s_2, sr=self.fs)
            feature=chroma
            return feature
        '''
=======
>>>>>>> 411f71b0e3852d4ca5e979dc3fccf64df52a6212
        frames = (len(signal) - self.FRAME_LEN) / self.FRAME_SHIFT + 1
        feature = []
        for f in xrange(frames):
            # Windowing
            frame = signal[f * self.FRAME_SHIFT : f * self.FRAME_SHIFT +
                           self.FRAME_LEN] * self.window
            # Pre-emphasis
            frame[1:] -= frame[:-1] * 0.95
            #Librosa chromas
<<<<<<< HEAD
            print frame.shape
            s_2=abs(librosa.stft(frame, n_fft=4096,win_length=4096,window=ones(4096)))**2
            #print S.shape
            print s_2.shape
            chroma = librosa.feature.chroma_stft(S=s_2, sr=self.fs)
            print chroma.shape
            #frame=librosa.feature.chroma_stft(y=frame, sr=self.fs,  n_chroma=self.n_bands)
            feature.append(chroma)
        feature = array(feature)
        '''
=======
            frame=librosa.feature.chroma_stft(y=frame, sr=self.fs, n_fft=self.FFT_size, n_chroma=self.n_bands)
            feature.append(feature)
        feature = row_stack(feature)
>>>>>>> 411f71b0e3852d4ca5e979dc3fccf64df52a6212
        # Mean & variance normalization
        if feature.shape[0] > 1 and self.normalize:
            mu = mean(feature, axis=0)
            #print "mean: ", mu
            sigma = std(feature, axis=0)
            #print "std: ", sigma
            feature = (feature - mu) / sigma
            #print "abs: ", amax(feature,axis=0)-amin(feature,axis=0)
            #print "max: ", amax(feature,axis=0)

        return feature


