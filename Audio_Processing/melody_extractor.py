from __future__ import division
import vamp
import librosa
import numpy as np
import scipy.io.wavfile as wavfile
import matplotlib.pyplot as plt




class Melody_extractor(object):
    """
    Returns the melody of an audio file
    Param:
        fs= sampling freq
        minfqr
        maxfqr
        voicing
        minspeaksaliency

    """

    def __init__(self, fs, minfqr=100.0, maxfqr=1200.0, voicing=0.2, minpeaksalience=0.0):

        self.fs = fs
        self.minfqr=minfqr
        self.maxfqr=maxfqr
        self.voicing=voicing
        self.minpeaksalience=minpeaksalience
        self.params= {"minfqr": minfqr, "maxfqr":maxfqr, "voicing": 0.2, "minpeaksalience": 0.0}


    def extract(self, signal):
        """
        Extract Melody of the sound x in numpy array format.
        """
        if signal.ndim > 1:
            print "INFO: Input signal has more than 1 channel; the channels will be averaged."
            signal = mean(signal, axis=1)

        #Vamp UPF melody extractor plugin
		data = vamp.collect(audio, sr, "mtg-melodia:melodia", parameters=self.params)
		hop, melody = data['vector']
		# Melodia returns unvoiced (=no melody) sections as negative values.we will put them to 0:
		melody_pos = melody[:]
		melody_pos[melody<=0] = 0
		# Finally, you might want to plot the pitch sequence in cents rather than in Hz. 
		# This especially makes sense if you are comparing two or more pitch sequences 
		# to each other (e.g. comparing an estimate against a reference).
		melody_cents = 1200*np.log2(melody/55.0)
		melody_cents[melody<=0] = 0
        return melody_cents

