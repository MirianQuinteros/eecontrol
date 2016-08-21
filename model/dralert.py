#!/usr/bin/python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

class DataReaderAlert(QMessageBox):

	def __init__(self):
		super().__init__()
		self.setIcon(QMessageBox.Warning)
		self.setText("Ocurrió un error con la lectura de datos")
		self.setInformativeText("Verifique que la placa se encuentra conectada y sea reconocida por el sistema")
		self.setWindowTitle("Alerta de dispositivo")
		self.setStandardButtons(QMessageBox.Ok)