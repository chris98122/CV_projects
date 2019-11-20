import sys, os.path, tempfile
from PyQt5.QtWidgets import QFileDialog, QLabel, QAction,\
    QApplication, QMenuBar, QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QEvent
from PIL import Image, ImageFilter, ImageGrab

from filters import *
from util import *
class PhotoFilter(QWidget):

    def __init__(self):
        super().__init__()
        self.ui()

    def ui(self):
        self.fname = QFileDialog.getOpenFileName(self, 'Open file')[0]
        self.td = tempfile.TemporaryDirectory()
        screen_res = ImageGrab.grab().size

        self.lbl = QLabel(self)
        self.lbl.setAlignment(Qt.AlignCenter)
        self.pixmap = QPixmap(self.fname)
        self.lbl.setPixmap(self.pixmap)
        self.lbl.setMinimumSize(screen_res[0] // 10, screen_res[1] // 10)
        self.lbl.installEventFilter(self)
        hbox = QVBoxLayout(self)
        hbox.addWidget(self.lbl)
        self.setLayout(hbox)
        self.setGeometry(screen_res[0] // 5, screen_res[1] // 5, screen_res[0]
                         // 2, screen_res[1] // 2)
        self.setWindowState(Qt.WindowMaximized)
        self.setWindowTitle('project1 by chris')
        self.setWindowIcon(QIcon(self.resource_path('data\Logo.ico')))

        openFile = QAction('Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open file')
        openFile.triggered.connect(self.open_file)

        saveFile = QAction('Save As...', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.setStatusTip('Save file as...')
        saveFile.triggered.connect(self.save_file)

        Gaussian = QAction('Gaussian filter', self)
        Gaussian.setShortcut('ctrl+G')
        Gaussian.setStatusTip('Gaussian filter')
        Gaussian.triggered.connect(self.Gaussian_filter)
 
        Prewitt = QAction('Prewitt_operation', self) 
        Prewitt.setShortcut('ctrl+P')
        Prewitt.setStatusTip('prewitt op')
        Prewitt.triggered.connect(self. Prewitt_op)

        
        Roberts = QAction('Roberts operation', self) 
        Roberts .setShortcut('ctrl+R')
        Roberts.setStatusTip('Roberts_operation')
        Roberts.triggered.connect(self. Roberts_op)

        
        Sobel = QAction('Sobel operation', self)  
        Sobel.setShortcut('ctrl+L')
        Sobel.setStatusTip('sobel operation')
        Sobel.triggered.connect(self. Sobel_op)

        mean= QAction('mean filter', self)
        mean.setShortcut('ctrl+M') 
        mean.setStatusTip('mean_filter')
        mean.triggered.connect(self.mean_filter)


        median= QAction('median filter', self) 
        median.setShortcut('ctrl+N') 
        median.setStatusTip('median filter')
        median.triggered.connect(self.Median_filter)

        menubar = QMenuBar()
        fileMenu = menubar.addMenu('&File')
        filterMenu = menubar.addMenu('&Filters')
        fileMenu.addAction(openFile)
        fileMenu.addAction(saveFile)
        filterMenu.addAction(Gaussian)  
        filterMenu.addAction(Roberts)
        filterMenu.addAction(Sobel) 
        filterMenu.addAction(Prewitt )
        filterMenu.addAction(mean)
        filterMenu.addAction(median)
        hbox.setMenuBar(menubar)
            
        self.arr = None
        self.kernel_size = 5
        self.sigma = 1
 
        self.kernel_text = QLineEdit(self)
        self.kernel_text.textChanged[str].connect(self.kernel_text_OnChanged) 

        self.sigma_text = QLineEdit(self)
        self.sigma_text.textChanged[str].connect(self.sigma_text_OnChanged) 

        self.kernel_text.setAlignment(Qt.AlignBottom)
        
        self.kernel_text.setMaximumWidth(100)

        self.ql = QLabel("kernel size")
        self.ql .setAlignment(Qt.AlignBottom) 
        self.ql.setMaximumHeight(20)
        hbox.addWidget( self.ql  )  
        
        hbox.addWidget(  self.kernel_text)  
        self.ql2= QLabel("sigma size")
        self.ql2.setMaximumHeight(20)
        self.ql2 .setAlignment(Qt.AlignBottom)
        hbox.addWidget(self.ql2 )   
        self.sigma_text.setAlignment(Qt.AlignBottom)
        self.sigma_text.setMaximumWidth(100)
        hbox.addWidget(  self.sigma_text)

    def eventFilter(self, source, event):
        if (source is self.lbl and event.type() == QEvent.Resize):
            self.lbl.setPixmap(self.pixmap.scaled(
                self.lbl.size(), Qt.KeepAspectRatio))
        return super(PhotoFilter, self).eventFilter(source, event)

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def screen_print(self, name):
        self.pixmap = QPixmap(name)
        self.lbl.setPixmap(self.pixmap.scaled(
            self.lbl.size(), Qt.KeepAspectRatio))

    def open_file(self):
        ofname = QFileDialog.getOpenFileName(self, 'Open file')[0]

        if ofname:
            self.fname = ofname
            self.screen_print(self.fname)

    def save_file(self):
        if self.fname:
            sname = QFileDialog.getSaveFileName(self, 'Save file')[0]

            if sname:
                sname = sname + '.' + (self.fname).split('.')[-1]
                sf = Image.open(((self.td).name).replace('\\', '/') + '/' +
                                (self.fname).split('/')[-1])
                sf.save(sname)

                self.screen_print(sname)

    def show_file(self, im):
        fn = ((self.td).name).replace('\\', '/') + '/' +\
             (self.fname).split('/')[-1]
        im.save(fn)

        self.screen_print(fn)

    def Gaussian_filter(self): 
        self.filter_implement(Gaussian_filter_implement,self.fname,self.kernel_size,self.sigma) 


    def Prewitt_op(self):
        self.filter_implement(Prewitt_op_implement,self.fname)

    def Sobel_op(self): 
        self.filter_implement(Sobel_op_implement,self.fname)
 
    def mean_filter(self):
        self.filter_implement(mean_filter_implement,self.fname,self.kernel_size)


    def Median_filter(self):
        self.filter_implement(median_filter_implement,self.fname,self.kernel_size)


    def Roberts_op(self): 
        self.filter_implement(Roberts_op_implement,self.fname)

    def filter_implement(self,funct,fname,*args): 
        if self.fname:
            im = Image.open(self.fname)
            if im.mode != 'RGB':
                im = im.convert('RGB')

            x, y = im.size
            arr = np.array(im)
            if args is None:
                arr = funct(arr) 
            else:
                arr = funct(*args,arr) 
            im = get_PIL_by_numpy(arr)
            
            self.show_file(im)


    def kernel_text_OnChanged(self,text):
        # add text to selected shape
        try:
            if int(text) is not None:
                self.kernel_size =  int(text)
            else:
                self.kernel_size = 5
        
        except:
            self.kernel_size = 5
        

    def sigma_text_OnChanged(self,text):
        # add text to selected shape
        try:
            if float(text) is not None:
                if  float(text) <= 1 and float(text)>0:
                    self.sigma = int(text) 
        except: 
                self.sigma =1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pf = PhotoFilter()
    pf.show()
    sys.exit(app.exec_())
