from numpy import *
import librosa


from numpy import *
import librosa



class CQT_Chroma_Extractor(object):
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
    def __init__(self, fs, win_length_ms=25, win_shift_ms=10, FFT_SIZE=512, n_bands=12,mel=False, normalize=True):
        self.fs = fs
        self.FFT_SIZE = FFT_SIZE
        self.FRAME_LEN = int(float(win_length_ms) / 1000 * fs)
        self.FRAME_SHIFT = int(float(win_shift_ms) / 1000 * fs)
        self.window = hamming(self.FRAME_LEN)
        self.n_bands = n_bands
        self.normalize = normalize


    def extract(self, signal):
        """
        Extract Chromas of the sound x in numpy array format.
        """
        if signal.ndim > 1:
            print "INFO: Input signal has more than 1 channel; the channels will be averaged."
            signal = mean(signal, axis=1)
        frames = (len(signal) - self.FRAME_LEN) / self.FRAME_SHIFT + 1
        feature = []
        for f in xrange(frames):
            # Windowing
            frame = signal[f * self.FRAME_SHIFT : f * self.FRAME_SHIFT +
                           self.FRAME_LEN] * self.window
            # Pre-emphasis
            frame[1:] -= frame[:-1] * 0.95
            #Librosa CQT 
            #TODO!!!!!!!! http://librosa.github.io/librosa/generated/librosa.feature.chroma_cqt.html#librosa.feature.chroma_cqt

            feature.append(feature)
        feature = row_stack(feature)
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


