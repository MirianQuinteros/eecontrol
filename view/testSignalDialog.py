#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui, uic
import math, numpy, threading, pyaudio
from model import SignalProducer

class TestSignalDialog(QDialog):

    def __init__(self, parent = None):
        super(TestSignalDialog, self).__init__(parent)

        layout = QFormLayout(self)

        # nice widget for editing the date
        self.fqehd = QSpinBox()
        self.fqehd.setRange(10,35000)
        self.fqehd.setValue(10000)

        self.fforz = QSpinBox()
        self.fforz.setRange(0,1000)
        self.fforz.setValue(10)

        self.dc = QSpinBox()
        self.dc.setRange(0,100)
        self.dc.setValue(60)

        self.btnHallar = QPushButton('Generar señal')
        self.btnHallar.clicked.connect(self.generateandplot)

        layout.addRow(QLabel('Frec. EHD Hz'), self.fqehd)
        layout.addRow(QLabel('Frec. forzado Hz'), self.fforz)
        layout.addRow(QLabel('Duty Cycle %'), self.dc)
        layout.addRow(self.btnHallar)

        # OK and Cancel buttons
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addRow(self.buttons)

    def generateandplot(self):
        self.buttons.button(QDialogButtonBox.Ok).setEnabled(False)
        
        p = pyaudio.PyAudio()
        period = 1/self.fforz.value()
        stream = p.open(format=pyaudio.paFloat32,
                    channels=1, rate=44100, output=1)
        prod = SignalProducer(1)
        chunk = prod.produceChunk(self.fqehd.value(), period, self.dc.value())
        prod.plotSignal(chunk)
        for x in range(0,50):
            stream.write(chunk.astype(numpy.float32).tostring())
        stream.close()
        p.terminate()
        self.buttons.button(QDialogButtonBox.Ok).setEnabled(True)

    # static method to create the dialog and return (date, time, accepted)
    @staticmethod
    def getff(parent = None):
        dialog = TestSignalDialog(parent)
        result = dialog.exec_()
        return (result == QDialog.Accepted)