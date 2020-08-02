import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import QApplication, QClipboard
from PyQt5 import QtCore, QtWidgets
from PyQt5.Qt import QApplication, QClipboard
from PyQt5 import QtCore, QtWidgets
class main_window(QMainWindow):
     def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle(QApplication.translate("MainWindow", "PixelAnnotationTool "))
        self.list_label.setSpacing(1)
        self.image_canvas = None
        self._isLoadingLabels = False
        self.save_action = QAction(tr("&Save current image"), self)
        self.copy_mask_action =  QAction(tr("&Copy Mask"), self)
        self.paste_mask_action =  QAction(tr("&Paste Mask"), self)
        self.clear_mask_action =  QAction(tr("&Clear Mask mask"), self)
        self.close_tab_action =  QAction(tr("&Close current tab"), self)
        self.swap_action =  QAction(tr("&Swap check box Watershed"), self)
        self.undo_action =  QAction(tr("&Undo"), self)
        self.redo_action =  QAction(tr("&Redo"), self)
        self.next_file_action =  QAction(tr("&Select next file"), self)
        self.previous_file_action =  QAction(tr("&Select previous file"), self)
        self.undo_action.setShortcuts(QKeySequence.Undo)
        self.redo_action.setShortcuts(QKeySequence.Redo)
        self.save_action.setShortcut(Qt.CTRL + Qt.Key_S)
        self.swap_action.setShortcut(Qt.CTRL + Qt.Key_Space)
        self.copy_mask_action.setShortcut(Qt.CTRL + Qt.Key_C)
        self.paste_mask_action.setShortcut(Qt.CTRL + Qt.Key_V)
        self.clear_mask_action.setShortcut(Qt.CTRL + Qt.Key_R)
        self.close_tab_action.setShortcut(Qt.CTRL + Qt.Key_W)
        self.next_file_action.setShortcut(Qt.CTRL + Qt.SHIFT + Qt.Key_Down)
        self.previous_file_action.setShortcut(Qt.CTRL + Qt.SHIFT + Qt.Key_Up)
        self.undo_action.setEnabled(False)
        self.redo_action.setEnabled(False)
        self.menuFile.addAction(self.save_action)
        self.menuEdit.addAction(self.close_tab_action)
        self.menuEdit.addAction(self.undo_action)
        self.menuEdit.addAction(self.redo_action)
        self.menuEdit.addAction(self.copy_mask_action)
        self.menuEdit.addAction(self.paste_mask_action)
        self.menuEdit.addAction(self.clear_mask_action)
        self.menuEdit.addAction(self.swap_action)
        self.menuEdit.addAction(self.next_file_action)
        self.menuEdit.addAction(self.previous_file_action)
        self.tabWidget.clear()   
        QtCore.QObject.connect(self.swap_action, QtCore.SIGNAL(triggered()), self.swapView)
        QtCore.QObject.connect(self.actionOpen_config_file, SIGNAL(triggered())                       , self.loadConfigFile())
        QtCore.QObject.connect(self.actionSave_config_file, SIGNAL(triggered())                       , self.saveConfigFile())
        QtCore.QObject.connect(self.close_tab_action      , SIGNAL(triggered())                       , self.closeCurrentTab())
        QtCore.QObject.connect(self.copy_mask_action      , SIGNAL(triggered())                       , self.copyMask())
        QtCore.QObject.connect(self.paste_mask_action     , SIGNAL(triggered())                       , self.pasteMask())
        QtCore.QObject.connect(self.clear_mask_action     , SIGNAL(triggered())                       , self.clearMask())
        QtCore.QObject.connect(self.next_file_action      , SIGNAL(triggered())                       , self.nextFile())
        QtCore.QObject.connect(self.previous_file_action  , SIGNAL(triggered())                       , self.previousFile())
        QtCore.QObject.connect(self.tabWidget             , SIGNAL(tabCloseRequested(int))            , self.closeTab(int))
        QtCore.QObject.connect(self.tabWidget             , SIGNAL(currentChanged(int))               , self.updateConnect(int))
        QtCore.QObject.connect(self.tree_widget_img       , SIGNAL(itemClicked(QTreeWidgetItem ,int)), self.treeWidgetClicked())
if __name__ == "__main__":
    tap = QtWidgets.QApplication(sys.argv)
    newWin = main_window()
    newWin.show()
    tap.exec_()
    