#!/usr/bin/python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

class SecurityAlert(QMessageBox):

	def __init__(self):
		super().__init__()
		self.setIcon(QMessageBox.Warning)
		self.setText("Se detiene la lectura de datos y la generación de señal")
		self.setInformativeText("Verifique la configuración de la señal, se detectó un voltaje superior al admitido")
		self.setWindowTitle("Alerta de seguridad")
		self.setStandardButtons(QMessageBox.Ok)