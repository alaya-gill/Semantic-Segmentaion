import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QBrush, QColor 
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from pyqtspinner.spinner import WaitingSpinner
from ui import Ui_MainWindow
import os
from os.path import expanduser
import sys
from PyQt5.Qt import QApplication, QClipboard
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QCheckBox,QMainWindow, QFileDialog, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QPlainTextEdit,QLabel, QFrame
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import os, os.path
import cv2
import glob
import copy 
import numpy as np
import json
import io
import codecs
from train import ModelClass
import threading
import  pickle

class MainW (QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.pushButton_2_clicked)
        self.pushButton_13.clicked.connect(self.open_dialog_box2)
        self.listWidget_5.clicked[QtCore.QModelIndex].connect(self.listWidget_5_clicked)
        self.Size_2.valueChanged.connect(self.valuechange_size2)
        self.spinBox.valueChanged.connect(self.valuechange_spinBox)
        self.spinBox_2.valueChanged.connect(self.valuechange_spinBox_2)
        self.doubleSpinBox.valueChanged.connect(self.valuechange_doubleSpinBox)
        self.pushButton_14.clicked.connect(self.pushButton_14_clicked)
        self.listWidget_4.clicked.connect(self.listWidget_4_clicked)
        self.actionOutput_Directory.triggered.connect(self.chooseDirectory)
        self.pushButton_15.clicked.connect(self.pushButton_15_clicked)
        self.pushButton_5.clicked.connect(self.pushButton_5_clicked)
        self.pushButton_6.clicked.connect(self.pushButton_6_clicked)
        self.epochs=10 
        self.batch_size=2
        self.learning_rate=0.00001
        self.pushButton_7.clicked.connect(self.pushButton_7_clicked)
        self.pushButton_9.clicked.connect(self.pushButton_9_clicked)
        self.new_image_name=""
        self.dictin={}
        self.dir=""
        self.pushButton_10.clicked.connect(self.pushButton_10_clicked)
        self.pushButton_12.clicked.connect(self.pushButton_12_clicked)
        self.check=False
        self.loaded_image_3t=False
        self.loaded_image_4t=False    

    def pushButton_10_clicked(self):
        filename = str(QFileDialog.getExistingDirectory(self,"Open a folder containing images",expanduser("~"),QFileDialog.ShowDirsOnly))
        path = str(filename)+"/"
        image_list = []
        for filename in glob.glob(path+'*.jpg'): 
            image_list.append(os.path.basename(filename))
            self.image_path3.append(filename)
        for filename in glob.glob(path+'*.png'): 
            image_list.append(os.path.basename(filename))
            self.image_path3.append(filename)
        
        self.listWidget_9.addItems(image_list)
        self.listWidget_9.clicked[QtCore.QModelIndex].connect(self.listWidget_9_clicked)
        
    def listWidget_9_clicked(self,index):
        image_name=index.data()
        self.new_image_name=image_name
        im = cv2.imread(self.image_path3[index.row()])
        im = cv2.resize(im,(480,320))
        self.original_image=im
        image = QtGui.QImage(im.data, im.shape[1], im.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        self.label_7.setPixmap(QtGui.QPixmap.fromImage(image))
        self.label_7.setScaledContents(True)
        self.label_7.setWordWrap(False)
        self.label_7.setOpenExternalLinks(False)
        self.loaded_image_4t=True

    def pushButton_12_clicked(self):
        if self.loaded_image_4t==False:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Load Original Image First by clicking on Images!!")
            msgBox.setWindowTitle("Semantic Segmentation")
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                print('OK clicked')
            return
        fileName=""
        if not self.dir:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileName(self,"Select the .pt model file", "","*.pt", options=options)
            if fileName:
                self.dir=fileName
            else:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setText("Select .pt File!!")
                msgBox.setWindowTitle("Semantic Segmentation")
                msgBox.setStandardButtons(QMessageBox.Ok)
                returnValue = msgBox.exec()
                if returnValue == QMessageBox.Ok:
                    print('OK clicked')

        fileName=self.dir
        th = threading.Thread(target=self.segmentedImage4t,args=(fileName,))
        self.label_8.setMovie(self.movie)
        self.movie.start()
        self.label_12.setVisible(False)
        self.label_8.setVisible(True)
        th.start()

    def segmentedImage4t(self,fileName):
        im=self.obj.predict(self.original_image,fileName)   
        im = cv2.resize(im,(480,320))
        image = QtGui.QImage(im.data, im.shape[1], im.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        self.label_8.setPixmap(QtGui.QPixmap.fromImage(image))
        self.label_8.setScaledContents(True)
        self.label_8.setWordWrap(False)
        self.label_8.setOpenExternalLinks(False)

    def pushButton_7_clicked(self):
        filename = str(QFileDialog.getExistingDirectory(self,"Open a folder containing labels.json file",expanduser("~"),QFileDialog.ShowDirsOnly))
        path = str(filename)+"/labels.json"
        
        if os.path.isfile(path) and os.access(path, os.R_OK):
            self.output=path
            image_list = []
            path=str(filename)+"/"
            for filename in glob.glob(path+'*.jpg'): 
                image_list.append(os.path.basename(filename))
                self.image_path2.append(filename)
            for filename in glob.glob(path+'*.png'): 
                image_list.append(os.path.basename(filename))
                self.image_path2.append(filename)
            self.listWidget_7.addItems(image_list)
            self.listWidget_7.clicked[QtCore.QModelIndex].connect(self.listWidget_7_clicked)
            with open(self.output) as f:
                self.dictin = json.loads(f.read())
            
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Directory doesn't contain labels.json file!!")
            msgBox.setWindowTitle("Semantic Segmentation")
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                print('OK clicked')

    def pushButton_9_clicked(self):
        if self.loaded_image_3t==False:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Load Ground Truth Image First by clicking on Images!!")
            msgBox.setWindowTitle("Semantic Segmentation")
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                print('OK clicked')
            return
        fileName=""
        if not self.dir:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileName(self,"Choose .pt model File", "","*.pt", options=options)
            if fileName:
                self.dir=fileName
            else:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setText("Select .pt File!!")
                msgBox.setWindowTitle("Semantic Segmentation")
                msgBox.setStandardButtons(QMessageBox.Ok)
                returnValue = msgBox.exec()
                if returnValue == QMessageBox.Ok:
                    print('OK clicked')
        
        fileName=self.dir
        try:
            with open((os.path.dirname(fileName)+"/"+(os.path.basename(fileName).replace(".pt",".sm"))), 'rb') as inp:
                sm = pickle.load(inp)
                l=[]
                i=[]
                for k,v in sm.items():
                    l.append((k,str(v)))
                
                for tup in l:
                    p=','.join([':'.join(tup)])
                    i.append(p)
                self.listWidget_8.addItems(i)
        except:
            print("No summary File")
        th = threading.Thread(target=self.segmentedImage3t,args=(fileName,))
        self.label_6.setMovie(self.movie)
        self.movie.start()
        self.label_6.setVisible(True)
        self.label_12.setVisible(False)
        th.start()

    def segmentedImage3t(self,fileName):
        print(fileName)
        im=self.obj.predict(self.original_image,fileName)
        im=cv2.imread('./Image.png')
        im = cv2.resize(im,(480,320))
        image = QtGui.QImage(im.data, im.shape[1], im.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        self.label_6.setPixmap(QtGui.QPixmap.fromImage(image))
        self.label_6.setScaledContents(True)
        self.label_6.setWordWrap(False)
        self.label_6.setOpenExternalLinks(False)
        os.remove('./Image.png')
        

    def listWidget_7_clicked(self,index):
        image_name=index.data()
        self.new_image_name=image_name
        im = cv2.imread(self.image_path2[index.row()])
        print(self.image_path2[index.row()])
        im = cv2.resize(im,(480,320))
        self.original_image=im
        new_dict={}
        new_dict=self.dictin[self.new_image_name]['region']
        for r in new_dict:
            x=(new_dict[str(r)]['x'])
            y=(new_dict[str(r)]['y'])
            l=[i for i in zip(x,y)]
            if new_dict[str(r)]['color_name']=="Red":
                cv2.fillPoly(im, np.array([l]), (0,0,255))
            elif new_dict[str(r)]['color_name']=="Green":
                cv2.fillPoly(im, np.array([l]), (0,255,0))
        self.loaded_image_3t=True

        
        image = QtGui.QImage(im.data, im.shape[1], im.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        self.label_2.setPixmap(QtGui.QPixmap.fromImage(image))
        self.label_2.setScaledContents(True)
        self.label_2.setWordWrap(False)
        self.label_2.setOpenExternalLinks(False)

    def valuechange_spinBox(self):
        self.epochs=self.spinBox.value()

    def valuechange_spinBox_2(self):
        self.batch_size=self.spinBox_2.value()

    def valuechange_doubleSpinBox(self):
        self.learning_rate=self.doubleSpinBox.value()

    def pushButton_5_clicked(self):
        if self.labels_directory=="./":
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("No Directory Chosen where Labels Exist!!")
            msgBox.setWindowTitle("Semantic Segmentation")
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                print('OK clicked')
        else:
            
            self.movie.start()
            self.label_12.setVisible(True)
            th = threading.Thread(target=self.runParallel)
            th.start()


    def runParallel(self):
        self.obj.trainModel(self.epochs,self.batch_size,self.learning_rate)
        self.label_12.setVisible(False)
        self.check=True

    def pushButton_6_clicked(self):
        if self.check:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, i = QFileDialog.getSaveFileName(self,"Choose Directory and provide the file name only!","","All Files (*);;Text Files (*.txt)", options=options)
            if fileName:
                with open(fileName+'.sm', 'wb') as output:
                    pickle.dump(self.obj.getSummary(), output, pickle.HIGHEST_PROTOCOL)
                fileName=fileName+".pt"
                self.dir=fileName
                self.obj.saveModel(fileName)
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Run Architechture First!!")
            msgBox.setWindowTitle("Semantic Segmentation")
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                print('OK clicked')
                

            
    def pushButton_2_clicked(self):
        filename = str(QFileDialog.getExistingDirectory(self,"Open a folder where labels Exist",expanduser("~"),QFileDialog.ShowDirsOnly))
        path = str(filename)+"/labels.json"
        if os.path.isfile(path) and os.access(path, os.R_OK):
            
            image_list = []
            path=str(filename)+"/"
            for filename in glob.glob(path+'*.jpg'): 
                image_list.append(os.path.basename(filename))
                self.image_path.append(filename)
            for filename in glob.glob(path+'*.png'):
                image_list.append(os.path.basename(filename))
            self.labels_directory=path
            print(self.labels_directory)
            self.listWidget_2.addItems(image_list)
            self.obj=ModelClass(path)
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Directory doesn't contain labels.json file!!")
            msgBox.setWindowTitle("Semantic Segmentation")
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                print('OK clicked')

    def chooseDirectory(self):
        filename = str(QFileDialog.getExistingDirectory(self,"Choose output directory",expanduser("~"),QFileDialog.ShowDirsOnly))
        path = str(filename)+"/"
        self.output_directory=path

    def pushButton_15_clicked(self):
        if self.output_directory==None:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Select Directory First!!")
            msgBox.setWindowTitle("Semantic Segmentation")
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                print('OK clicked')
            return
        if self.image_name=="":
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Load Image First!!")
            msgBox.setWindowTitle("Semantic Segmentation")
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                print('OK clicked')
            return
        cv2.imwrite(self.output_directory+self.image_name,self.original_image)
        items_list =self.listWidget.findItems(self.image_name,QtCore.Qt.MatchExactly)
        for item in items_list:
            r = self.listWidget.row(item)
            self.listWidget.takeItem(r)
            self.image_path.pop(r)
        
        maindict={}
        check=False
        PATH=self.output_directory + 'labels.json'
        if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
            with open(PATH) as f:
                maindict = json.loads(f.read())
                check=True
                
        out = dict()
        region = dict()
        num=0
        out["filename"] = str(self.image_name) # name of the attribute is filename
        ret, thresh = cv2.threshold(self.blank_img[:, :, 1], 127, 255, 0)
        contours, hierarchy =  cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        gx = []
        gy = []
        for k in contours:
            tmpx=[]
            tmpy=[]
            for i in k:
                
                for j in i:
                    tmpx.append(int(j[0]))
                    tmpy.append(int(j[1]))
            gx.append(tmpx)
            gy.append(tmpy)
        
        for x  ,y in zip (gx,gy):
            region[str(num)] = {}
            region[str(num)]["x"] =  x
            region[str(num)]["y"] =  y
            region[str(num)]["color_name"] = "Green"
            region[str(num)]["color_value"] = [0,255,0]
            num += 1
        ret, thresh = cv2.threshold(self.blank_img[:, :, 2], 127, 255, 0)
        contours, hierarchy =  cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        rx = []
        ry = []
        for k in contours:
            tmpx=[]
            tmpy=[]
            for i in k:
                
                for j in i:
                    tmpx.append(int(j[0]))
                    tmpy.append(int(j[1]))
            rx.append(tmpx)
            ry.append(tmpy)
        
        
        for x  ,y in zip (rx,ry):
            region[str(num)] = {}
            region[str(num)]["x"] =  x
            region[str(num)]["y"] =  y
            region[str(num)]["color_name"] = "Red"
            region[str(num)]["color_value"] = [255,0,0]
            num += 1
        out["region"] = region 
        if not(gx or gy or ry or rx):
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("You didn't draw anything!!")
            msgBox.setWindowTitle("Semantic Segmentation")
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                print('OK clicked')
        else:
            if check:
                m={str(self.image_name):out}
                with open(PATH, 'w') as outfile:
                    maindict.update(m)
                    json.dump(maindict, outfile)
            else:
                maindict={str(self.image_name):out}
                with open(PATH, 'w') as outfile:
                    json.dump(maindict, outfile)
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Save Successful!!")
            msgBox.setWindowTitle("Semantic Segmentation")
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                print('OK clicked')
        


    def open_dialog_box2(self):
        filename = str(QFileDialog.getExistingDirectory(self,"Open a folder containing images",expanduser("~"),QFileDialog.ShowDirsOnly))
        path = str(filename)+"/"
        self.output=path
        image_list = []
        for filename in glob.glob(path+'*.jpg'): 
            image_list.append(os.path.basename(filename))
            self.image_path.append(filename)
        for filename in glob.glob(path+'*.png'): 
            image_list.append(os.path.basename(filename))
            self.image_path.append(filename)
        if not image_list:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Choose Directory with Images!!")
            msgBox.setWindowTitle("Semantic Segmentation")
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                print('OK clicked')
        else:
            self.listWidget.addItems(image_list)
            self.listWidget.clicked[QtCore.QModelIndex].connect(self.listWidget_clicked)
        
    def listWidget_clicked(self, index):
        self.image_name=index.data()
        self.im = cv2.imread(self.image_path[index.row()])
        self.im = cv2.resize(self.im,(480,320))
        self.blank_img=np.zeros((320,480,3),np.uint8 )
        self.original_image=self.im
        self.undo=[copy.deepcopy(self.blank_img)]
        self.overlay=self.im.copy()
        self.image = QtGui.QImage(self.im.data, self.im.shape[1], self.im.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        self.label.setPixmap(QtGui.QPixmap.fromImage(self.image))
        self.label.setScaledContents(True)
        self.label.setWordWrap(False)
        self.label.setOpenExternalLinks(False)
        self.loaded_image=True
    

    def listWidget_5_clicked(self,index):
        if index.data()=="Brush":
            self.polygon=False
            self.brush=True
            self.count=0
        elif index.data()=="Polygon":
            self.brush=False
            self.polygon=True
            self.count=0
        
    def listWidget_4_clicked(self,index):
        if index.data()=="Trees" and (self.polygon or self.brush):
            self.brush_color=(0, 255, 0)
        elif index.data()=="Banners" and (self.polygon or self.brush):
            self.brush_color=(0, 0, 255)
    def valuechange_size2(self):
      self.brush_size=self.Size_2.value()

    def pushButton_14_clicked(self):
        if not self.undo:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Draw on Image First!!")
            msgBox.setWindowTitle("Semantic Segmentation")
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                print('OK clicked')
        if len(self.undo) ==1:
            self.blank_img=np.zeros((320,480,3),np.uint8 )
            if self.polygon and len(self.points)>0:
                self.points.pop()
            self.undo=[copy.deepcopy(self.blank_img)]
            im=self.im
            self.image = QtGui.QImage(im.data, im.shape[1], im.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
            self.label.setPixmap(QtGui.QPixmap.fromImage(self.image))
            self.label.setScaledContents(True)
            self.label.setWordWrap(False)
            self.label.setOpenExternalLinks(False)
        elif len(self.undo) >1:
            alpha=0.5
            self.undo.pop()
            if self.polygon and len(self.points)>0:
                self.points.pop()
            im=copy.deepcopy(self.undo[-1])
            self.blank_img=copy.deepcopy(self.undo[-1])
            original=copy.deepcopy(self.im)
            original[np.where((original == [0,0,0]).all(axis = 2))] = [255,255,255]
            im = cv2.addWeighted(self.blank_img, alpha, original, 1 , 0)
            self.image = QtGui.QImage(im.data, im.shape[1], im.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
            self.label.setPixmap(QtGui.QPixmap.fromImage(self.image))
            self.label.setScaledContents(True)
            self.label.setWordWrap(False)
            self.label.setOpenExternalLinks(False)
            if self.polygon  and len(self.points)==1:
                self.points.pop()
            if len(self.undo) ==1:
                if self.polygon and len(self.points)>0:
                    self.points.pop()
                self.blank_img=np.zeros((320,480,3),np.uint8 )
                self.undo=[copy.deepcopy(self.blank_img)]
                im=self.im
                self.image = QtGui.QImage(im.data, im.shape[1], im.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
                self.label.setPixmap(QtGui.QPixmap.fromImage(self.image))
                self.label.setScaledContents(True)
                self.label.setWordWrap(False)
                self.label.setOpenExternalLinks(False)




if __name__ == '__main__':

    app = QApplication(sys.argv)
    myapp = MainW()
    myapp.show()
    sys.exit(app.exec_())