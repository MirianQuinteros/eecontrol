#!/usr/bin/python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from time import sleep
import threading, logging
from PyDAQmx import *
from Controller import ExperienceController, datareader, timecounter

class ExperienceExecutor():

  def __init__(self, experiences, status, volts, smoke, waiting,
               counter, maxvolt, expId, readvlbl, read_enabled):
    self.items = experiences
    self.status = status
    self.volts = volts
    self.smoke = smoke
    self.waiting = waiting
    self.counter = counter
    self.maxvolt = maxvolt
    self.expIdLabel = expId
    self.readvlbl = readvlbl
    self.read_enabled = read_enabled
    self.running = False
    self.itemRunning = None
    self.lastItem = 999999
    self.experienceCont = None
    self.counterObj = None
    self.error = False

  def startExecution(self):
    self.executeFrom(0)

  def restartExecution(self):
    maxx = len(self.items)
    i = self.lastItem
    
    if (self.lastItem < maxx)  & (self.running == False):
      self.restart()
      i = i + 1
      sleep(self.waiting.value())

    self.executeFrom(i)

  def executeFrom(self, start):
    self.error = False
    self.running = True
    maxx = len(self.items)
    i = start

    while ( (i < maxx) & self.running ):
      self.lastItem = i
      self.itemRunning = self.items[i]
      self.expIdLabel.setText(str(self.itemRunning.id))
      try:
        self.smokeAction(self.itemRunning)
        self.cameraAction(self.itemRunning)
        self.signalAction(self.itemRunning)
        sleep(self.waiting.value())
        i = i + 1
      except:
        print('error con la placa')
        break
        
    if self.running & (i >= maxx):
      self.lastItem = 999999
      self.running = False
      self.itemRunning = None

  def smokeAction(self, exp):
    if (exp.smoke) :
      self.volts.setText('0 KHz')
      self.status.setText('Comenzando inyeccion \n de humo')
      QApplication.processEvents()
      self.genFunction(self.smoke.value())

  def cameraAction(self, exp):
    if (exp.camera) :
      self.volts.setText('0 KHz')
      self.status.setText('Iniciando camara')
      QApplication.processEvents()
      self.genFunction()

  def genFunction(self, time=3):
    try:
      value = 1.3
      task = Task()
      task.CreateAOVoltageChan("Dev1/ao0","",0,5.0,DAQmx_Val_Volts,None)
      task.StartTask()
      task.WriteAnalogScalarF64(1,5.0,value,None)
      task.StopTask()
      sleep(time)
    except Exception as ade:
      print('Error n la generacion de func' + str(ade))
      self.error = True
      raise Exception('Error con la placa NI DAQ')


  def signalAction(self, exp):

    tSignal = threading.Thread(target=self.generateSignal, args=(exp,))
    tSignal.start()

    if self.read_enabled:
        tReadData = threading.Thread(target=self.readDataNIDAQ, args=(exp,exp.duration,))
        tReadData.start()

    tTimer = threading.Thread(target=self._countdown, args=(exp.duration,))
    tTimer.start()

    tTimer.join()
    tSignal.join()
    if self.read_enabled:
        tReadData.join()

  def generateSignal(self, exp):
    self.volts.setText(str(exp.fehd) + ' KHz')
    self.status.setText('Ejecutando señal')
    QApplication.processEvents()
    self.experienceCont = ExperienceController(exp)
    self.experienceCont.start()

  def regenerateSignal(self, exp):
    self.volts.setText(str(exp.fehd) + ' KHz')
    self.status.setText('Ejecutando señal')
    QApplication.processEvents()
    self.experienceCont.restart()

  def readDataNIDAQ(self, exp, time):
    try:
      self.dataReader = datareader.DataReader(exp, self.maxvolt, self.readvlbl)
      self.drleft = self.dataReader.execute(time)
      if self.drleft == 0:
        print('lectura ok')
      elif self.drleft > 0:
        print('hay que volver a ejecutar porque se detuvo')
      else:
        print('Ocurrio otro error')
    except Exception as ade:
      print('Ocurrió una excepcion ' + str(ade) )
      self.killSignalGen()

  def _countdown(self, start):
    self.counterObj = timecounter.TimeCounter(self.counter)
    self.leftDurationCounter = self.counterObj.execute(start)

  def pauseExecution(self):
    print('pause executor')
    self.experienceCont.pause()
    if self.read_enabled:
      self.dataReader.pause()
    self.counterObj.pause()
    self.running = False

  def stopExecution(self):
    print('stop executor')
    self.experienceCont.stop()
    if self.read_enabled:
      self.dataReader.stop()
    self.counterObj.stop()
    self.running = False

  def killSignalGen(self):
    sleep(1)
    if self.experienceCont is not None:
      self.experienceCont.stop()
    if self.counterObj is not None:
      self.counterObj.stop()
    self.running = False
    self.error = True

  def restart(self):
    print('restart executor')
    exp = self.itemRunning

    tSignal = threading.Thread(target=self.regenerateSignal, args=(exp,))
    tSignal.start()

    if self.read_enabled:
        tReadData = threading.Thread(target=self.readDataNIDAQ, args=(exp,self.drleft))
        tReadData.start()

    tTimer = threading.Thread(target=self._countdown, args=(self.leftDurationCounter,))
    tTimer.start()

    tTimer.join()
    tSignal.join()

    if self.read_enabled:
        tReadData.join()