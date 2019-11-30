import sys, os.path, tempfile
from PyQt5.QtWidgets import QFileDialog, QLabel, QAction,\
    QApplication, QMenuBar, QWidget, QVBoxLayout,QTextEdit,QLineEdit,QHBoxLayout
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QEvent
from PIL import Image, ImageFilter, ImageGrab
from PyQt5 import QtCore, QtGui, QtWidgets
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
        hbox = QHBoxLayout(self)
        
        self.setLayout(hbox)
        self.setGeometry(screen_res[0] // 5, screen_res[1] // 5, screen_res[0]
                         // 2, screen_res[1] // 2)
        self.setWindowState(Qt.WindowMaximized)
        self.setWindowTitle('project2 by chris')
        self.setWindowIcon(QIcon(self.resource_path('data\Logo.ico')))

        openFile = QAction('Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open file')
        openFile.triggered.connect(self.open_file)

        saveFile = QAction('Save As...', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.setStatusTip('Save file as...')
        saveFile.triggered.connect(self.save_file) 

        edge_standard = QAction('Morphological edge detection(Standard)', self)
        edge_standard.setShortcut('ctrl+Q') 
        edge_standard.triggered.connect(self.edge_standard )


        
        edge_external = QAction('Morphological edge detection(external)', self)
        edge_external.setShortcut('ctrl+R') 
        edge_external.triggered.connect(self.edge_external )


        
        edge_internal = QAction('Morphological edge detection(internal)', self)
        edge_internal.setShortcut('ctrl+T') 
        edge_internal.triggered.connect(self.edge_internal )

 
        gradient= QAction('Morphological gradient', self)
        gradient.setShortcut('ctrl+M')
        gradient.setStatusTip('Morphological gradient')
        gradient.triggered.connect(self.gradient)

        cond_dilation= QAction('Binary Reconstruction', self)
        cond_dilation.setShortcut('ctrl+N')
        cond_dilation.setStatusTip('Binary Reconstruction')
        cond_dilation.triggered.connect(self.cond_dilation)
        
        grey_reconstruction= QAction('Gray scale Reconstruction', self)
        grey_reconstruction.setShortcut('ctrl+J')
        grey_reconstruction.setStatusTip('Gray scale Reconstruction')
        grey_reconstruction.triggered.connect(self.grey_reconstruction)

        menubar = QMenuBar()
        fileMenu = menubar.addMenu('&File')
        filterMenu = menubar.addMenu('&Filters')
        fileMenu.addAction(openFile)
        fileMenu.addAction(saveFile)

        filterMenu.addAction(edge_standard)
        filterMenu.addAction(edge_external)
        filterMenu.addAction(edge_internal)


        filterMenu.addAction(gradient) 
        filterMenu.addAction(cond_dilation) 
        filterMenu.addAction(grey_reconstruction) 
        
        hbox.setMenuBar(menubar)

        self.ql2= QLabel("SE")
        self.ql2.setMaximumHeight(20) 
        self.ql2.setAlignment(Qt.AlignBottom) 
        
        self.ql= QLabel("VALID")
        self.ql.setMaximumHeight(20)  
        self.ql.setAlignment(Qt.AlignBottom) 

        self.SE_edit=QTextEdit(self) 
        self.SE_edit.setMaximumWidth(300)
        self.SE_edit.setMaximumHeight(300)
        self.SE_edit.setText("1 1 1 \n1 1 1 \n1 1 1")
        self.SE_edit.setAlignment(Qt.AlignBottom) 

        self.ql3= QLabel("center (start from 0,0)")
        self.ql3.setMaximumHeight(20)
        self.ql3.setAlignment(Qt.AlignBottom) 

        self.ql4= QLabel("VALID")
        self.ql4.setMaximumHeight(20)
        self.ql4.setAlignment(Qt.AlignBottom)

        self.center_edit=QLineEdit(self)  
        self.center_edit.setMaximumWidth(300)
        self.center_edit.setMaximumHeight(20)
        self.center_edit.setText("0 0")
        self.center_edit.setAlignment(Qt.AlignBottom)
        self.center_edit.textChanged.connect(self.center_edit_OnChanged)  
        self.SE_edit.textChanged.connect(self.SE_edit_OnChanged) 

        childlayout = QVBoxLayout(self) 
        childlayout.addWidget(self.ql2)
        childlayout.addWidget(self.ql)
        childlayout.addWidget(self.SE_edit)
        childlayout.addWidget(self.ql3)
        childlayout.addWidget(self.ql4)
        childlayout.addWidget(self.center_edit) 
        childlayout.setAlignment(Qt.AlignVCenter)

        hbox.addLayout(childlayout) 
        hbox.addWidget(self.lbl)

        self.arr = None
        self.SE =  np.array([[1,1,1],
                      [ 1, 1, 1],
                      [ 1, 1, 1]])
        self.center =  [0,0]


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

 


    def edge_standard(self):
        if self.fname:
            im = Image.open(self.fname)
            if im.mode != 'RGB':
                im = im.convert('RGB')

            x, y = im.size
            arr = np.array(im)

            arr =  edge_detection(arr,self.SE,self.center ,STANDARD)
            im = get_PIL_by_numpy(arr)
            
            self.show_file(im)

    def edge_external(self):
        if self.fname:
            im = Image.open(self.fname)
            if im.mode != 'RGB':
                im = im.convert('RGB')

            x, y = im.size
            arr = np.array(im)

            arr =  edge_detection(arr,self.SE,self.center ,EXTERNAL)
            im = get_PIL_by_numpy(arr)
            
            self.show_file(im)

    def edge_internal(self):
        if self.fname:
            im = Image.open(self.fname)
            if im.mode != 'RGB':
                im = im.convert('RGB')

            x, y = im.size
            arr = np.array(im)

            arr =  edge_detection(arr,self.SE,self.center ,INTERNAL)
            im = get_PIL_by_numpy(arr)
            
            self.show_file(im)



    def gradient(self):
         if self.fname:
            im = Image.open(self.fname)
            if im.mode != 'RGB':
                im = im.convert('RGB')

            x, y = im.size
            arr = np.array(im)

            arr =  gradient(arr,self.SE,self.center )
            im = get_PIL_by_numpy(arr)
            
            self.show_file(im)

    def cond_dilation(self): 
         if self.fname:
            im = Image.open(self.fname)
            if im.mode != 'RGB':
                im = im.convert('RGB')

            x, y = im.size
            arr = np.array(im)

            arr =  conditional_dilation(arr,self.SE,self.center )
            im = get_PIL_by_numpy(arr)
            
            self.show_file(im)     
    
    def grey_reconstruction(self):
         if self.fname:
            im = Image.open(self.fname)
            if im.mode != 'RGB':
                im = im.convert('RGB')

            x, y = im.size
            arr = np.array(im)
            arr =  gray_recon(arr,self.SE,self.center )
            im = get_PIL_by_numpy(arr)
            
            self.show_file(im)     
 
    def SE_edit_OnChanged(self):
        try:
            if valid_SE(self.SE_edit.toPlainText()):
                self.ql.setText("VALID") 
                self.SE = process_SE(self.SE_edit.toPlainText())   
            else:
                self.ql.setText("not valid,use default SE") 
                self.SE =  np.array([[1,1,1],
                        [ 1, 1, 1],
                        [ 1, 1, 1]])
        except: 
            self.ql.setText("not valid,use default SE") 
            self.SE =  np.array([[1,1,1],
                      [ 1, 1, 1],
                      [ 1, 1, 1]])
        self.center_edit_OnChanged(self.center_edit.text())

    def center_edit_OnChanged(self,text):
        try:
            if valid_center(text,self.SE):
                self.ql4.setText("VALID") 
                self.center = process_center(text,self.SE)          
            else:
                self.ql4.setText("not valid,use default center 0,0")        
                self.center = [0,0]
        except: 
            self.ql4.setText("not valid,use default center 0,0")        
            self.center = [0,0]
   

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pf = PhotoFilter()
    pf.show()
    sys.exit(app.exec_())
