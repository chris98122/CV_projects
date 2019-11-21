
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

def process_SE(str):
    return  np.array([[1,1,1],
                      [ 1, 1, 1],
                      [ 1, 1, 1]])

def get_PIL_by_numpy(arr):
    return Image.fromarray(arr.astype('uint8')).convert('RGB')