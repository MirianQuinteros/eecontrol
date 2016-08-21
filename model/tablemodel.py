#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QTimer
import math, numpy
from model import Experience

class MyTableModel(QAbstractTableModel):

    def __init__(self, parent, rows, columns, headerdata):
        super().__init__(parent)
        self.rows = rows
        self.columns = columns
        self.headerData = headerdata
        self.added=0

    def getRows(self):
        return self.rows

    def columnCount(self, index):
        return len(self.columns)

    def rowCount(self, index):
        return len(self.rows)

    def data(self, index, role):
        if index.isValid():
            if (role == QtCore.Qt.DisplayRole) or (role == QtCore.Qt.EditRole):
                attr_name = self.columns[index.column()]
                row = self.rows[index.row()]
                return getattr(row, attr_name)

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled
        elif index.column() == 0:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if index.column() == 0:
            return False
        if index.column() == 2:
            if float(value) > 1:
                return False
        if index.isValid() and role == QtCore.Qt.EditRole:
            attr_name = self.columns[index.column()]
            row = self.rows[index.row()]
            setattr(row, attr_name, value)
            return True

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headerData[col]
        return None

    def insertRows(self, row, rowss=1, index=QModelIndex()):
        self.beginInsertRows(QModelIndex(), row, row + rowss - 1)
        for r in range(rowss):
            rc = len(self.rows)
            if rc == 0:
              lastId = 0
            else:
              lastRow = self.rows[rc - 1]
              lastId = lastRow.id
            self.rows.insert(row+r, Experience(id=lastId+1))
            self.added+=1
        self.endInsertRows()
        return True

    def removeRows(self, row, rowss=1, index=QModelIndex()):
        self.beginRemoveRows(QModelIndex(), row, row + rowss - 1)
        if row == (len(self.rows) - 1):
          self.rows = self.rows[:row]
        else:
          self.rows = self.rows[:row] + self.rows[row + rowss:]
        self.endRemoveRows()
        return True
