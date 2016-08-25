#!/usr/bin/python

from PyDAQmx import *
import sys
from time import sleep
import numpy, time, threading
from model import dralert
import matplotlib.pyplot as plt
from Controller import callbackdatareader
from Exceptions import MaxVoltageException

class DataReader():

	def __init__(self, exp, securityFlag):
		self.exp = exp
		self.securityFlag = securityFlag
		self.faltante = None

	def execute(self, start):
		try:
			filename = self.getFileName()
			task = callbackdatareader.CallbackTask(self.exp.fehd, self.securityFlag,
													filename)
			task.StartTask()
			self.runTimer(start, task)
		except Exception as errr:
			print('error con el dispositivov ' + str(errr) )
			raise
		return self.end(task, filename)

	def end(self, task, filename):
		if self.faltante == -1:
			raise MaxVoltageException("er")
		else:
			return self.faltante

	def runTimer(self, secs, task):

		th = threading.Thread(target=self.timer, args=(secs,task,))
		th.start()
		th.join()

	def timer(self, secs, task):
		i = 0
		voltStatusOk = True
		self.timerRun = True

		while ((i < secs) & voltStatusOk & self.timerRun):
			i+=1
			voltStatusOk = task.getStatus()
			sleep(1)

		task.StopTask()
		task.ClearTask()
		
		if voltStatusOk == False:
			self.faltante = -1 #Hubo un error
		elif self.timerRun == False: #frenado manual
			self.faltante = secs - i
		else:
			self.faltante = 0

	def pause(self):
		print('Data reader paused')
		self.timerRun = False

	def stop(self):
		print('Data reader stopped')
		self.timerRun = False

	def getFileName(self):
		tt = time.strftime("%d-%m-%y-%H-%M-%S")
		filename = 'reports\\' + tt+"-Exp-"+str(self.exp.id)+"-"+str(self.exp.fehd)+"-"+str(self.exp.dc)
		
		return filename	+ '.csv'
			