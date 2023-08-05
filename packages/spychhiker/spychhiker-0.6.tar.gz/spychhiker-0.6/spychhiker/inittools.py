#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 07:54:59 2020

@author: benjamin
"""

from os import path
from .speechaudio import SpeechAudio
import soundfile
import numpy as np

def file2speech(fileName, chn=1, sro=None):
    
    if path.isfile(fileName):
        y, sr = soundfile.read(fileName)
        if len(y.shape) == 2:
            idx = np.argmax(y.shape)
            if idx == 0:
                y = y[:,chn-1]
            else:
                y = y[chn-1,:]
        SpeechObject = SpeechAudio('signal', y.astype(float), 'sampling_frequency', sr)
        if sro is not None:
            if sr != sro:
                SpeechObject.speechresample(sro)
    else:
        raise ValueError("File does not exist")    
    return SpeechObject