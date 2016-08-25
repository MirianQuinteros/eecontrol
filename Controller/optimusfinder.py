#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import pyaudio
import wave
from PyDAQmx import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui
from time import sleep
import math, numpy, threading
from model import signalproducer, dralert

class OptimusFinder():
	
	def __init__(self, fromfq, tofq, step, volts):
		self.fromfq = fromfq
		self.tofq = tofq
		self.volts = volts
		self.step = step
		self.allresults = []
		self.maxval = 0
		self.theFreq = -1
		self.rsOK = False

	def genTestSignal(self, freq):
		
		p = pyaudio.PyAudio()
		generator = signalproducer.SignalProducer(1)
		chunk = generator.produceChunk(freq, 3, 100)
		stream = p.open(format=pyaudio.paFloat32,channels=1, rate=44100, output=1)
		
		stream.write(chunk.astype(numpy.float32).tostring())
		
		stream.close()
		p.terminate()
		
	def readSignal(self, freq, voltm):
		try:
			analog_input = Task()
			read = int32()
			data = numpy.zeros((1000,), dtype=numpy.float64)
			analog_input.CreateAIVoltageChan("Dev1/ai0","",DAQmx_Val_Cfg_Default,-10.0,10.0,DAQmx_Val_Volts,None)
			analog_input.CfgSampClkTiming("",10000.0,DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,1000)
			analog_input.StartTask()
			analog_input.ReadAnalogF64(1000,5.0,DAQmx_Val_GroupByChannel,data,1000,byref(read),None)

			mm = max(data)

			voltm.setText('Voltaje actual: ' + str(mm))
			QApplication.processEvents()

			if mm > self.maxval:
				self.theFreq = freq
				self.maxval = mm
				print(mm)
			self.rsOK = True
		except:
			print('rror con device')
			self.rsOK = False

	def find(self, voltm, freqm):

		for s in range(self.fromfq, self.tofq, self.step):
			
			freqm.setText('Frecuencia actual ' + str(s))
			QApplication.processEvents()

			thGenSignal = threading.Thread(target=self.genTestSignal, args=(s,))
			thGenSignal.start()

			thReadResult = threading.Thread(target=self.readSignal, args=(s,voltm,))
			thReadResult.start()

			thGenSignal.join()
			thReadResult.join()
			if self.rsOK == False:
				msg = dralert.DataReaderAlert()
				msg.exec_()
				break
			sleep(3)
		voltm.setText('Max voltaje encontrado ' + str(self.maxval))
		freqm.setText('Frecuencia correspondiente ' + str(self.theFreq))
		QApplication.processEvents()

			