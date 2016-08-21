#!/usr/bin/python

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui

class SignalTypeDelegate(QtGui.QItemDelegate):
    
    def createEditor(self, parent, option, index):
        if index.isValid():
            comboBox = QtGui.QComboBox(parent)
            comboBox.addItem("Seno")
            comboBox.addItem("Coseno")        
        comboBox.activated.connect(self.emitCommitData)
        return comboBox
  
    def setEditorData(self, editor, index):
        comboBox = editor
        if not comboBox:
            return
        pos = comboBox.findText(index.model().data(index, QtCore.Qt.EditRole),
                QtCore.Qt.MatchExactly)
        comboBox.setCurrentIndex(pos)
  
    def setModelData(self, editor, model, index):
        comboBox = editor
        if not comboBox:
            return
  
        model.setData(index, comboBox.currentText())
  
    def emitCommitData(self):
        self.commitData.emit(self.sender())