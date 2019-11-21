
import hashlib
import re
import sys
from PyQt5 import  QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 

import copy
import numpy as np


from PIL import Image 
def valid_SE(input):
    lines = input.split('\n') 
    linenum=len(lines)
    
    temp = 0
    #print("len lines",len(lines))
    for i in range( linenum):
        #print(line)
        lines[i] = lines[i].strip()
        words = lines[i].split(" ") 
        wordnum = len(words)
        if i == 0:
            temp = wordnum
        for word in words:
            if int(word) is None:
                return False   
        if temp != wordnum:
            return False 
        temp = wordnum
    print("valid")
    return True
    
def process_SE(input):
    lines = input.split('\n')
    linenum=len(lines)
    wordnum = len(lines[0].strip().split(" "))
    shape = (linenum, wordnum)
    arr =  np.zeros(shape) 
    for i in range( linenum):
        for j in range(wordnum):
            lines[i] = lines[i].strip()
            words = lines[i].split(" ") 
            arr[i][j] = int(words[j])
    print(arr)
    return arr

def get_PIL_by_numpy(arr):
    return Image.fromarray(arr.astype('uint8')).convert('RGB')