#!/usr/bin/python

import sys
from time import sleep
import numpy

class TimeCounter():

	def __init__(self, display):
		self.running = True
		self.counter = display

	def execute(self, start):
		self.running = True
		i = start
		while self.running & (i >= 0):
			self.counter.display(i)
			i = i - 1
			sleep(1)
		return i

	def pause(self):
		#print('Counter paused')
		self.running = False

	def stop(self):
		#print('Counter stopped')
		self.running = False


