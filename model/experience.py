#!/usr/bin/python
# -*- coding: utf-8 -*-
import pyaudio
import wave
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui, uic
import math, numpy, threading, json
from . import signalproducer

class Experience():

  def __init__(self, id=1, jsonObj=None):
    if jsonObj is None :
        self.id = id
        self.descr = "Set description..."
        self.voltage = 1.0
        self.fehd = 4.0
        self.fforz = 10
        self.dc = 50
        self.duration = 30
        self.camera = False
        self.smoke = False
    else :
        print(jsonObj)
        self.__dict__ = json.loads(jsonObj)

  def ejecutar(self, duration):
    self.stop = False

    print ("Ejecutando..." + str(self.id))

    p = pyaudio.PyAudio()
    volume = self.voltage
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1, rate=44100, output=1)

    producer = signalproducer.SignalProducer(volume)

    durationLeft = self.play_tone(stream, producer, length=duration)
    
    stream.close()
    p.terminate()
    return durationLeft

  def detener(self):
    self.stop = True

  def play_tone(self, stream, producer, length=1):
    
    period = 1/self.fforz
    freq = self.fehd * 1000 # to KHz
    chunk = producer.produceChunk(freq, period , self.dc, 10)
    
    if chunk is None:
        print('ERROR producing chunk')
        return length
    
    x = 0
    while (x <= length) & (self.stop == False):
        x+=(period*10)
        stream.write(chunk.astype(numpy.float32).tostring())

    if x < length:
        durationLeft = length - x
    else:
        durationLeft = -1
    return durationLeft