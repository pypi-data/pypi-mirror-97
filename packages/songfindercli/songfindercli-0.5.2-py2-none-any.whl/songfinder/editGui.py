# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import division

try:
	import tkinter as tk
	import tkinter.ttk as ttk
except ImportError:
	import Tkinter as tk
	import ttk

import errno
from songfinder import messages as tkMessageBox

from songfinder.elements import elements
from songfinder import fonctions as fonc
from songfinder import guiHelper
from songfinder import inputFrame
from songfinder import gestchant
from songfinder import classSettings as settings

class EditGui(object):
	def __init__(self, frame, dataBase=None, screens=None, \
				printerCallback=None, saveCallback=None, \
				newCallback=None, diapoList=None):

		self._dataBase = dataBase
		self._screens = screens
		self._printerCallback = printerCallback
		self._saveCallback = saveCallback
		self._setSong = newCallback
		self._diapoList = diapoList

		buttonSubPanel = ttk.Frame(frame)
		titleSubPanel = ttk.Frame(frame)
		chordsSubPanel = ttk.Frame(frame)
		supinfoSubPanel = ttk.Frame(frame)
		textSubPanel = ttk.Frame(frame)

		buttonSubPanel.pack(side=tk.TOP)
		titleSubPanel.pack(side=tk.TOP, fill=tk.X)
		chordsSubPanel.pack(side=tk.TOP, fill=tk.X)
		supinfoSubPanel.pack(side=tk.TOP, fill=tk.X)
		textSubPanel.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

		self._newSongWindow = None
		self._printedElement = None

		self._inputTitle = inputFrame.TextField(titleSubPanel, width=20, \
								text="Titre :", packing=tk.LEFT, state=tk.DISABLED)
		self._inputAuthor = inputFrame.TextField(titleSubPanel, width=10, \
								text="Auteur :", packing=tk.LEFT, state=tk.DISABLED)
		self._inputKey = inputFrame.TextField(chordsSubPanel, width=5, \
								text='Tonalité: ', packing=tk.LEFT, state=tk.DISABLED)
		self._inputTranspose = inputFrame.TextField(chordsSubPanel, width=3, \
								text='Transposition: ', packing=tk.LEFT, state=tk.DISABLED)
		self._inputCapo = inputFrame.TextField(chordsSubPanel, width=3, \
								text='Capo: ', packing=tk.LEFT, state=tk.DISABLED)
		self._inputNumCCLI = inputFrame.TextField(supinfoSubPanel, width=3, \
								text='Num (CCLI): ', packing=tk.LEFT, state=tk.DISABLED)
		self._inputNumTurf = inputFrame.TextField(supinfoSubPanel, width=3, \
								text='Num (Turf): ', packing=tk.LEFT, state=tk.DISABLED)
		self._inputNumCustom = inputFrame.TextField(supinfoSubPanel, width=3, \
								text='Num (Custom): ', packing=tk.LEFT, state=tk.DISABLED)

		self._buttonSaveSong = tk.Button(buttonSubPanel, text='Sauver', \
							command=self._saveSong, state=tk.DISABLED)
		buttonCreateSong = tk.Button(buttonSubPanel, text='Créer un nouveau chant', \
							command=self._createNewSongWindow)
		self._buttonCreateNewVersion = tk.Button(buttonSubPanel, \
							text='Créer une autre version du chant', \
							command=lambda: self._createNewSongWindow(self._printedElement))

		if screens and screens[0].width > 2000:
			width=56
		else:
			width=48
		if screens and screens[0].height > 2000:
			height=46
		else:
			height=32

		self._songTextField = tk.Text(textSubPanel, width=width, height=height, \
										undo=True, state=tk.DISABLED)
		self._songTextFieldScroller = tk.Scrollbar(textSubPanel, command=self._songTextField.yview)
		self._songTextField['yscrollcommand'] = self._songTextFieldScroller.set

		self._inputTitle.pack(side=tk.LEFT, fill=tk.X, expand=1)
		self._inputAuthor.pack(side=tk.LEFT, fill=tk.X, expand=1)

		self._inputKey.pack(side=tk.LEFT, fill=tk.X, expand=1)
		self._inputTranspose.pack(side=tk.LEFT, fill=tk.X, expand=1)
		self._inputCapo.pack(side=tk.LEFT, fill=tk.X, expand=1)

		self._inputNumCCLI.pack(side=tk.LEFT, fill=tk.X, expand=1)
		self._inputNumTurf.pack(side=tk.LEFT, fill=tk.X, expand=1)
		self._inputNumCustom.pack(side=tk.LEFT, fill=tk.X, expand=1)

		self._buttonSaveSong.pack(side=tk.LEFT)
		buttonCreateSong.pack(side=tk.LEFT)
		self._buttonCreateNewVersion.pack(side=tk.LEFT)

		self._songTextField.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
		self._songTextFieldScroller.pack(side=tk.LEFT, fill=tk.Y)


		self._inputFieldsList = [self._inputTitle, self._inputAuthor, \
						self._inputTranspose, self._inputCapo, self._inputKey, \
						self._inputNumCCLI, self._inputNumTurf, self._inputNumCustom]

		for field in self._inputFieldsList:
			field.bind("<KeyRelease>", self._changeSongState)
		# Edition de la liste de selection
		frame.bind_all("<Control-s>", self._saveSong)
		self._songTextField.bind("<KeyRelease>", self._changeSongState)
		frame.bind_class("Text","<Control-a>", self._selectAllText)


	def _printerOff(self):
		guiHelper.change_text(self._songTextField, '')
		self._songTextField["state"] = tk.DISABLED
		for field in self._inputFieldsList:
			guiHelper.change_text(field, '')
			field.state = tk.DISABLED

	def _printOn(self):
		self._songTextField["state"] = tk.NORMAL
		for field in self._inputFieldsList:
			field.state = tk.NORMAL

	def _updateContent(self, element=None):
		if not element:
			element = self._printedElement
		guiHelper.change_text(self._songTextField, element.text)
		guiHelper.change_text(self._inputTitle, element.title)
		guiHelper.change_text(self._inputAuthor, element.author or '')
		guiHelper.change_text(self._inputTranspose, element.transpose or '')
		guiHelper.change_text(self._inputCapo, element.capo or '')
		guiHelper.change_text(self._inputKey, element.key)
		guiHelper.change_text(self._inputNumCCLI, element.nums.get('hymn') or '')
		guiHelper.change_text(self._inputNumTurf, element.nums.get('turf') or '')
		guiHelper.change_text(self._inputNumCustom, element.nums.get('custom') or '')

	def _saveSong(self, event=None): # pylint: disable=unused-argument
		if self._dataBase and self._printedElement.etype == 'song':
			cursorPosition = self._songTextField.index("insert")
			scrollPosition = self._songTextFieldScroller.get()[0]

			# TODO a retirer
			title = self._printedElement.title
			if title[:3] in ['JEM', 'SUP'] and title[3:6].isdigit():
				self._printedElement.title = title[7:]

			self._printedElement.transpose = self._inputTranspose.get(1.0, tk.END) # pylint: disable=no-member
			self._printedElement.capo = self._inputCapo.get(1.0, tk.END) # pylint: disable=no-member
			self._printedElement.key = self._inputKey.get(1.0, tk.END) # pylint: disable=no-member
			self._printedElement.turfNumber = self._inputNumTurf.get(1.0, tk.END) # pylint: disable=no-member
			self._printedElement.hymnNumber = self._inputNumCCLI.get(1.0, tk.END) # pylint: disable=no-member
			self._printedElement.text = self._songTextField.get(1.0, tk.END) # pylint: disable=no-member
			self._printedElement.title = self._inputTitle.get(1.0, tk.END) # pylint: disable=no-member
			self._printedElement.author = self._inputAuthor.get(1.0, tk.END) # pylint: disable=no-member
			try:
				self._dataBase.save(songs=[self._printedElement])
			except (OSError, IOError) as error:
				if error.errno == errno.ENOENT:
					try:
						tkMessageBox.showerror('Erreur', 'Le chemin du chant "%s" n\'est pas valide. '\
											%self._printedElement.chemin)
					except UnicodeEncodeError:
						tkMessageBox.showerror('Erreur', 'Le chemin du chant "%s" n\'est pas valide. '\
											%repr(self._printedElement.chemin))
					return 1
				else:
					raise

			self._updateContent()
			self._syntaxHighlighting()

			self._songTextField.mark_set("insert", cursorPosition )
			self._songTextField.yview('moveto', scrollPosition)
			self._songTextField.edit_modified(False)

			for field in self._inputFieldsList:
				field.edit_modified(False) # pylint: disable=no-member

			self._buttonSaveSong.config(state=tk.DISABLED)
			if self._saveCallback:
				self._saveCallback()
			return 0
		else:
			return 1

	def _changeSongState(self, event=None): # pylint: disable=unused-argument
		notModified = all([not field.edit_modified() for field in self._inputFieldsList]) # pylint: disable=no-member

		if (self._songTextField.edit_modified() or not notModified ) \
				and self._printedElement \
				and self._printedElement.etype == 'song':
			self._buttonSaveSong.config(state=tk.NORMAL)
			self._syntaxHighlighting()

	def _selectAllText(self, event):
		event.widget.tag_add("sel","1.0","end")

	def _syntaxHighlighting(self):
		guiHelper.coloration(self._songTextField, "black")
		guiHelper.coloration(self._songTextField, "blue", \
							settings.GENSETTINGS.get('Syntax', 'newline'))
		guiHelper.coloration(self._songTextField, "red", '\\ac')
		guiHelper.coloration(self._songTextField, "red", '[', ']')
		guiHelper.coloration(self._songTextField, "red", '\\...')
		guiHelper.coloration(self._songTextField, "red", "(bis)")
		guiHelper.coloration(self._songTextField, "red", "(ter)")
		for newslideSyntax in settings.GENSETTINGS.get('Syntax', 'newslide'):
			guiHelper.coloration(self._songTextField, "blue", newslideSyntax) # TclError None

	def _createNewSongWindow(self, copiedSong=''):
		if self._newSongWindow:
			self._newSongWindow.destroy()
		self._newSongWindow = tk.Toplevel()
		with guiHelper.SmoothWindowCreation(self._newSongWindow, screens=self._screens):
			self._newSongWindow.title("Nouveau chant")
			self.newTitle = inputFrame.TextField(self._newSongWindow, width=40, \
									text='Titre du nouveau chant: ', packing=tk.TOP)
			if copiedSong:
				self.newTitle.insert(1.0, copiedSong.nom) # pylint: disable=no-member
			bouton = tk.Button(self._newSongWindow, text='Créer',\
				command = lambda chant = copiedSong: self._createNewSong(chant))

			self.newTitle.pack(side=tk.TOP, fill=tk.X, expand=1)
			bouton.pack(side=tk.TOP)
			self.newTitle.focus_set()

	def	_createNewSong(self, copiedSong=''):
		if self._dataBase:
			tmp = self.newTitle.get(1.0, tk.END) # pylint: disable=no-member
			tmp = fonc.upper_first(tmp)
			tmp = tmp.replace('\n', '')
			tmp, title = gestchant.newSongTitle(tmp, self._dataBase.maxCustomNumber)
			newSong = elements.Chant(tmp, title)
			newSong.text = '%s'%settings.GENSETTINGS.get('Syntax', 'newslide')[0]

			if newSong not in self._dataBase or \
			(newSong in self._dataBase and\
			tkMessageBox.askyesno('Création', 'Le chant "%s" existe déjà, '
							'voulez-vous l\'écraser ?'%newSong.nom)):
				self._newSongWindow.destroy()
				self._newSongWindow = None
				self._printedElement = newSong
				self._songTextField.focus_set()
				if not copiedSong:
					self._printerOff()
					self._printOn()
					guiHelper.change_text(self._songTextField, \
										"%s\n" \
										%settings.GENSETTINGS.get('Syntax', 'newslide')[0])
					guiHelper.change_text(self._inputTitle, self._printedElement.title)
				if not self._saveSong():
					self._dataBase.add(newSong)

					if self._saveCallback:
						self._saveCallback()
					if self._setSong:
						self._setSong(newSong)
					self.printer(toPrintDict={newSong:100})

					tkMessageBox.showinfo('Confirmation', \
							'Le chant "%s" a été créé.'%newSong.nom)

			if self._newSongWindow != None:
				self._newSongWindow.focus_set()
				self.newTitle.insert(1.0, '') # pylint: disable=no-member
			self._activeButtons()

	def _activeButtons(self):
		if self._printedElement:
			self._buttonCreateNewVersion.config(state=tk.NORMAL)
		else:
			self._buttonCreateNewVersion.config(state=tk.DISABLED)

	def printer(self, event=None, toPrintDict=None, loadDiapo=False): # pylint: disable=unused-argument
		if not toPrintDict:
			toPrintDict=dict()
		maxPriority = 0
		toPrint = None
		for element, priority in toPrintDict.items():
			if element and priority > maxPriority:
				toPrint = element
				maxPriority = priority

		if toPrint:
			self._printOn()
			notModified = all([not field.edit_modified() for field in self._inputFieldsList]) # pylint: disable=no-member
			if (self._songTextField.edit_modified() or not notModified) \
						and toPrint.title:
				if tkMessageBox.askyesno('Sauvegarde', \
							'Voulez-vous sauvegarder les modifications '
							'sur le chant:\n"%s" ?'%self._printedElement.title):
					self._saveSong()
			self._printedElement = toPrint
			self._updateContent(element=toPrint)
			self._syntaxHighlighting()
			if loadDiapo and hasattr(self._diapoList, 'load'):
				self._diapoList.load([toPrint])
				self._diapoList.diapoNumber = 1
		else:
			self._printerOff()

		self._songTextField.edit_modified(False)
		for field in self._inputFieldsList:
			field.edit_modified(False) # pylint: disable=no-member
		self._buttonSaveSong.config(state=tk.DISABLED)
		self._songTextField.edit_reset()
		self._activeButtons()
		if self._printerCallback:
			self._printerCallback()

	def resetText(self):
		try:
			self._printedElement.resetText()
		except AttributeError:
			pass

	def printedElement(self):
		return self._printedElement

	def bindPrinterCallback(self, function):
		self._printerCallback = function

	def bindSaveCallback(self, function):
		self._saveCallback = function

	def bindSetSong(self, function):
		self._setSong = function

	def useDataBase(self, dataBase):
		self._dataBase = dataBase
