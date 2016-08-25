#!/usr/bin/python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from time import sleep
import threading, logging, math
from PyDAQmx import *
from Controller import ExperienceController, datareader, timecounter
from Exceptions import MaxVoltageException

class ExperienceExecutor():

  def __init__(self, experiences, status, volts, smoke, waiting,
               counter, maxvolt, expId, read_enabled):
    self.items = experiences
    self.status = status
    self.volts = volts
    self.smoke = smoke
    self.waiting = waiting
    self.counter = counter
    self.maxvolt = maxvolt
    self.expIdLabel = expId
    self.read_enabled = read_enabled
    self.running = False
    self.lastItemIndex = None
    self.experienceCont = None
    self.counterObj = None
    self.error = False

  def startExecution(self):
    self.running = True
    i = self.restartExecution()
    self.executeFrom(i)

  def restartExecution(self):

    if self.lastItemIndex is not None:
        i = self.lastItemIndex
        self.signalAction(self.items[i], True)
        i = i + 1
        if self.running:
            sleep(self.waiting.value())
        return i
    else:
        return 0 #desde el principio

  def executeFrom(self, start):
    
    self.error = False
    maxx = len(self.items)
    i = start

    while ( (i < maxx) & self.running ):
      self.lastItemIndex = i
      item = self.items[i]
      self.expIdLabel.setText(str(item.id))
      try:
        self.smokeAction(item)
        self.cameraAction(item)
        self.signalAction(item, False)
        if self.running:
            sleep(self.waiting.value())
        i = i + 1
      except:
        print('error con la placa')
        break
        
    if self.running & (i >= maxx):
      self.lastItemIndex = None
      self.running = False

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
      value = 2
      task = Task()
      task.CreateAOVoltageChan("Dev1/ao0","",0,5.0,DAQmx_Val_Volts,None)
      task.StartTask()
      task.WriteAnalogScalarF64(1,5.0,value,None)
      sleep(time)
      task.WriteAnalogScalarF64(1,5.0,0,None)
      task.StopTask()
    except Exception as ade:
      print('Error n la generacion de func' + str(ade))
      self.error = True
      raise Exception('Error con la placa NI DAQ')

  def signalAction(self, exp, isRestart):

    tSignal = threading.Thread(target=self.generateSignal, args=(exp,isRestart))
    tSignal.start()

    leftTime = exp.duration
    if isRestart:
        leftTime = math.ceil(self.experienceCont.durationLeft)
    
    if self.read_enabled:    
        tReadData = threading.Thread(target=self.readDataNIDAQ, args=(exp,leftTime,))
        tReadData.start()

    tTimer = threading.Thread(target=self._countdown, args=(leftTime,))
    tTimer.start()

    tTimer.join()
    tSignal.join()
    if self.read_enabled:
        tReadData.join()

  def generateSignal(self, exp, isRestart):
    self.volts.setText(str(exp.fehd) + ' KHz')
    self.status.setText('Ejecutando señal')
    QApplication.processEvents()
    if isRestart:
        self.experienceCont.restart()
    else:
        self.experienceCont = ExperienceController(exp)
        self.experienceCont.start()

  def readDataNIDAQ(self, exp, time):
    try:
      self.dataReader = datareader.DataReader(exp, self.maxvolt)
      result = self.dataReader.execute(time)
      if result == 0:
        print('lectura ok')
      elif result > 0:
        print('hay que volver a ejecutar porque se detuvo')
      else:
        print('Ocurrio otro error')
    except MaxVoltageException as eee:
      print('Maximo voltaje alcanzado ' + str(eee))
      self.killSignalGen('ERROR_SEC')
    except Exception as ade:
      print('Ocurrió una excepcion ' + str(ade) )
      self.killSignalGen()

  def _countdown(self, start):
    self.counterObj = timecounter.TimeCounter(self.counter)
    self.counterObj.execute(start)

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
    self.lastItemIndex = None

  def killSignalGen(self, error=''):
    sleep(1)
    if self.experienceCont is not None:
      self.experienceCont.stop()
    if self.counterObj is not None:
      self.counterObj.stop()
    self.running = False
    self.error = error
    self.lastItemIndex = None
