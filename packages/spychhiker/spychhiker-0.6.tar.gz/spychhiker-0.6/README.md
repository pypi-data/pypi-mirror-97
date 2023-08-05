# SpychHiker library

## Presentation

SpychHiker is an open-source python library that offers various functionalities for speech analysis and processing. Features include
* analysis of vocal tract configurations: transfer function [1], dynamic acoustic-to-articulatory inversion [2]
* analysis and transformation of audio speech signals: voiced/noise source separation [3], formant shifting...
* running speech synthesis based on physical model [4]
* analysis of oral corpus 

Main classes include:
* `VtNetwork`: this superclass models the whole vocal tract system as a waveguide network, including the side branches, the glottis and the potential supraglottal oscillators (e.g. the tongue tip). It is used to perform running speech synthesis.
* `VtWaveguide`: this class is inherated from the superclass `VtNetwork`, and models any acoustic waveguide. This is used to compute transfer functions and to perform acoustic-to-articulatory inversion.
* `Oscillator`: this superclass is used to add self-oscillating objects in `VtNetwork` objects. This is used for running speech synthesis. `Glottis` and `Tongue` are the subclasses inherited from 'Oscillator'.
* `SpeechAudio`: this superclass is used to analyze and perform operations on speech audio signals.
* `SpeechSegment`: this subclass is inherited from `SpeechAudio`. It should contain a segment of speech signal corresponding to a phoneme, a word, a phrase, etc. It is used for phonetic analysis of oral corpus.
* `Speaker`: this class contains acoustic realizations of a speaker. It should be used for phonetic analysis of oral corpus.

## Installation
The easy way to install the library is with pip
```
pip install spychhiker
```

You can also get the source codes by cloning this repo with git
```
git clone https://gitlab.com/benjamin.elie/spychhiker.git

```
or by doawnloading its content, and then install it manually

```
python3 -m pip install path_to_spychhiker -e
```

* WARNING #1: Please, do not modify anything in the spychhiker folder, including demo files, unless you want to modify the repository.
* WARNING #2: You may need to install the package python3-tk if you want matplotlib figures to be displayed when executing scripts from a terminal

## Updates

SpychHiker is in its developement stage, so that you may expect regular available updates. Simply run the following command in the spychhiker folder
```
git pull origin master
```
or via pip
```
pip install spychhiker -U
```

## Demos

The folder `Demos` contains several examples showing how to use the different functionalities. If you want to modify these files, please do these modifications on a copy version located outside the spychhiker folder.

## Contact

For questions and remarks, please contact me at bnjmn.elie (at) gmail.com

## Papers to cite

Since these codes do not come out of the blue, you may consider acknowledging the following studies.
If you publish results based on SpeechHiker and if you:
* used the transfer function method, please cite [1],
* used the dynamic acoustic inversion of the vocal tract, please cite [2],
* used the X-GLOS method for voiced/noise source separation, please cite [3],
* used the ESMF synthesizer for running speech synthesis, please cite[4],
* used the ESMF synthesize with the 'ishi' model of the vocal folds, please cite [5], and [6] for the 'smooth' model,
* mention the frication noise generator, please cite [7],
* used the tongue-tip oscillation model in the ESMF synthesizer, please cite [8],
* used the provided default data and desire to mention or to detail them, please cite [9] for the wall-loss terms, [10] for the nasal tract area function, and [11] for the subglottal tract area function.

Additionnaly, SpychHiker uses other libraries:
* librosa fpr LPC analysis [12]
* praat-parselmouth for pitch analysis/modification and formant estimation [13]

## References:
[1] M. M. Sondhi and J. Schroeter, "A hybrid time-frequency domain articulatory speech synthesizer", IEEE Trans. Acoust. Speech Sig. Process. 35(7), 955-967 (1987)

[2] Elie B., and Laprie Y. "Audiovisual to area and length functions inversion of human vocal tract". EUSIPCO, Lisbon 2014.

[3] Elie B., and Chardon G. "Robust tonal and noise separation in presence of colored noise, and application to voiced fricatives". Intern. Congress on Acoustics (ICA), Buenos Aires 2016. 

[4] Elie B., and Laprie Y. "Extension of the single-matrix formulation of the vocal tract: consideration of bilateral channels and connection of self-oscillating models of the vocal folds with a glottal chink". Speech Comm. 82, pp. 85-96 (2016)

[5] Ishizaka K., and Flanagan J. L. "Synthesis of Voiced Sounds from a Two-Mass Model of the Vocal Cords", Bell Syst. Tech. J., vol. 51(6), pp. 1233-1268, 1972

[6] Bailly L., Pelorson X., Henrich N., and Ruty, N. "Influence of a constriction in the near field of the vocal folds: Physical modeling and experimental validation". The Journal of the Acoustical Society of America, 124(5), pp. 3296-3308 (2008)

[7] Birkholz P. "Enhanced area functions for noise source modeling in the vocal tract", in: 10th International Seminar on Speech Production, Köln, pp. 1-4 (2014)

[8] Elie B., and Laprie Y. "Simulating alveolar trills using a two-mass model of the tongue tip". J. Acoust. Soc. Am. 142(5), pp. 3245-3256 (2017)

[9] Birkholz P., Jackèl D. "Influence of temporal discretization schemes on formant frequencies and bandwidths in the time-domain simulation of the vocal tract system.", in: Proc. of the Interspeech 2004-ICSLP, 
pp. 1125-1128 (2004)

[10] Serrurier A., and Badin P. "A three-dimensional articulatory model of the velum and nasopharyngeal wall based on MRI and CT data". The Journal of the Acoustical Society of America, 123(4), pp. 2335-2355 (2008)

[11] Story B. H. "Phrase-level speech simulation with an airway modulation model of speech production", Computer Speech & Language 27(4), pp. 989-1010 (2013)

[12] McFee, Brian, Colin Raffel, Dawen Liang, Daniel PW Ellis, Matt McVicar, Eric Battenberg, and Oriol Nieto. “librosa: Audio and music signal analysis in python.” In Proceedings of the 14th python in science conference, pp. 18-25. 2015.

[13] Jadoul, Y., Thompson, B., & de Boer, B. (2018). Introducing Parselmouth: A Python interface to Praat. Journal of Phonetics, 71, 1-15.



