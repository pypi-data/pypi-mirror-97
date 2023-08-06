# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import division

try:
	import tkinter as tk
except ImportError:
	import Tkinter as tk
import math

from songfinder import screen
from songfinder import themes
from songfinder import simpleProgress
from songfinder import classSettings as settings


class Presentation(object):
	def __init__(self, frame, diapoList, screens=None, closeCallback=None):
		self._closeCallback = closeCallback
		self._frame = frame
		self._diapoList = diapoList
		self._themePres = None

		if not screens:
			self._screens = screen.Screens()
		else:
			self._screens = screens

		# Fenetre de presentation
		self._presentationWindow = tk.Toplevel(frame)
		self.hide()
		self._presentationWindow.title("Presentation")
		self._presentationWindow.protocol("WM_DELETE_WINDOW", self.hide)

		frame.bind_all("<Escape>", self.hide)
		self._presentationWindow.bind("<Button-1>", self._nextSlide)
		self._presentationWindow.bind("<Button-3>", self._previousSlide)

		self._delayId = None
		self._passed = 0
		self._total = 0

	def isHided(self):
		return self._isHided

	def hide(self, event=None): # pylint: disable=unused-argument
		self._presentationWindow.withdraw()
		self._isHided = True
		if self._closeCallback:
			self._closeCallback()

	def show(self):
		inputRatio = screen.getRatio(settings.GENSETTINGS.get('Parameters', 'ratio'), \
										self._screens[-1].ratio)
		self._screens.fullScreen(self._presentationWindow)
		if inputRatio != 0:
			self._width = math.floor(min(inputRatio*self._screens[-1].height, \
									self._screens[-1].width))
			self._height = math.floor(min(self._screens[-1].width//inputRatio, \
									self._screens[-1].height))
		else:
			self._width = self._screens[-1].width
			self._height = self._screens[-1].height
		self._createTheme()
		self._prefetch()
		self.printer()
		self._presentationWindow.deiconify()
		self._isHided = False

	def _prefetch(self):
		progressBar = simpleProgress.SimpleProgress("Création du cache des images", \
													screens=self._screens)
		progressBar.start(len(self._diapoList))
		self._diapoList.prefetch([self._themePres], progressBar.update)
		progressBar.stop()

	def _previousSlide(self, event=None): # pylint: disable=unused-argument
		self._diapoList.decremente()

	def _nextSlide(self, event=None): # pylint: disable=unused-argument
		self._diapoList.incremente()

	def _createTheme(self):
		if self._themePres:
			self._themePres.destroy()
		self._themePres = themes.Theme(self._presentationWindow, \
							width=self._width, height=self._height, bg='black')
		self._themePres.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

	def _prefetcher(self):
		if self._diapoList is not None:
			self._diapoList[-1].prefetch([self._themePres])
			for i in reversed(range(2)):
				self._diapoList[i+1].prefetch([self._themePres])

	def printer(self):
		self._total += 1
		if self._delayId:
			self._frame.after_cancel(self._delayId)
		self._delayId = self._frame.after(50, self._printer)
		# ~ print 'present', (self._total-self._passed)/self._total

	def _printer(self):
		self._passed += 1
		if self._themePres:
			diapo = self._diapoList[0]
			if self._themePres.name != diapo.themeName:
				self._createTheme()
			diapo.printDiapo(self._themePres)
			self._prefetcher()

	def bindCloseCallback(self, function):
		self._closeCallback = function
