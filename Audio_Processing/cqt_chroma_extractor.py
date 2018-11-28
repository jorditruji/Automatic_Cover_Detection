from __future__ import print_function
import numpy as np
import scipy
import librosa
import time

#Based on 
"""
===============
Enhanced chroma
===============

This notebook demonstrates a variety of techniques for enhancing chroma features.

Beyond the default parameter settings of librosa's chroma functions, we apply the following
enhancements:

    1. Over-sampling the frequency axis to reduce sensitivity to tuning deviations
    2. Harmonic-percussive-residual source separation to eliminate transients.
    3. Nearest-neighbor smoothing to eliminate passing tones and sparse noise.  This is inspired by the
       recurrence-based smoothing technique of
       `Cho and Bello, 2011 <http://ismir2011.ismir.net/papers/OS8-4.pdf>`_.
    4. Local median filtering to suppress remaining discontinuities.
"""

# Code source: Brian McFee
# License: ISC
# sphinx_gallery_thumbnail_number = 6



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
    def __init__(self, fs, bins_per_octave=12*3, separate=True):
        self.fs = fs
        self.bins_per_octave = bins_per_octave 
        self.separate=separate



    def extract(self, signal):
        """
        Extract Chromas of the sound x in numpy array format.
        """
        start_time=time.time()
        if signal.ndim > 1:
            signal = np.mean(signal, axis=1)
            print ("INFO: Input signal has more than 1 channel, the channels will be averaged.")


        # Remove percussion if separate:
        if self.separate:
            signal, percussion = librosa.effects.hpss(signal)

        #isolating the harmonic component.we'll use a large margin for separating harmonics from percussives
        y_harm = librosa.effects.harmonic(y=signal, margin=8)
        chroma_os_harm = librosa.feature.chroma_cqt(y=y_harm, sr=self.fs, bins_per_octave=self.bins_per_octave)
         # There's still some noise in there though.
        # We can clean it up using non-local filtering.
        # This effectively removes any sparse additive noise from the features.
        chroma_filter = np.minimum(chroma_os_harm,
                                   librosa.decompose.nn_filter(chroma_os_harm,
                                                               aggregate=np.median,
                                                               metric='cosine'))
        # Local discontinuities and transients can be suppressed by
        # using a horizontal median filter.
        chroma_smooth = scipy.ndimage.median_filter(chroma_filter, size=(1, 9))
        print("--- %s seconds --- for chroma" % (time.time() - start_time))
        return chroma_smooth


