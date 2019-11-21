
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
    temp = len(lines[0].split(" "))
    #print("len lines",len(lines))
    for line in lines:
        #print(line)
        words = line.split(" ") 
        wordnum = len(words)
       # print(wordnum)
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
    wordnum = len(lines[0].split(" "))
    shape = (linenum, wordnum)
    arr =  np.zeros(shape) 
    for i in range( linenum):
        for j in range(wordnum):
            words = lines[i].split(" ") 
            arr[i][j] = int(words[j])
    print(arr)
    return arr

def get_PIL_by_numpy(arr):
    return Image.fromarray(arr.astype('uint8')).convert('RGB')