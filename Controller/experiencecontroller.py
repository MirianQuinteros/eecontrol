#!/usr/bin/python
# -*- coding: utf-8 -*-
import pyaudio
import wave
import sys
import math, numpy, threading

class ExperienceController():

	def __init__(self, exp):
		self.exp = exp
		self.durationLeft = 0

	def ejecutar(self, dur):
		self.durationLeft = self.exp.ejecutar(dur)

	def start(self):
		print('Experience controller start')
		self.thread = threading.Thread(target=self.ejecutar, args=(self.exp.duration,))
		self.thread.start()
		self.thread.join()

	def pause(self):
		print('Experience controller pause')
		self.exp.detener()

	def restart(self):
		print('Experience controller restart')
		if self.durationLeft > 0:
			thread = threading.Thread(target=self.ejecutar, args=(self.durationLeft,))
			thread.start()
			thread.join()

	def stop(self):
		print('Experience controller stop')
		self.exp.detener()
