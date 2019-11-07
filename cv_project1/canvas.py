
import hashlib
import re
import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 


class Canvas(QWidget):
    
    def __init__(self, *args, **kwargs):
        super(Canvas, self).__init__(*args, **kwargs) 
        self.pixmap = QPixmap()
        self.visible = {} 
        self._painter = QPainter()
        
        self.offsets = QPointF(), QPointF()
        self.scale = 1.0
    
    def loadPixmap(self, pixmap):
        try: 
            self.pixmap = pixmap
            self.update() 
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        

    
    def paintEvent(self, event): 
        if not self.pixmap:
            return super(Canvas, self).paintEvent(event)

        p = self._painter
        p.begin(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.HighQualityAntialiasing)
        p.setRenderHint(QPainter.SmoothPixmapTransform)

        p.scale(self.scale, self.scale) 

        p.drawPixmap(0, 0, self.pixmap) 
        p.end()
