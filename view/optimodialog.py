#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import QTimer
from time import sleep
import math, numpy, threading
import json
import constants
import logging
from Controller import optimusfinder

class OptimoDialog(QDialog):

    def __init__(self, parent = None):
        super(OptimoDialog, self).__init__(parent)

        #layout = QVBoxLayout(self)
        layout = QFormLayout(self)

        # nice widget for editing the date
        self.fromfq = QSpinBox()
        self.fromfq.setRange(10,29999)
        self.fromfq.setValue(100)

        self.tofq = QSpinBox()
        self.tofq.setRange(10,30000)
        self.tofq.setValue(1000)

        self.step = QSpinBox()
        self.step.setRange(1,9999)
        self.step.setValue(200)

        self.btnHallar = QPushButton('Hallar')
        self.btnHallar.clicked.connect(self.findOpt)

        self.max_volt = QLabel('Máximo voltaje: ?')
        self.freq_max = QLabel('Frecuencia: ?')

        layout.addRow(QLabel('Frec. Mín. Hz'), self.fromfq)
        layout.addRow(QLabel('Frec. Máx. Hz'), self.tofq)
        layout.addRow(QLabel('Paso'), self.step)
        layout.addRow(self.btnHallar)
        layout.addRow(self.max_volt)
        layout.addRow(self.freq_max)

        # OK and Cancel buttons
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addRow(self.buttons)

    def findOpt(self):
        self.buttons.button(QDialogButtonBox.Ok).setEnabled(False)
        self.optimusFinder = optimusfinder.OptimusFinder(self.fromfq.value(), self.tofq.value(), self.step.value(), 1)
        self.optimusFinder.find(self.max_volt, self.freq_max)
        self.buttons.button(QDialogButtonBox.Ok).setEnabled(True)

    def getfromfq(self):
        return self.max_volt.text()

    # static method to create the dialog and return (date, time, accepted)
    @staticmethod
    def getff(parent = None):
        dialog = OptimoDialog(parent)
        result = dialog.exec_()
        optimusfq = dialog.getfromfq()
        return (optimusfq, result == QDialog.Accepted)