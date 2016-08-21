#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import constants
import json
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui
from model import Experience, tablemodel
from Utils import ExpEncoder

class ExpFileManager():

	def __init__(self, modelParent):
		self.currentOpenFileName = None
		self.modelParent = modelParent

	def newSet(self):
		if self.currentOpenFileName is not None:
			#preguntar si hay que guardar los anteriores cambios
			self.currentOpenFileName = None
		tmodel = tablemodel.MyTableModel(self.modelParent, [], constants.columnFields, constants.columnHeaders)
		return tmodel	

	def saveSet(self, rows):
		s = json.dumps(rows, cls=ExpEncoder)
		if self.currentOpenFileName is None:
			print('el archivo actual esta en nulo')
			self.currentOpenFileName = QtGui.QFileDialog.getSaveFileName(self.modelParent, 'Guardar', 'C:\\','JSON (*.json)')
		file = open(self.currentOpenFileName,'w')
		file.truncate()
		file.write(s)
		file.close()

	def loadSet(self):
		expList = []
		fname = QtGui.QFileDialog.getOpenFileName(self.modelParent, 'Open file', 'C:\\', 'JSON (*.json)')
		f = open(fname, 'r')
		with f:
			data = f.read()
			s = json.loads(data)
			for exp in s:
				expstr = json.dumps(exp)
				e = Experience(jsonObj=expstr)
				expList.append(e)
			self.currentOpenFileName = fname
			tmodel = tablemodel.MyTableModel(self.modelParent, expList, constants.columnFields, constants.columnHeaders)
			return tmodel

