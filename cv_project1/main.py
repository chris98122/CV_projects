 

import sys
#PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中
from PyQt5.QtWidgets import QApplication, QMainWindow
from util import *
from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets

import os.path
import platform
import subprocess
from functools import partial

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
#导入designer工具生成的login模块 

__appname__="project 1 by chris"
class WindowMixin(object):

    def menu(self, title, actions=None):
        menu = self.menuBar().addMenu(title) 
        if actions:
            addActions(menu, actions)
        return menu
 

class MainWindow(QMainWindow, WindowMixin):
    def __init__(self, parent=None): 
        super(MainWindow, self).__init__()
        self.setWindowTitle(__appname__)
        self.setGeometry(300, 300,800, 600) 

 
        self.menus = struct(
        file=self.menu('&File'),
        help=self.menu('&Help')) 
         
        
        self.image = QImage()
        self.filePath = None
        self.imageData = None

        action = partial(newAction, self)
        
        open = action('openFile', self.openFile,
                      'Ctrl+O', 'open', 'openImg')

        
        save = action('save', self.saveFile,
                      'Ctrl+S', 'save', 'saveImg', enabled=False)

        saveAs = action( 'saveAs', self.saveFileAs,
                        'Ctrl+Shift+S', 'save-as','saveAsDetail', enabled=False)

        
        addActions(self.menus.file,
                   (open, save, saveAs ))

        help = action( 'tutorial' , self.showTutorialDialog, None, 'help',  'tutorialDetail' )
        showInfo = action('info', self.showInfoDialog, None, 'help', 'info')

        addActions(self.menus.help,  (help,showInfo))

        
    def openFile(self, _value=False): 
        path = os.path.dirname(self.filePath) if self.filePath else '.'
        formats = ['*.%s' % fmt.data().decode("ascii").lower() for fmt in QImageReader.supportedImageFormats()] 
        filename = QFileDialog.getOpenFileName(self, '%s - Choose Image or Label file' % __appname__, path)
        if filename:
            if isinstance(filename, (tuple, list)):
                filename = filename[0]
                if filename:
                    self.loadFile(filename)

    
    def loadFile(self, filePath=None): 
        filePath = os.path.abspath(filePath)    
        
        if filePath and os.path.exists(filePath):
            self.imageData = read(filePath, None)    
            image = QImage.fromData(self.imageData)
            if image.isNull():
                self.errorMessage(u'Error opening file',
                                u"<p>Make sure <i>%s</i> is a valid image file." %   filePath)
                self.status("Error reading %s" %  filePath)
                return False
        
            self.image = image
            self.filePath = filePath 
            self.canvas.loadPixmap(QPixmap.fromImage(image))

            #写到这里 还没写canvas

 
    def saveFile(self, _value=False):
        if self.defaultSaveDir is not None and len( self.defaultSaveDir ):
            if self.filePath:
                imgFileName = os.path.basename(self.filePath)
                savedFileName = os.path.splitext(imgFileName)[0]
                savedPath = os.path.join(self.defaultSaveDir, savedFileName)
                self._saveFile(savedPath)
        else:
            imgFileDir = os.path.dirname(self.filePath)
            imgFileName = os.path.basename(self.filePath)
            savedFileName = os.path.splitext(imgFileName)[0]
            savedPath = os.path.join(imgFileDir, savedFileName)
            self._saveFile(savedPath if self.labelFile
                           else self.saveFileDialog(removeExt=False))

    def saveFileAs(self, _value=False):
        assert not self.image.isNull(), "cannot save empty image"
        self._saveFile(self.saveFileDialog())
 


    def showInfoDialog(self):
        msg = u"Name:{0}\nProgram to realize the convolution operation and the next filters,Roberts operator;".format(__appname__ )+ \
            "Prewitt operator; Sobel operator;"+\
            "Gaussian filter, mean filter and Median filter\n"+ \
            "Kernal size and sigma adjustable" 
        QMessageBox.information(self, u'Information', msg)
    
    ## Callbacks ##
    def showTutorialDialog(self):
        msg = u"load images, click the corrisponding button, set Kernel size and sigma, and save images."
        QMessageBox.information(self, u'Tutorial', msg)

def read(filename, default=None):
        try:
            with open(filename, 'rb') as f:
                return f.read()
        except:
            return default
if __name__ == "__main__":
    #固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    #初始化
    myWin = MainWindow()
    #将窗口控件显示在屏幕上
    myWin.show()
    #程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())