from __future__ import division
import vamp
import librosa
import numpy as np
import scipy.io.wavfile as wavfile
import matplotlib.pyplot as plt
import time



class Melody_Extractor(object):
    """
    Returns the melody of an audio file
    Param:
        fs= sampling freq
        minfqr
        maxfqr
        voicing
        minspeaksaliency

    """

    def __init__(self, fs, minfqr=100.0, maxfqr=1200.0, voicing=0.2, minpeaksalience=0.0, separate=True):

        self.fs = fs
        self.minfqr=minfqr
        self.maxfqr=maxfqr
        self.voicing=voicing
        self.minpeaksalience=minpeaksalience
        self.params= {"minfqr": minfqr, "maxfqr":maxfqr, "voicing": 0.2, "minpeaksalience": 0.0}
        self.separate=separate

    def extract(self, signal):
        """
        Extract Melody of the sound x in numpy array format.
        """
        start_time=time.time()
        if signal.ndim > 1:
            print "INFO: Input signal has more than 1 channel; the channels will be averaged."
            signal = np.mean(signal, axis=1)


        # Remove percussion if separate:
        if self.separate:
            audio, percussion = librosa.effects.hpss(signal)

        #Vamp UPF melody extractor plugin
        data = vamp.collect(audio, self.fs, "mtg-melodia:melodia", parameters=self.params)
        hop, melody = data['vector']

        timestamps = 8 * 128/self.fs + np.arange(len(melody)) * (128/self.fs)
        # Melodia returns unvoiced (=no melody) sections as negative values.we will put them to 0:
        melody_pos = melody[:]
        melody_pos[melody<=0] = 0
        # Finally, you might want to plot the pitch sequence in cents rather than in Hz. 
        # This especially makes sense if you are comparing two or more pitch sequences 
        # to each other (e.g. comparing an estimate against a reference).
        melody_cents = 1200*np.log2(melody/55.0)
        melody_cents[melody<=0] = 0
        print("--- %s seconds --- for melody extraction" % (time.time() - start_time))

        return melody_cents,timestamps

