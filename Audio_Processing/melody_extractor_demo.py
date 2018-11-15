import vamp
import librosa
import numpy as np
import scipy.io.wavfile as wavfile
import matplotlib.pyplot as plt
# This is the audio file we'll be analyzing.
# You can download it here: http://labrosa.ee.columbia.edu/projects/melody/mirex05TrainFiles.zip
audio_file = '../Tests/Amy_Winehouse_-_You_re_Wondering_Now-9b3lo5a3iEk.wav'
# This is how we load audio using Essentia
fm1, wav_data1 = wavfile.read(audio_file)

# This is how we load audio using Librosa
audio, sr = librosa.load(audio_file, mono=True)
data = vamp.collect(audio, sr, "mtg-melodia:melodia")
# vector is a tuple of two values: the hop size used for analysis and the array of pitch values
# Note that the hop size is *always* equal to 128/44100.0 = 2.9 ms
hop, melody = data['vector']
print(hop)
print(melody)

timestamps = 8 * 128/44100.0 + np.arange(len(melody)) * (128/44100.0)
# parameter values are specified by providing a dicionary to the optional "parameters" parameter:
params = {"minfqr": 100.0, "maxfqr": 4000.0, "voicing": 0.2, "minpeaksalience": 0.0}

data = vamp.collect(audio, sr, "mtg-melodia:melodia", parameters=params)
hop, melody = data['vector']
# Melodia returns unvoiced (=no melody) sections as negative values. So by default, we get:
plt.figure(figsize=(18,6))
plt.plot(timestamps, melody)
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')




# A clearer option is to get rid of the negative values before plotting
melody_pos = melody[:]
melody_pos[melody<=0] = 0
plt.figure(figsize=(18,6))
plt.plot(timestamps, melody_pos)
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')

# Finally, you might want to plot the pitch sequence in cents rather than in Hz. 
# This especially makes sense if you are comparing two or more pitch sequences 
# to each other (e.g. comparing an estimate against a reference).
melody_cents = 1200*np.log2(melody/55.0)
melody_cents[melody<=0] = 0
plt.figure(figsize=(18,6))
plt.plot(timestamps, melody_cents)
plt.xlabel('Time (s)')
plt.ylabel('Frequency (cents relative to 55 Hz)')
plt.show()

plt.show()
