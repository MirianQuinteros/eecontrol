#!/usr/bin/python

import sys
import matplotlib.pyplot as plt
from PyQt4 import QtGui
import numpy as np

class Example(QtGui.QMainWindow):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):
        self.statusBar()

        openFile = QtGui.QAction(QtGui.QIcon('open.png'), 'Graficar CSV', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Acciones')
        fileMenu.addAction(openFile)
        
        self.setGeometry(300, 200, 250, 100)
        self.setWindowTitle('Plot CSV')
        self.show()
        
    def showDialog(self):

        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', 'C:\\', 'CSV (*.csv)')
        f = open(fname, 'r')
        
        with f:
            x = np.loadtxt( f , delimiter=',', unpack=True)
            t = list(range(len(x)))
            result = [i * 1/40000 for i in t]
            plt.plot(result, x, label='Gráfico de los datos leidos')
            plt.xlabel('x')
            plt.title('Voltaje leido')
            plt.legend()
            plt.show()
                                
        
def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
