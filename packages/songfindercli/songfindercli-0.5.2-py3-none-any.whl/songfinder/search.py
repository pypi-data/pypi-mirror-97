# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import division

import logging

from songfinder import corrector
from songfinder import cache
from songfinder import gestchant

class Searcher(object):
	def __init__(self, dataBase):
		self._dataBase = dataBase
		self._correctors = dict()
		self._cache = cache.Cache(100, self._search)
		singles = ';'.join((sets[0] for sets in self._dataBase.getDico('lyrics').values()))
		couples = ';'.join((sets[1] for sets in self._dataBase.getDico('lyrics').values()))
		self._corrector = corrector.Corrector(singles, couples)
		self._tolerance =  0.3

	def search(self, toSearch):
		if not toSearch.isdigit():
			self._toSearch = gestchant.netoyage_paroles(toSearch)
		else:
			self._toSearch = toSearch
		# ~ tmps1=time.time()
		self._toSearch = self._corrector.check(self._toSearch)
		# ~ logging.debug('temps corrections %ss'%(time.time()-tmps1))
		return self._cache.get(self._toSearch, args=[self._toSearch])

	def _search(self, toSearch): # Use of caching
		if toSearch.isdigit():
			try:
				num = int(toSearch)
				return list(self._dataBase.getDico('nums')[num])
			except KeyError:
				logging.warning('%s does not correspond to any number in dataBase'%toSearch)
		self._songDict = self._dataBase.getDico('lyrics')
		self._found = self._dataBase.keys()
		self._searchCore()
		if len(self._found) > 20:
			self._searchCore()
		return self._found[:9]

	def _searchCore(self):
		self._toSearchList = self._toSearch.split(' ')
		self._tolerance =  0.3

		if len(self._found) != 1:
			self._keyWordSearch(1)
			if len(self._toSearchList) > 1 and len(self._found) > 5:
				self._keyWordSearch(2)
			if len(self._toSearchList) > 2 and len(self._found) > 5:
				self._keyWordSearch(3)
			if len(self._toSearchList) > 1 and len(self._found) > 5:
				self._tolerance = 0.2
				self._keyWordSearch(2)
			if len(self._toSearchList) > 1 and len(self._found) > 5:
				self._tolerance = 0.1
				self._keyWordSearch(2)
			if len(self._toSearchList) > 2 and len(self._found) > 5:
				self._keyWordSearch(3)

	def _keyWordSearch(self, nbWords):
		dico_taux = dict()
		toSearchSet = set()
		plusieurs_mots = []
		for i,mot in enumerate(self._toSearchList):
			plusieurs_mots.append(mot)
			if i > nbWords-2:
				toSearchSet.add(' '.join(plusieurs_mots))
				plusieurs_mots = plusieurs_mots[1:]
		taux_max = 0
		for song in self._found:
			refWords = self._songDict[song][nbWords-1]
			refSet = set(refWords.split(';'))
			taux = len(toSearchSet &  refSet)/len(toSearchSet)

			try:
				dico_taux[taux].append(song)
			except KeyError:
				dico_taux[taux] = [song]

			if taux > taux_max:
				taux_max = taux

		self._found = []
		taux_ordered = sorted(dico_taux.keys(), reverse=True)
		for taux in taux_ordered:
			if taux > taux_max-self._tolerance-nbWords/10:
				self._found += sorted(dico_taux[taux])

	def resetCache(self):
		self._cache.reset()
		self._corrector.resetCache()
