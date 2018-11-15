# Automatic_Cover_Detection
UPC ETSETB 2018 Digital Speech and Audio Processing project.

Implementation of a cover detector based on chroma features and melodies.

## Dataset
Evaluation of the system is carried on with covers80 dataset and other songs added by the team.
D. P. W. Ellis (2007). The "covers80" cover song data set
    Web resource, available: http://labrosa.ee.columbia.edu/projects/coversongs/covers80/. 


## Feature extraction

### Enhanced chromas:
The structure of the song can be described as a chord progression, the most similar features we can automatically from the song are the chromas.

Implementation based on: https://librosa.github.io/librosa_gallery/auto_examples/plot_chroma.html

![alt text](https://github.com/jorditruji/Automatic_Cover_Detection/blob/master/Images/enhanced_chromas.png)


### Melody:
In order to extract the melodies automatically we will use an implementetion of Melody Extraction from Polyphonic Music Signals using Pitch Contour Characteristics.

Paper: http://mtg.upf.edu/node/2436 
Implementation: https://www.upf.edu/web/mtg/melodia

![alt text](https://github.com/jorditruji/Automatic_Cover_Detection/blob/master/Images/processed_melody.png)

## Comparison

### Alignment

Dynamic time wrapping will be used n order to compare both melody vectors(n_samples) and chroma matrices (12*n_frames).
![alt text](https://github.com/jorditruji/Automatic_Cover_Detection/blob/master/Images/dtw.png)

### Distances


## Decision

TODOOOOOOOOO
