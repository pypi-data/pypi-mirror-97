# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 15:31:35 2020

@author: benjamin
Some functions used to read segmentation files
"""

from os import path
import numpy as np
import xml.etree.ElementTree as ET
import json

def removequotes(label):
    
    new_label = []
    for k1 in range(len(label)):
        lbltmp = label[k1]        
        new_label_tmp = []
        for k2 in range(len(lbltmp)):
            lbltmp2 = lbltmp[k2]
            if lbltmp2 == '"':
                lbltmp2 = '"#"'
            lbltmp2 = lbltmp2.replace('"', '')
            new_label_tmp.append(lbltmp2)
        new_label.append(new_label_tmp)
    return new_label

def func_readTextgrid(fileName):
    
    labels = []
    start = []
    stop = []
    
    POINT_BUFFER = 0.025

    if not path.exists(fileName):
        print('Error: %s not found\n', fileName)
        return labels, start, stop
    
    f = open(fileName, "r")
    C = np.loadtxt(f,
               delimiter='\n', dtype='str')
    f.close()
    
    tiers = -1
    proceed_int = False
    proceed_pnt = False
    xmin = 0
    xmax = 1

    for k in range(len(C)):
    
        A = C[k]
        if 'intervals: size ' in A.lower():
            tiers += 1        
            tier_len = int(A[A.index('=')+1:])
            labels.append([])
            start.append(np.zeros(tier_len))
            stop.append(np.zeros(tier_len))
            cnt = 0
            proceed_int = True
            
        if 'xmin' in A.lower():
            if proceed_int:
                start[tiers][cnt] = float(A[A.index('=')+1:])
            else:
                xmin = float(A[A.index('=')+1:])
                
        if 'xmax' in A.lower():
            if proceed_int:
                stop[tiers][cnt] = float(A[A.index('=')+1:])
            else:
                xmax = float(A[A.index('=')+1:])
                
        if 'text' in A.lower():
            if proceed_int:
                lab = A[A.index('=')+1:]
                while lab[0] == ' ':
                    lab = lab[1:]
                while lab[-1] != ('"'):
                    lab = lab[:-1]
                labels[tiers].append(lab)
                cnt += 1
                if cnt + 1 > tier_len:
                    proceed_int = False
                
        if 'points: size ' in A.lower():
            tiers += 1
            tier_len = int(A[A.index('=')+1:])
            labels.append([])
            start.append(np.zeros(tier_len))
            stop.append(np.zeros(tier_len))
            cnt = 0
            proceed_pnt = True
            
        if 'time' in A.lower():
            if proceed_pnt:
                start[tiers][cnt] = float(A[A.index('=')+1:]) - POINT_BUFFER
                stop[tiers][cnt] = float(A[A.index('=')+1:]) + POINT_BUFFER
        
        if 'mark' in A.lower():
            if proceed_pnt:
                lab = A[A.index('=')+1:]
                while lab[0] == ' ':
                    lab = lab[1:]
                while lab[-1] != ('"'):
                    lab = lab[:-1]
                labels[tiers].append(lab)
                cnt += 1
                if cnt + 1 > tier_len:
                    proceed_pnt = False
            
    return labels, start, stop

def getchildren(segm, word):
    idx = np.array([ x.tag.lower()==word.lower() for x in segm ]).astype(int)
    idx2 = np.argwhere(idx).reshape(-1).astype(int)
    return [segm[x] for x in idx2]

def read_xml_segmentation_files(fileName):
              
    start = []
    dur = []
    labels = []
    stop = []
    
    if not path.exists(fileName):
        print('Error: %s not found\n', fileName)
        return labels, start, stop
    
    root = ET.parse(fileName).getroot()
    listRoot = list(root)
    varTmp = getchildren(listRoot, 'SegmentList')
    segList = list(varTmp[0])
    structSegm = getchildren(segList, 'SpeechSegment')
    nSeg = len(structSegm)
        
    for kS in range(nSeg):
        varTmp = list(structSegm[kS])
    
        structWord = getchildren(varTmp, 'word') # varTmp(arrayfun(@(x)strcmpi(x.Name,'word'), varTmp));
        nWord = len(structWord) 
        for kW in range(nWord):
            currWord = structWord[kW]
            att = currWord.attrib
            readWord = currWord.text
            readWord = readWord.replace(' ', '')
            # readWord = readWord.replace('.', '')
            # readWord = readWord.replace(',', '')
            # readWord = readWord.replace('?', '')
            # readWord = readWord.replace(';', '')
            # readWord = readWord.replace('!', '')
            # readWord = readWord.replace('/', '')
            # readWord = readWord.replace(chr(8217), '')
            # readWord = readWord.replace(chr(39), '')

            if readWord != []:  
                idx_dur = att.get('dur')
                idx_start = att.get('stime')
                dur.append(float(idx_dur))
                start.append(float(idx_start))
                labels.append(readWord)
    
    stop = [x + y for (x,y) in zip(start,dur)]
    
    return labels, start, stop

def read_json_segmentation_files(fileName):
    
    labels = []
    instants = []    
   
    if not path.exists(fileName):
        print('Error: %s not found\n', fileName)
        return labels, instants
    
    with open(fileName, 'r') as myfile:
        jstr = myfile.read().replace('\n', '')
    idjson = json.loads(jstr)    
    tiers = idjson['tiers']
    nTiers = len(tiers)
    
    if nTiers == 1 and type(tiers) is not list:
        tiers = [tiers]        
    
    for k in range(nTiers):
        events = tiers[k]['events']
        if type(events) is dict:
            events = [events]
        nEvents = len(events)     
        lblTmp = []
        instTmp = np.zeros((nEvents, 2))
        for kE in range(nEvents):
            lblTmp.append(events[kE]['segment_name'])
            instTmp[kE,:] = [ events[kE]['segment_start'], 
                             events[kE]['segment_stop'] ]
            
        labels.append(lblTmp)
        instants.append(instTmp)
    
    return labels, instants

def read_seg_segmentation_files(fileName):
    
    labels = []
    instants = []
    
    if not path.exists(fileName):
        print('Error: %s not found\n', fileName)
        return labels, instants
    
    f = open(fileName, "r")
    C = np.loadtxt(f,
                   comments=None,
                   delimiter='\n', 
                   dtype='str')
    
    nPhon = len(C)
    lblPhon = []
    instPhon = []
    lblWord = []
    instWord = []
    lblSent = []
    instSent = []
    iterSent = 0
    
    for k in range(nPhon):
        currPhon = C[k]
        if '#@ sid=' in currPhon:
            idx1 = currPhon.find('-')
            idx2 = currPhon.find('-', idx1 + 1)
            sentStart = float(currPhon[idx1+1:idx2])
            sentEnd =  float(currPhon[idx2+1:])
            sentTmp = np.array([sentStart, sentEnd]).reshape(1,-1)
            
            if iterSent == 0:
                instSent = sentTmp
            else:
                lblSent.append(lblSentTmp)
                instSent = np.vstack((instSent, sentTmp))
    
            iterSent += 1
            lblSentTmp = []
        else:
            if '#@ word' in currPhon:
                idx1 = currPhon.find('=')
                idx2 = currPhon.find(' ')
                idx2 = currPhon.find(' ', idx2 + 1)
                Word = currPhon[idx1+1:idx2]
                lblWord.append(Word)
                if lblSentTmp == []:
                    lblSentTmp = Word
                else:
                    lblSentTmp = lblSentTmp + ' ' + Word
            
            if currPhon[0] != '#':
                idx1 = currPhon.find(' ')
                idx2 = currPhon.find(' ', idx1 + 1)
                idx3 = currPhon.find(' ', idx2 + 1)
                idx4 = currPhon.find(' ', idx3 + 1)
                idx5 = currPhon.find(' ', idx4 + 1)
                idx6 = currPhon.find(' ', idx5 + 1)

                fileId = currPhon[:idx1]
                sentId = currPhon[idx1+1:idx2]
                idx2Tmp = sentId.find(':')        
                label = sentId[idx2Tmp+2]
                sentPos = sentId[-1]
                start = float(currPhon[idx3+1:idx4]) / 100 + sentStart - 1e-2
                sumC = float(currPhon[idx4+1:idx5]) / 100
                sumC += float(currPhon[idx5+1:idx6]) / 100
                
                wEnd = start + sumC + float(currPhon[idx6+1:]) / 100

                lblPhon.append(label)
                instTmp = np.array([start, wEnd]).reshape(1,-1)
                if instPhon == []:
                    instPhon = instTmp
                else:
                    instPhon = np.vstack((instPhon, instTmp))
                if sentPos in ['1', '3']:
                    if instWord == []:
                        instWord = instTmp
                    else:
                        instWord = np.vstack((instWord, instTmp))
                if sentPos in ['2', '3']:
                    instWord[-1,1] = wEnd

    instants = [instPhon, instWord, instSent]
    labels = [lblPhon, lblWord, lblSent]     
   
    return labels, instants

def read_whc_segmentation_files(fileName):
    
    labels = []
    instants = []
    
    if not path.exists(fileName):
        print('Error: %s not found\n', fileName)
        return labels, instants
    
    f = open(fileName, "r")
    C = np.loadtxt(f,
               delimiter='\n', dtype='str')
    
    nWord = len(C)
    lblWord = []
    instWord = []
    for k in range(nWord):
        currWord = C[k]  
        if currWord[0] == '(':
            idx1 = currWord.find('-')
            idx2 = currWord.find('-', idx1 + 1)
            sentStart = float(currWord[idx1+1:idx2])
        else:
            idx1 = currWord.find(' ')
            idx2 = currWord.find(' ', idx1 + 1)
            idx3 = currWord.find(' ', idx2 + 1)
            label = currWord[:idx1]
            start = float(currWord[idx1+1:idx2]) / 100 + sentStart - 1 / 100
            wEnd = float(currWord[idx2+1:idx3]) / 100 + sentStart

            lblWord.append(label)
            instTmp = np.array([start, wEnd]).reshape(1, -1)
            if instWord == []:
                instWord = instTmp
            else:
                instWord = np.vstack((instWord, instTmp))

    instants = [instWord]
    labels = [lblWord]     
   
    return labels, instants
