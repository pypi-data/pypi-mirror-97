# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import division

try:
	import tkinter as tk
except ImportError:
	import Tkinter as tk
import os
import time
import logging

import songfinder
from songfinder import messages as tkMessageBox
from songfinder import fonctions as fonc
from songfinder import inputFrame

class SearchGui(object):
	def __init__(self, frame, searcher=None, dataBase=None, screens=None, \
				addElementToSelection=None, printer=None, diapoList=None):

		self._frame = frame
		self._printer = printer
		self._songFound = []
		self._searcher = searcher
		# database is only needed to delete elements
		self._dataBase = dataBase
		self._diapoList = diapoList

		self._addElementToSelection = addElementToSelection

		self._priorityMultiplicator = 1

		if screens and screens[0].width > 2000:
			width=46
		else:
			width=30

		self._inputSearch = inputFrame.entryField(frame, width=width, text="Recherche: ")
		explainLabel = tk.Label(frame, text="Chants trouvés: \n"
								"Utilisez leur numéro dans la liste pour les selectionner")
		self._searchResults = tk.Listbox(frame, width=width, height=9)

		self._upButton = tk.Button(frame, \
								text='Ajouter chant', \
								command=lambda event=None, mouseClic=1: \
										self._select(event, mouseClic))

		self._inputSearch.pack(side=tk.TOP, fill=tk.X, expand=1)

		explainLabel.pack(side=tk.TOP, fill=tk.X)
		self._searchResults.pack(side=tk.TOP, fill=tk.X, expand=1)
		self._upButton.pack(side=tk.TOP, fill=tk.X, expand=1)
		self._searchResults.bind("<ButtonRelease-1>", self._printerWrapper)
		self._searchResults.bind("<Double-Button-1>", lambda event, mouseClic=1: \
												self._select(event, mouseClic))

		self._searchResults.bind("<KeyRelease-Up>", self._printerWrapper)
		self._searchResults.bind("<KeyRelease-Down>", self._printerWrapper)
		self._searchResults.bind("<Delete>", self._deleteSong)

		self._inputSearch.bind("<Key>", self._search)
		self._inputSearch.bind("<KeyRelease-BackSpace>", self._nothing)
		self._inputSearch.bind("<KeyRelease-Left>", self._nothing)
		self._inputSearch.bind("<KeyRelease-Right>", self._nothing)
		self._inputSearch.bind("<KeyRelease-Up>", self._nothing)
		self._inputSearch.bind("<KeyRelease-Down>", self._nothing)

		self._inputSearch.focus_set()

		self._delayId = None
		self._passed = 0
		self._total = 0

	def _printerWrapper(self, event=None):
		outDictElements = {}
		if self._searchResults.curselection() and self._songFound:
			select = self._searchResults.curselection()[0]
			toAdd = self._songFound[select]
			outDictElements[toAdd] = 18*self._priorityMultiplicator
		if self._searchResults.size() > 0 and self._songFound: # ValueError None
			toAdd = self._songFound[0]
			outDictElements[toAdd] = 6*self._priorityMultiplicator

		if self._printer:
			time.sleep(0.1) # TTODO, this is a hack for linux/mac, it enable double clic binding
			self._printer(event=event, toPrintDict=outDictElements, loadDiapo=True)
		elif self._diapoList is not None and hasattr(self._diapoList, 'load'):
			self._diapoList.load([toAdd])
			self._diapoList.diapoNumber = 1

	def _search(self, event):
		#~ self.timer.cancel()
		#~ self.timer = threading.Timer(0.1, self._searchCore, [event])
		#~ self.timer.start()
		self._priorityMultiplicator = 10
		self._total += 1
		if self._delayId:
			self._frame.after_cancel(self._delayId)
		self._delayId = self._frame.after(100, self._searchCore, event)
		# ~ print 'search', (self._total-self._passed)/self._total
		self._priorityMultiplicator = 1

	def _searchCore(self, event):
		self._passed += 1
		if self._searcher:
			if self._inputSearch.get(): # pylint: disable=no-member
				searchInput = fonc.safeUnicode(self._inputSearch.get()) # pylint: disable=no-member
				self._songFound = self._searcher.search(searchInput)
				self._showResults()
			self._select(event)
			self._printerWrapper(event)
		else:
			logging.warning("No searcher have been defined for searchGui")

	def _showResults(self):
		self._searchResults.delete(0,'end')
		for i,song in enumerate(self._songFound):
			self._searchResults.insert(i, ('%d -- %s'%(i+1, song)))

	def _select(self, event, mouseClic=0):
		if self._addElementToSelection:
			keyboardInput = ''
			numbers = [str(i) for i in range(1,10)]
			if event:
				# For ubuntu num lock wierd behaviour
				toucheNumPad = event.keycode
				if songfinder.__myOs__ in ['ubuntu', 'darwin']:
					listNumPad = [87, 88, 89, 83, 84, 85, 79, 80, 81]
				else:
					listNumPad = []
				if not self._inputSearch.get().isdigit(): # pylint: disable=no-member
					if toucheNumPad in listNumPad:
						keyboardInput = str(listNumPad.index(toucheNumPad) + 1)
					else:
						keyboardInput = event.keysym
			if mouseClic == 1:
				if self._searchResults.curselection():
					keyboardInput = str(int(self._searchResults.curselection()[0])+1)
					if (keyboardInput not in numbers) \
							or (int(keyboardInput) >= self._searchResults.size()+ 1):
						logging.warning('The input element number "%s" is invalid, '
									'can not figure out what element to add.'
									'Valid entry are "%s", maximum entry is "%s"'\
									%(keyboardInput, ', '.join(numbers), self._searchResults.size()+ 1))
				else:
					logging.warning('The result list was not selected, '
								'can not figure out what element to add.')

			if keyboardInput in numbers:
				if int(keyboardInput) < self._searchResults.size()+ 1:
					element = self._songFound[int(keyboardInput)-1]
					self._addElementToSelection(element)
				self._inputSearch.delete(0, tk.END) # pylint: disable=no-member
				self._inputSearch.focus_set()
			elif keyboardInput.isdigit():
				logging.warning('Got an invalid number from event "%s", '
							'can not figure out what element to add.'%keyboardInput)

	def _deleteSong(self, event): # pylint: disable=unused-argument
		if self._dataBase and self._searchResults.curselection():
			select = self._searchResults.curselection()[0]
			toDelete = self._songFound[select]
			if tkMessageBox.askyesno('Confirmation', \
						'Etes-vous sur de supprimer '
						'le chant:\n"%s" ?'%toDelete.nom):
				path = toDelete.chemin
				if os.path.isfile(path):
					os.remove(path)
				self._dataBase.remove(toDelete)
				try:
					self._searcher.resetCache()
				except AttributeError:
					pass
				if toDelete in self._songFound:
					self._songFound.remove(toDelete)
				self._showResults()
				self._printerWrapper()

	def _nothing(self,event=0):
		pass

	def setSong(self, song):
		self._songFound = [song]
		self._showResults()

	def resetCache(self):
		try:
			self._searcher.resetCache()
		except AttributeError:
			pass

	def resetText(self):
		for song in self._songFound:
			song.reset()

	def resetDiapos(self):
		for element in self._songFound:
			element.resetDiapos()

	def bindAddElementToSelection(self, function):
		self._addElementToSelection = function

	def bindPrinter(self, function):
		self._printer = function

	def useDataBase(self, dataBase):
		self._dataBase = dataBase

	def useSearcher(self, searcher):
		self._searcher = searcher
