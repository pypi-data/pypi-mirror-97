# -*- coding: utf-8 -*-
#cython: language_level=2
from __future__ import unicode_literals

import os
import errno
import xml.etree.cElementTree as ET

try: # Windows only imports
	import win32con
	import win32api
except ImportError:
	pass

from songfinder import cache
import songfinder

# This fonction has a duplicate in src.fonctions
def indent(elem, level=0):
	i = "\r\n" + level*"  "
	if elem:
		if not elem.text or not elem.text.strip():
			elem.text = i + "  "
		if not elem.tail or not elem.tail.strip():
			elem.tail = i
		for subElem in elem:
			indent(subElem, level+1)
		if not elem.tail or not elem.tail.strip():
			elem.tail = i
	else:
		if level and (not elem.tail or not elem.tail.strip()):
			elem.tail = i

class Settings(object):
	def __init__(self, settingsPath, cheminRoot, portable):
		self._settings = None
		self._settingsPath = settingsPath
		self._dataPath = cheminRoot
		self._portable = portable
		self._cache = cache.Cache(20, self._get)
		self._name = None

		try:
			os.makedirs(self._settingsPath)
			try:
				win32api.SetFileAttributes(self._settingsPath,win32con.FILE_ATTRIBUTE_HIDDEN)
			except NameError: # For Ubuntu
				pass
		except (OSError, IOError) as error:
			if error.errno == errno.EEXIST:
				pass
			else:
				raise
		self._changeCount = 0
		self._maxChange = 30

		# Dict enable renaming of parameters for a nex release
		self._renameParameters={'Latex_Parameters/key':'Export_Parameters/chords', \
								'Latex_Parameters/reorder':'Export_Parameters/reorder', \
								'Latex_Parameters/one_song_per_page':'Export_Parameters/one_song_per_page', \
								'Latex_Parameters/alphabetic_list':'Export_Parameters/alphabetic_list', \
								'Latex_Parameters/transpose':'Export_Parameters/transpose', \
								'Latex_Parameters/list':'Export_Parameters/list', \
								'Latex_Parameters/sol_chords':'Export_Parameters/sol_chords', \
								'Latex_Parameters/booklet':'Export_Parameters/booklet', \
								'Latex_Parameters/saut_lignes':'Export_Parameters/saut_lignes', \
								'Latex_Parameters/one_chorus':'Export_Parameters/one_chorus', \
								'Latex_Parameters/ignore':'Export_Parameters/ignore', \
								'Latex_Parameters/affiche_liste':'Export_Parameters/affiche_liste', \
								'Latex_Parameters/two_columns':'Export_Parameters/two_columns', \
								'Latex_Parameters/capo':'Export_Parameters/capo', \
								'Latex_Parameters/simple_chords':'Export_Parameters/simple_chords', \
								'Latex_Parameters/keep_first':'Export_Parameters/keep_first', \
								'Latex_Parameters/keep_last':'Export_Parameters/keep_last', \
								'Latex_Parameters/diapo':'Export_Parameters/diapo', \
								}

	def create(self):
		raise NotImplementedError

	def write(self):
		fileName = os.path.join(self._settingsPath, self._name)
		tree = ET.ElementTree(self._settings)
		indent(self._settings)
		tree.write(fileName , encoding="UTF-8")

	def read(self):
		self._cache.reset()
		fileName = os.path.join(self._settingsPath, self._name)
		try:
			tree = ET.parse(fileName)
			old_settings_file = tree.getroot()
		except (OSError, IOError, ET.ParseError):
			old_settings_file = None
		# Copy old file settings in new file
		if old_settings_file is not None:
			for param in old_settings_file:
				for key, value in param.attrib.items():
					for oldName, newName in self._renameParameters.items():
						tag = param.tag
						if tag == oldName.split('/')[0] and key == oldName.split('/')[1]:
							tag = newName.split('/')[0]
							key = newName.split('/')[1]
					try:
						newSetting = self._settings.find(tag).attrib[key]
						if len(newSetting.split(', ')) == len(value.split(', ')) :
							self._settings.find(tag).set(key, value)
					except (AttributeError, KeyError):
						pass

	def get(self, setting, parameter):
		return self._cache.get(setting+parameter, args=[setting, parameter])

	def _get(self, setting, parameter):
		try:
			value = self._settings.find(setting).attrib[parameter]
		except (AttributeError, KeyError):
			logging.warning('Value for parameter "%s/%s" not found'%(setting, parameter))
			self.create()
			self.read()
			self.write()
			value = self._settings.find(setting).attrib[parameter]
		try:
			value = int(value)
		except ValueError:
			try:
				value = float(value)
			except ValueError:
				pass
		try:
			newvalue = value.split(', ')
			newvalue[1] # This line is actualy usefull to test if newvalue if big enough # pylint: disable=pointless-statement
			try:
				newvalue.remove('')
			except ValueError:
				pass
			value = newvalue
		except (AttributeError, IndexError):
			pass

		if (setting.lower() in ['paths', 'path'] \
				or parameter.lower() in ['background', 'backgrounds']) \
				and value != '':
			value = os.path.join( os.path.abspath(value))
			value = value.replace('/', os.sep).replace('\\', os.sep)
		return value

	def set(self, setting, parameter, value):
		self._cache.reset()
		if (setting.lower() in ['paths', 'path'] \
				or parameter.lower() in ['background', 'backgrounds']) \
				and self._portable \
				and value != '':
			value = os.path.relpath(value)
		try:
			self._settings.find(setting).set(parameter, value)
		except AttributeError:
			logging.warning('Not able to set "%s" as value for parameter '
						'"%s/%s" not found'%(value, setting, parameter))
			self.create()
			self.read()
			self.write()
			self._settings.find(setting).set(parameter, value)
		self._changeCount += 1

		if self._changeCount > self._maxChange:
			self.write()

class GenSettings(Settings):
	def __init__(self, settingsPath, cheminRoot, portable):
		Settings.__init__(self, settingsPath, cheminRoot, portable)
		self._name = 'SettingsGen'

	def create(self):
		self._settings = ET.Element(self._name)
		chemins = ET.SubElement(self._settings, "Paths")
		if not self._portable:
			chemins.set("data", '')
		else:
			chemins.set("data", os.path.join(self._dataPath, "songFinderData") )
		chemins.set("shir", '')
		chemins.set("topchretiens", '')
		chemins.set("remote", '')

		extentions = ET.SubElement(self._settings, "Extentions")
		extentions.set("video", ".avi, .mp4, .mov, .mkv, .vob, .mpg, .mpa, "
						".mpg, .webm, .flv, .ogg, .wmv, .amv, .asf, .m4v, "
						".3gp, .nsv, .mka, .mks, .rmvb, .mxf, .mpeg")
		extentions.set("audio", ".mp3, .ogg, .oga, .flac, .wav, .wma, .aif, "
						".alac, .aa, .aax, .aax+, .aac, .m4a, .m4p, .m4b, "
						".mp4, .3gp, .aa3, .oma, .at3, .ape, .vqf, .vql, "
						".vqe, .au, ac3, .amr, .3gpp, .smf")
		extentions.set("image", ".jpg, .png, .gif, .bmp, .tiff, .jpeg")
		extentions.set("presentation", ".ppt, .pptx, .odf, .pdf")
		extentions.set("chant", ".sfs, ")
		extentions.set("liste", ".sfl, ")
		extentions.set("bible", ".sfb, ")
		extentions.set("chordpro", ".crd, .chopro, .pro, .chordpro, .cho")

		parametres = ET.SubElement(self._settings, "Parameters")
		parametres.set("size_of_previews", "2")
		parametres.set("ratio", 'auto')
		parametres.set("ratio_avail", 'auto, 5/4, 4/3, 3/2, 16/10, 16/9, 21/9, 32/9' )
		parametres.set("autoload", 'non')
		parametres.set("sync", 'oui')
		parametres.set("scm", 'git')
		parametres.set("autoreceive", 'non')
		parametres.set("highmemusage", 'non')
		parametres.set("autoexpand", 'non')

		syntax = ET.SubElement(self._settings, "Syntax")
		syntax.set("newslide", "\\ss, \\sc, \\sb, \\si")
		syntax.set("newline", "\\l")
		syntax.set("element_type", 'song, media, image, verse, empty, preach, latex, beamer')

class LatexSettings(Settings):
	def __init__(self, settingsPath, cheminRoot, portable):
		Settings.__init__(self, settingsPath, cheminRoot, portable)
		self._name = 'SettingsLatex'

	def create(self):
		self._settings = ET.Element(self._name)
		latex_parametres = ET.SubElement(self._settings, "Export_Parameters")
		latex_parametres.set("reorder", "oui")
		latex_parametres.set("one_song_per_page", "non")
		latex_parametres.set("alphabetic_list", "oui")
		latex_parametres.set("transpose", "oui")
		latex_parametres.set("chords", "oui")
		latex_parametres.set("list", "non")
		latex_parametres.set("sol_chords", "oui")
		latex_parametres.set("booklet", "non")
		latex_parametres.set("saut_lignes", "oui")
		latex_parametres.set("one_chorus", "oui")
		latex_parametres.set("ignore", "oui")
		latex_parametres.set("affiche_liste", "oui")
		latex_parametres.set("two_columns", "oui")
		latex_parametres.set("capo", "non")
		latex_parametres.set("simple_chords", "non")
		latex_parametres.set("keep_first", "non")
		latex_parametres.set("keep_last", "non")
		latex_parametres.set("diapo", "non")

class PresSettings(Settings):
	def __init__(self, settingsPath, cheminRoot, portable):
		Settings.__init__(self, settingsPath, cheminRoot, portable)
		self._name = 'SettingsPres'

	def create(self):
		self._settings = ET.Element(self._name)
		present_parametres = ET.SubElement(self._settings, "Presentation_Parameters")
		present_parametres.set("font", "Arial")
		present_parametres.set("size", "75")
		present_parametres.set("size_line", "27")
		present_parametres.set("line_per_diapo", "0")

		song = ET.SubElement(self._settings, "song")
		song.set("Numerote_diapo", "oui")
		song.set("Print_title", "oui")
		song.set("Check_bis", "oui")
		song.set("Clean_majuscule", "oui")
		song.set("Majuscule", "oui")
		song.set("Saut_ligne", "oui")
		song.set("Saut_ligne_force", "non")
		song.set("oneslide", "non")
		song.set("Ponctuation", "oui")
		song.set("Justification", "center")
		song.set("Background", os.path.join(self._dataPath, "backgrounds", "fond_bleu.jpg") )

		media = ET.SubElement(self._settings, "media")
		media.set("Numerote_diapo", "non")
		media.set("Print_title", "non")
		media.set("Check_bis", "non")
		media.set("Clean_majuscule", "oui")
		media.set("Majuscule", "non")
		media.set("Saut_ligne", "non")
		media.set("Saut_ligne_force", "non")
		media.set("oneslide", "non")
		media.set("Ponctuation", "oui")
		media.set("Justification", "center")
		media.set("Background", os.path.join(self._dataPath, "backgrounds", "fond_noir.jpg") )

		image = ET.SubElement(self._settings, "image")
		image.set("Numerote_diapo", "non")
		image.set("Print_title", "non")
		image.set("Check_bis", "non")
		image.set("Clean_majuscule", "oui")
		image.set("Majuscule", "non")
		image.set("Saut_ligne", "non")
		image.set("Saut_ligne_force", "non")
		image.set("oneslide", "non")
		image.set("Ponctuation", "oui")
		image.set("Justification", "center")
		image.set("Background", os.path.join(self._dataPath, "backgrounds", "fond_noir.jpg") )

		verse = ET.SubElement(self._settings, "verse")
		verse.set("Numerote_diapo", "oui")
		verse.set("Print_title", "oui")
		verse.set("Check_bis", "non")
		verse.set("Clean_majuscule", "non")
		verse.set("Majuscule", "non")
		verse.set("Saut_ligne", "oui")
		verse.set("Saut_ligne_force", "oui")
		verse.set("oneslide", "non")
		verse.set("Ponctuation", "oui")
		verse.set("Justification", "left")
		verse.set("Background", os.path.join(self._dataPath, "backgrounds", "fond_bleu.jpg") )

		empty = ET.SubElement(self._settings, "empty")
		empty.set("Numerote_diapo", "non")
		empty.set("Print_title", "non")
		empty.set("Check_bis", "non")
		empty.set("Clean_majuscule", "non")
		empty.set("Majuscule", "non")
		empty.set("Saut_ligne", "non")
		empty.set("Saut_ligne_force", "non")
		empty.set("oneslide", "non")
		empty.set("Ponctuation", "non")
		empty.set("Justification", "center")
		empty.set("Background", os.path.join(self._dataPath, "backgrounds", "fond_noir.jpg") )

		latex = ET.SubElement(self._settings, "latex")
		latex.set("Numerote_diapo", "non")
		latex.set("Print_title", "non")
		latex.set("Check_bis", "non")
		latex.set("Clean_majuscule", "oui")
		latex.set("Majuscule", "oui")
		latex.set("Saut_ligne", "oui")
		latex.set("Saut_ligne_force", "non")
		latex.set("oneslide", "non")
		latex.set("Ponctuation", "oui")
		latex.set("Justification", "left")
		latex.set("Background", os.path.join(self._dataPath, "backgrounds", "fond_noir.jpg") )

		latex = ET.SubElement(self._settings, "markdown")
		latex.set("Numerote_diapo", "non")
		latex.set("Print_title", "non")
		latex.set("Check_bis", "non")
		latex.set("Clean_majuscule", "oui")
		latex.set("Majuscule", "oui")
		latex.set("Saut_ligne", "oui")
		latex.set("Saut_ligne_force", "non")
		latex.set("oneslide", "non")
		latex.set("Ponctuation", "oui")
		latex.set("Justification", "left")
		latex.set("Background", os.path.join(self._dataPath, "backgrounds", "fond_noir.jpg") )

		latex = ET.SubElement(self._settings, "beamer")
		latex.set("Numerote_diapo", "oui")
		latex.set("Print_title", "oui")
		latex.set("Check_bis", "oui")
		latex.set("Clean_majuscule", "oui")
		latex.set("Majuscule", "oui")
		latex.set("Saut_ligne", "oui")
		latex.set("Saut_ligne_force", "non")
		latex.set("oneslide", "non")
		latex.set("Ponctuation", "oui")
		latex.set("Justification", "center")
		latex.set("Background", os.path.join(self._dataPath, "backgrounds", "fond_bleu.jpg") )

		latex = ET.SubElement(self._settings, "preach")
		latex.set("Numerote_diapo", "non")
		latex.set("Print_title", "oui")
		latex.set("Check_bis", "non")
		latex.set("Clean_majuscule", "non")
		latex.set("Majuscule", "non")
		latex.set("Saut_ligne", "oui")
		latex.set("Saut_ligne_force", "oui")
		latex.set("oneslide", "non")
		latex.set("Ponctuation", "oui")
		latex.set("Justification", "left")
		latex.set("Background", os.path.join(self._dataPath, "backgrounds", "fond_noir.jpg") )


GENSETTINGS = GenSettings(songfinder.__settingsPath__,
						songfinder.__dataPath__,
						songfinder.__portable__)
PRESSETTINGS = PresSettings(songfinder.__settingsPath__,
						songfinder.__dataPath__,
						songfinder.__portable__)
LATEXSETTINGS = LatexSettings(songfinder.__settingsPath__,
						songfinder.__dataPath__,
						songfinder.__portable__)
GENSETTINGS.create()
GENSETTINGS.read()
PRESSETTINGS.create()
PRESSETTINGS.read()
LATEXSETTINGS.create()
LATEXSETTINGS.read()
