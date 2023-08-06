# -*- coding: utf-8 -*-
#cython: language_level=2
from __future__ import unicode_literals

import os
import errno
import traceback
from songfinder import messages as tkMessageBox
from songfinder import messages as tkFileDialog # pylint: disable=reimported

import songfinder
from songfinder import versionning as version
from songfinder import exception
from songfinder import classSettings as settings

class Paths(object):
	def __init__(self, fenetre=None):
		self.fenetre = fenetre
		self.update(showGui=False)

	def save(self, chemin): # TODO do it better
		if chemin != '':
			try:
				f = open(chemin + 'test.test',"w")
				f.close()
				os.remove(chemin + 'test.test')
			except (OSError, IOError) as error:
				if error.errno == errno.EACCES:
					tkMessageBox.showerror('Erreur', 'Le chemin "%s" n\'est pas '
											'accesible en écriture, '
											'choisissez un autre répertoire.'\
											%chemin, parent = self.fenetre)
					self.save( tkFileDialog.askdirectory(parent = self.fenetre) )
					return 1
				else:
					raise
			if os.path.isdir(chemin):
				settings.GENSETTINGS.set('Paths', 'data', chemin)
				self.root = chemin
				self.update()
			else:
				tkMessageBox.showerror('Erreur', 'Le chemin "%s" n\'existe pas.'\
										%chemin, parent = self.fenetre)
			return 0
		return 1

	def update(self, showGui=True):
		self.root = settings.GENSETTINGS.get('Paths', 'data')
		if showGui and self.root == '' and not songfinder.__unittest__:
			tkMessageBox.showinfo('Répertoire', 'Aucun répertoire pour les chants et '
									'les listes n\'est configuré.\n'
									'Dans le fenêtre suivante, selectionnez '
									'un répertoire existant ou créez en un nouveau. '
									'Par exemple, vous pouvez créer un répertoire "songfinderdata" '
									'parmis vos documents. '
									'Dans ce répertoire seront stocké : '
									'les chants, les listes, les bibles et les partitions pdf.', \
									parent = self.fenetre)
			path = tkFileDialog.askdirectory( initialdir = os.path.expanduser("~"), \
												parent = self.fenetre )
			if path:
				chemin = path
				try:
					os.makedirs(chemin)
				except (OSError, IOError) as error:
					if error.errno == errno.EEXIST:
						pass
					elif error.errno == errno.EACCES:
						tkMessageBox.showerror('Erreur', 'Le chemin "%s" n\'est '
												'pas accesible en ecriture, '
												'choisissez un autre répertoire.'\
												%chemin, parent = self.fenetre)
						self.save( tkFileDialog.askdirectory(parent = self.fenetre) )
						return 1
					else:
						raise
				self.save(chemin)
			else:
				raise Exception('No data directory configured, shuting down SongFinder.')

		self.songs = os.path.join(self.root, 'songs')
		self.sets = os.path.join(self.root, 'sets')
		self.bibles = os.path.join(self.root, 'bibles')
		self.pdf = os.path.join(self.root, 'pdf')
		self.preach = os.path.join(self.root, 'preach')
		self.listPaths = [self.songs, self.sets, self.bibles, self.pdf, self.preach]

		if self.root:
			for path in self.listPaths:
				try:
					os.makedirs(path)
				except (OSError, IOError) as error:
					if error.errno == errno.EEXIST:
						pass
					else:
						raise
		return 0

	def sync(self, screens=None, updateData=None):
		scm = settings.GENSETTINGS.get('Parameters', 'scm')
		if settings.GENSETTINGS.get('Parameters', 'sync') == 'oui' \
			and not os.path.isdir(os.path.join(self.root, '.%s'%scm)):
			if tkMessageBox.askyesno('Sauvegarde', 'Voulez-vous définir le dépot distant ?\n'
										'Ceci supprimera tout documents présent dans "%s"'\
										%self.root):
				try:
					version.AddRepo(self, scm, screens, updateData)
				except exception.CommandLineError:
					tkMessageBox.showerror('Erreur', traceback.format_exc())
			else:
				settings.GENSETTINGS.set('Parameters', 'sync', 'non')


PATHS = Paths()
