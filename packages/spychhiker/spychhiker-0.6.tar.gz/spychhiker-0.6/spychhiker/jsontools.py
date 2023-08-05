#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 18:38:50 2019

@author: benjamin
"""

import json
import os
from os import path
import numpy as np
import scipy.signal as ssg
from ._set import miscstruct
from .oscillator import Glottis
from .vtnetwork import VtNetwork
from .vtwaveguide import VtWaveguide, MainOralTract, GlottalChink
from .areafunction import AreaFunction
from .utils import Cosine_interp, lininterp1

def importjson(jsonFile, seq=None):
    
    if seq is None:
        if path.isfile(jsonFile):
            with open(jsonFile, 'r') as myfile:
                jstr = myfile.read().replace('\n', '')
            idjson = json.loads(jstr)
            af = [x['area'] * 1e-4 for x in idjson['tubes']]
            lf = [x['x'] * 1e-2 for x in idjson['tubes']]
            vArea = [x['velumArea'] * 1e-4 for x in idjson['tubes']]
            vpo = (idjson['VelumOpeningInCm'] * 1e-2)**2
        else:
            print('Warning: file does not exist')
            return
    else:
        nFrame = len(seq)
        for kF in range(nFrame):
            fTmp = jsonFile + '_' + '%.4d' %(seq[kF]) + '.json'
            if path.isfile(fTmp):
                with open(fTmp, 'r') as myfile:
                    jstr = myfile.read().replace('\n', '')
                idjson = json.loads(jstr)
                afTmp = [x['area'] * 1e-4 for x in idjson['tubes']]
                lfTmp = [x['x'] * 1e-2 for x in idjson['tubes']]
                vAreaTmp = [x['velumArea'] * 1e-4 for x in idjson['tubes']]
                vpoTmp = (idjson['VelumOpeningInCm'] * 1e-2)**2
                if kF == 0:
                    nTubes = len(afTmp)
                    af = np.zeros((nTubes, nFrame))
                    lf = np.zeros((nTubes, nFrame))
                    vpo = np.zeros(nFrame)
                    vAreaTmp = np.zeros((nTubes, nFrame))
                af[:,kF] = afTmp
                lf[:,kF] = lfTmp
                vpo[kF] = vpoTmp
                vArea[:,kF] = vAreaTmp
                
    areaObj = AreaFunction('area', np.array(af),
                           'length', np.array(lf))

    if (np.sum(vpo) == 0) and (np.sum(vArea) == 0):
        obj_out = VtWaveguide('area_function', areaObj)
    else:
       obj_out = MainOralTract('area_function', areaObj,
            'velopharyngeal_port', np.array(vpo),
            'velum_area', np.array(vArea))
    areaObj.parent = obj_out
    return np.array(af), np.array(lf), obj_out

def vtjsonread(jsonfile, pathaf, prm=None):
    
    if prm is None:
        prm = miscstruct()

    if not hasattr(prm,'fsim'):
        prm.fsim = 6e4
    if not hasattr(prm, 'amin'):
        prm.amin = 1e-11
    if not hasattr(prm,'agmax'):
        prm.agmax = 4e-5
    if not hasattr(prm,'psubmax'):
        prm.psubmax = 700
    fsim = prm.fsim
    amin = prm.amin    
       
    VT = VtNetwork()
    with open(jsonfile, 'r') as myfile:
        jstr = myfile.read().replace('\n', '')
    idjson = json.loads(jstr)
    gs = idjson['globalScenario']
    nTubes = gs['numberOfTubes']
    
    ##### Area function
    af = gs['keyAreaFunctions']
    afId = [x.get('mainAreaFunctionFile') for x in af]
    naf = len(afId)
    afTp = [x.get('synthesisTime')*1e-3 for x in af]
    afTrans = [x.get('transitionFromPreviousAreaFunction') for x in af]
    tEnd = max(afTp)
    tVec = np.arange(0,tEnd+1/fsim,1/fsim)
    nPt = len(tVec)
    
    af0 = np.zeros((nTubes, naf))
    lf0 = np.zeros((nTubes, naf))
    varea0 = np.zeros((nTubes, naf))
    vpo0 = np.zeros(naf)
    
    afOut = np.zeros((nTubes, nPt))
    lfOut = np.zeros((nTubes, nPt))
    vpoOut = np.zeros(nPt)
    vareaOut = np.zeros((nTubes, nPt))
    
    for kaf in range(naf):   
        tmpFile = afId[kaf]
        idx = tmpFile.find('.')
        tmpList = os.listdir(pathaf)
        
        ff = [ x for x in tmpList if x.find(tmpFile[0:idx]) >= 0]
        ftmp = os.path.join(pathaf, ff[0])        
        with open(ftmp, 'r') as myfile:
            jstr2 = myfile.read().replace('\n', '')
            idtmp = json.loads(jstr2)
        vpo0[kaf] = (idtmp['VelumOpeningInCm']/1e2)**2 
        af0[:,kaf] = [x.get('area')*1e-4 for x in idtmp['tubes']]
        lf0[:,kaf] = [x.get('x')*1e-2 for x in idtmp['tubes']]
        varea0[:,kaf] = [x.get('velumArea')*1e-4 for x in idtmp['tubes']]
        
    
        if (kaf > 0):
            ind = np.argwhere((tVec>= afTp[kaf-1]) * (tVec <= afTp[kaf]))[:,0]
            xi = np.array([afTp[kaf-1], afTp[kaf]])
            xo = tVec[ind]
            yiAf = np.concatenate((af0[:,kaf-1].reshape(-1,1), af0[:,kaf].reshape(-1,1)),axis=1)
            yiLf = np.concatenate((lf0[:,kaf-1].reshape(-1,1), lf0[:,kaf].reshape(-1,1)),axis=1)
            yiVaO = np.concatenate((varea0[:,kaf-1].reshape(-1,1), varea0[:,kaf].reshape(-1,1)),axis=1)
            yiVpO = np.array([vpo0[kaf-1], vpo0[kaf]]).reshape(-1,1).T
    
            if afTrans[kaf] == 'COS':        
                afOut[:,ind] = Cosine_interp( xi, yiAf, xo )
                lfOut[:,ind] = Cosine_interp( xi, yiLf, xo )
                vareaOut[:,ind] = Cosine_interp( xi, yiVaO, xo )
                vpoOut[ind] = Cosine_interp( xi, yiVpO, xo )
            elif afTrans[kaf] == 'LIN':
                afOut[:,ind] = lininterp1( xi, yiAf, xo, 1 )
                lfOut[:,ind] = lininterp1( xi, yiLf, xo, 1)
                vareaOut[:,ind] = lininterp1( xi, yiVaO, xo, 1)
                vpoOut[ind] = lininterp1( xi, yiVpO, xo )
      
    
    afOut = afOut-vareaOut
    ##### Check null values
    afOut[afOut < amin] = amin
    lfOut[lfOut < amin] = amin
    vareaOut[vareaOut < amin] = amin
    vpoOut[vpoOut < amin] = amin
    
    
    MOT = MainOralTract()
    MOT.area_function = AreaFunction('area', afOut,
                                     'length', lfOut, 
                                     'parent', MOT)
    if VT.waveguide is None:
        VT.waveguide = []
    VT.waveguide.append(MOT)
    ###### Check for nasal coupling and build nasal tract if necessary
    if np.sum(vpo0) > 0:
        kn = np.zeros(nPt)
        for k in range(nPt):
            tmp = list(vareaOut[:,k]) 
            idx = [x for x in range(len(tmp)) if tmp[x] > 0][0] #list(vareaOut[:,k]).index(not 0)
            if idx != []:
                kn[k] = idx
    
        kn = np.ceil(np.median(kn))
    
    #### F0
    F0 = gs['F0Commands']
    
    F0Hz = [x.get('FOInHz') for x in F0]
    F0tp = [x.get('timeInMs')*1e-3 for x in F0]
    idx0 = [x for x in range(len(F0Hz)) if F0Hz[x]>0]
    F0Hz = [F0Hz[x] for x in idx0]
    F0tp = [F0tp[x] for x in idx0]
    
    F0Out = lininterp1(F0tp,F0Hz,tVec)
    
    ##### Ag
    ag = gs['keyAG0']
    ag0 = [x.get('Ag0Opening') for x in ag]
    agPhon = [x.get('phoneticLabel') for x in ag]
    agTp = [x.get('synthesisTime')*1e-3 for x in ag]
    agTrans = [x.get('transitionFromPreviousAreaFunction') for x in ag]
    nag = len(ag0)
    
    agOut = np.zeros(nPt)    
    for kag in range(nag):
        if (kag > 0):
            ind = np.argwhere((tVec>= agTp[kag-1]) * (tVec <= agTp[kag]))[:,0]       
            if agTrans[kag] == 'COS':
                agOut[ind] = Cosine_interp( np.array([ agTp[kag-1], agTp[kag] ]), np.array([ag0[kag-1], ag0[kag] ]).reshape(-1,1).T, tVec[ind] )
            elif agTrans[kag] == 'LIN':
                agOut[ind] = lininterp1( np.array([ agTp[kag-1], agTp[kag] ]), np.array([ ag0[kag-1], af0[kag] ]).reshape(-1,1).T, tVec[ind] )
    
    Gl = Glottis()
    Gl.fundamental_frequency = F0Out
    lch = np.sqrt(agOut)
    lch[lch <= amin] = amin # if length = 0 => set to the minimal value
    lch[lch >= 1] = 1-amin #  if length = 1 => set to the maximal value (1-vmin)
    Gl.partial_abduction = lch
    
    ##### Check existence of glottal opening and build glottal chink if necessary
    if np.sum(agOut) > 0:
        agOut = agOut*prm.agmax
        agOut[agOut<amin] = amin
        Chink = GlottalChink()
        Chink.parent_wvg = [MOT]
        achTmp = agOut.reshape(1,-1)
        lchTmp = Gl.x_position[-1] * np.ones_like(achTmp)
        Chink.area_function = AreaFunction('area', achTmp,
                                           'length', lchTmp, 
                                           'parent', Chink)
        
        VT.waveguide.append(Chink)
    
    if VT.oscillators is None:
        VT.oscillators = []
    VT.oscillators.append(Gl)
    
    #### Segmentation
    seg = gs['segmentation']
    segStart = np.array([x.get('beginsAtInMs')*1e-3 for x in seg])
    segEnd = np.array([x.get('endsAtInMs')*1e-3 for x in seg])
    segPhon = [x.get('sampaCode') for x in seg]
    
    #### Build subglottal pressure
    psubOut = np.ones(nPt) * prm.psubmax     
    phonDur = (segEnd - segStart)
    nup = int(0.025 * prm.fsim)
    ndown = int(0.1 * prm.fsim)
    
    for k in range(len(segPhon)):
        ind = [x for x in range(len(tVec)) if tVec[x] >= segStart[k] and tVec[x] <= segEnd[k]]
        if segPhon[k] == '#':
            psubOut[ind] = 0
            if k < len(segPhon) - 1:
                if segPhon[k+1] != '#':
                    ind2ch = np.arange(ind[-1] - nup, ind[-1] + nup)
                    w = ssg.hann(2 * len(ind2ch))
                    w = w[:len(ind2ch)]
                    psubOut[ind2ch] = w * prm.psubmax
        else:
            if k < len(segPhon) - 1:
                if segPhon[k+1] == '#':
                    ind2ch = np.arange(ind[-1] - ndown, ind[-1] + ndown)
                    ind2ch = [x for x in ind2ch if x < len(psubOut)]
                    w = ssg.hann(2 * len(ind2ch))
                    w = w[:len(ind2ch)][::-1]
                    psubOut[ind2ch] = w * prm.psubmax
 
    VT.subglottal_control = psubOut
    VT.phonetic_label = segPhon
    VT.phonetic_instant = np.concatenate((segStart.reshape(-1,1), segEnd.reshape(-1,1)),axis=1)
    VT.simulation_frequency = fsim

    return VT