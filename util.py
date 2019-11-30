
import hashlib
import re
import sys
from PyQt5 import  QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 
import re
import copy
import numpy as np


from PIL import Image 


STANDARD = 1
EXTERNAL =2
INTERNAL =3
def valid_SE(input):
    lines = input.split('\n') 
    linenum=len(lines)
    
    temp = 0
    #print("len lines",len(lines))
    for i in range( linenum):
        #print(line)
        lines[i] = lines[i].strip()
        regex = re.compile('\s+')
        words = regex.split(lines[i]) 
        wordnum = len(words)
        if i == 0:
            temp = wordnum
        for word in words:
            if int(word) is None:
                return False   
        if temp != wordnum:
            return False 
        temp = wordnum
        if linenum == 1 and wordnum == 1:
            return False

    print("valid")
    return True
    
def process_SE(input):
    lines = input.split('\n')
    linenum=len(lines)
    regex = re.compile('\s+')
    wordnum = len( regex.split(lines[0].strip()))
    shape = (linenum, wordnum)
    arr =  np.zeros(shape) 
    for i in range( linenum):
        for j in range(wordnum):
            lines[i] = lines[i].strip()
            words =  regex.split(lines[i])
            arr[i][j] = int(words[j])
    print(arr)
    return arr

def valid_center(input,SE):
    # check two  num  
    regex = re.compile('\s+')
    wordnum = len(regex.split(input.strip()))
    if wordnum !=2: 
        return False
    # check two int num
    words = regex.split(input.strip())
    if int(words[0]) is None or int(words[1]) is None:
        return False
    # check size overflow
    x = int(words[0]) 
    y = int(words[1]) 
    if x > SE.shape[0] -1 or y > SE.shape[1] -1 :
        return False
    return True

def process_center(input,SE):
    regex = re.compile('\s+')
    words =  regex.split(input.strip())
    return [ int(words[0]) , int(words[1]) ]

def get_PIL_by_numpy(arr):
    return Image.fromarray(arr.astype('uint8')).convert('RGB')