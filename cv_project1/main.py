 

import sys
#PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中
from PyQt5.QtWidgets import QApplication, QMainWindow
from util import *
from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets

import os.path
import platform
import subprocess

from canvas import Canvas
from zoomWidget import ZoomWidget
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
    
    FIT_WINDOW, FIT_WIDTH, MANUAL_ZOOM = list(range(3))

    def __init__(self, parent=None): 
        super(MainWindow, self).__init__()
        self.setWindowTitle(__appname__)
        
        self.x_size = 800
        self.y_size = 600
        self.setGeometry(300, 300,self.x_size ,  self.y_size )  
        self.menus = struct(
        file=self.menu('&File'),
        help=self.menu('&Help'),
        view=self.menu('&View'))
         
        self.defaultSaveDir = None
        self.filePath = None
        self.imageData = None
        self.pixmap = None
        
        # Whether we need to save or not.
        self.dirty = False

        self.canvas = Canvas(parent=self)
        
        self.image = QImage()
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
        
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.canvas)
        self.scroll.setWidgetResizable(True)  
        self.setCentralWidget(self.scroll)


        self.scalers = {
            self.FIT_WINDOW: self.scaleFitWindow,
            self.FIT_WIDTH: self.scaleFitWidth,
            # Set to one to scale to 100% when loading files.
            self.MANUAL_ZOOM: lambda: 1,
        }

        self.zoomMode = self.MANUAL_ZOOM
        
        zoomIn = action( 'zoomin' , partial(self.addZoom, 10),
                        'Ctrl++', 'zoom-in', 'zoominDetail' , enabled=False)
        zoomOut = action( 'zoomout' , partial(self.addZoom, -10),
                         'Ctrl+-', 'zoom-out',  'zoomoutDetail', enabled=False)
        zoomOrg = action( 'originalsize' , partial(self.setZoom, 100),
                         'Ctrl+=', 'zoom',  'originalsizeDetail' , enabled=False)
        fitWindow = action( 'fitWin' , self.setFitWindow,
                           'Ctrl+F', 'fit-window',  'fitWinDetail' ,
                           checkable=True, enabled=False)
        fitWidth = action( 'fitWidth' , self.setFitWidth,
                          'Ctrl+Shift+F', 'fit-width',  'fitWidthDetail' ,
                          checkable=True, enabled=False)


        self.zoomWidget = ZoomWidget()

        zoom = QWidgetAction(self)
        zoom.setDefaultWidget(self.zoomWidget)
        self.zoomWidget.setWhatsThis(
            u"Zoom in or out of the image. Also accessible with"
            " %s and %s from the canvas." % (fmtShortcut("Ctrl+[-+]"),
                                             fmtShortcut("Ctrl+Wheel")))
   

        zoomActions = (self.zoomWidget, zoomIn, zoomOut,
                       zoomOrg, fitWindow, fitWidth)
        
        addActions(self.menus.view, ( 
            zoomIn, zoomOut, zoomOrg,
            fitWindow, fitWidth))

        Roberts = action('Roberts operator', self.Roberts_op,
                        None, 'Roberts operator', 'Roberts operator',
                        enabled=False)

        # Callbacks:
        self.zoomWidget.valueChanged.connect(self.paintCanvas)

        self.actions = struct(save=save,   saveAs=saveAs, open=open,    zoom=zoom, zoomIn=zoomIn, zoomOut=zoomOut, zoomOrg=zoomOrg,
                              fitWindow=fitWindow, fitWidth=fitWidth,
                              zoomActions=zoomActions,
                                onLoadActive=(
                                Roberts,Roberts))
        
        self.RobertsButton = QToolButton()
        self.RobertsButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.RobertsButton.setText('Roberts operator')

       
        self.RobertsButton.setDefaultAction(Roberts)

       
        listLayout = QVBoxLayout()
        listLayout.setContentsMargins(0, 0, 0, 0)
        listLayout.addWidget(self.RobertsButton)
        
        
        buttonListContainer = QWidget()
        buttonListContainer.setLayout(listLayout)

        self.dock = QDockWidget('filters', self)
        self.dock.setObjectName('filters')
        self.dock.setWidget(buttonListContainer)
        
        self.dockFeatures = QDockWidget.DockWidgetClosable | QDockWidget.DockWidgetFloatable
        self.dock.setFeatures(self.dock.features() ^ self.dockFeatures)
        
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock)


    
    def setDirty(self):
        self.dirty = True
        self.actions.save.setEnabled(True)

    def Roberts_op(self):
        print("roberts op")
        self.setDirty()

    def scaleFitWindow(self):
        """Figure out the size of the pixmap in order to fit the main widget."""
        e = 2.0  # So that no scrollbars are generated.
        w1 = self.centralWidget().width() - e
        h1 = self.centralWidget().height() - e
        a1 = w1 / h1
        # Calculate a new scale value based on the pixmap's aspect ratio.
        w2 = self.canvas.pixmap.width() - 0.0
        h2 = self.canvas.pixmap.height() - 0.0
        a2 = w2 / h2
        return w1 / w2 if a2 >= a1 else h1 / h2
    
    def scaleFitWidth(self):
        # The epsilon does not seem to work too well here.
        w = self.centralWidget().width() - 2.0
        return w / self.canvas.pixmap.width()

    def setFitWindow(self, value=True):
        if value:
            self.actions.fitWidth.setChecked(False)
        self.zoomMode = self.FIT_WINDOW if value else self.MANUAL_ZOOM
        self.adjustScale()
    
    def setFitWidth(self, value=True):
        if value:
            self.actions.fitWindow.setChecked(False)
        self.zoomMode = self.FIT_WIDTH if value else self.MANUAL_ZOOM
        self.adjustScale()

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
        
            print("Loaded %s" % os.path.basename(filePath))
            self.image = image
            self.filePath = filePath  
            self.pixmap = QPixmap.fromImage(image)
            
            self.canvas.setEnabled(True)
            self.canvas.loadPixmap(self.pixmap)
            #写到这里 还没写canvas 
            
            self.adjustScale(initial=True)
            self.paintCanvas() 
            self.toggleActions(True)

    def toggleActions(self, value=True):
        """Enable/Disable widgets which depend on an opened image."""
        for z in self.actions.zoomActions:
            z.setEnabled(value) 
            print("enabled")
        for action in self.actions.onLoadActive:
            action.setEnabled(value)

    def setZoom(self, value):
        self.actions.fitWidth.setChecked(False)
        self.actions.fitWindow.setChecked(False)
        self.zoomMode = self.MANUAL_ZOOM
        self.zoomWidget.setValue(value)

    def addZoom(self, increment=10):
        self.setZoom(self.zoomWidget.value() + increment)


    def resizeEvent(self, event):
        if self.canvas and not self.image.isNull() and self.zoomMode != self.MANUAL_ZOOM:
            self.adjustScale()
        super(MainWindow, self).resizeEvent(event)

    def paintCanvas(self):
        assert not self.image.isNull(), "cannot paint null image"   
        self.canvas.scale = 0.01 * self.zoomWidget.value() 
        self.canvas.adjustSize()
        self.canvas.update()

    
    def adjustScale(self, initial=False):
        value = self.scalers[self.FIT_WINDOW if initial else self.zoomMode]()
        self.zoomWidget.setValue(int(100 * value))

 
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