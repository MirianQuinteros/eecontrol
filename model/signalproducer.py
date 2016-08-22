#!/usr/bin/python

import pyaudio
import wave
import sys
from time import sleep
import math, numpy, threading
import matplotlib.pyplot as plt

class SignalProducer():

	def __init__(self, vol, sigType):
		self.volume = vol
		self.sigType = sigType

	def produceChunk(self, freq, length, dc, n=1):

		rate=44100
		chunk = []

		if self.sigType == 'Seno':
			chunk = self.sine(freq, length, rate) * self.volume
		elif self.sigType == 'Coseno':
			chunk = self.cos(freq, length, rate) * self.volume
		else:
			print('error in typesignal')
			return None

		total = len(chunk)
		highLevel = int(round(total * (100 - dc) / 100))
		chunk[total - highLevel :] = chunk[total - highLevel:] * 0
		chunks = []

		for i in range(n):
			chunks = numpy.append(chunks, chunk)
		return chunks

	def sine(self, frequency, length, rate):
		length = int(length * rate)
		factor = float(frequency) * (math.pi * 2) / rate
		sineresult = numpy.sin(numpy.arange(length) * factor)
		return sineresult

	def cos(self, frequency, length, rate):
		length = int(length * rate)
		factor = float(frequency) * (math.pi * 2) / rate
		cosresult = numpy.cos(numpy.arange(length) * factor)
		return cosresult

	def plotSignal(self, chunk):
		plt.close('all')
		plt.ylabel('some numbers')
		plt.plot(chunk)
		plt.show()

