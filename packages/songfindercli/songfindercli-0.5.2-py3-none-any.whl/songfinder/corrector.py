# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from songfinder import cache
from songfinder import distances

class Corrector(object):
	def __init__(self, words, couples=''):
		self._words = words
		self._couples = couples
		self._sizeDict = dict()
		self._couplesDict = dict()
		self._cacheList = cache.Cache(300, self._verifie_mot_opt)
		self._cacheWord = cache.Cache(300, self._verifie_mot)
		self._diffSize = 3
		self._tolerance = 0.3

		self._counter = 0

	def _getSizeDict(self):
		self._maxLengh = 0
		for word in set(self._words.split(';')):
			if word:
				try:
					self._sizeDict[len(word)].add(word)
				except KeyError:
					self._sizeDict[len(word)] = {word}
				if len(word) > self._maxLengh:
					self._maxLengh = len(word)

	def _getCouplesDict(self):
		for couple in set(self._couples.split(';')):
			for word in couple.split(' '):
				if word:
					try:
						self._couplesDict[word].add(couple)
					except KeyError:
						self._couplesDict[word] = set([couple])

	def _verifie_mot_opt(self, mot):
		if not self._sizeDict:
			self._getSizeDict()

		set_mots2 = set()
		taille = len(mot)
		rangeLow = max(1, taille-self._diffSize)
		rangeHigh = min(self._maxLengh, taille+self._diffSize) + 1
		for lengths in range(rangeLow, rangeHigh):
			if lengths in self._sizeDict:
				set_mots2 |= set( self._sizeDict[lengths] )

		props = self._verifie_mot(mot, set_mots2, self._tolerance, 1500, 0)
		if len(props) > 9:
			props = self._verifie_mot(mot, props, self._tolerance-0.1, 400, 3)
		if len(props) > 9:
			props = self._verifie_mot(mot, props, self._tolerance-0.2, 20, 3)
		return props

	def _checkCouple(self):
		if not self._couplesDict:
			self._getCouplesDict()
		word1, word2 = self._checking[self._counter:self._counter+2]
		correcs1 = self._cacheList.get(word1, args=[word1])
		correcs2 = self._cacheList.get(word2, args=[word2])
		correc_couple = set()
		for correc1 in correcs1:
			for correc2 in correcs2:
				try:
					correc_couple |= self._couplesDict[correc1] & self._couplesDict[correc2]
				except KeyError:
					pass
		if len(correcs1) == 1:
			word1 = list(correcs1)[0]
		if len(correcs2) == 1:
			word2 = list(correcs2)[0]
		sol = self._verifie_mot(' '.join([word1, word2]), correc_couple, 0.1, 1, 3)
		word1, word2 = list(sol)[0].split(' ')
		self._checking[self._counter:self._counter+2] = word1, word2

	def check(self, toCheck):
		self._toCheck = toCheck.split(' ')
		if len(self._toCheck) < 2 or not self._couples:
			self._singleCheck()
		else:
			self._coupleCheck()
		return ' '.join(self._checking)

	def _singleCheck(self):
		self._checking = []
		for word in self._toCheck:
			args = [word, self._cacheList.get(word, args=[word]), 0.05, 1, 3]
			sol = self._cacheWord.get(word, args=args)
			self._checking.append(list(sol)[0])

	def _coupleCheck(self):
		if self._counter > len(self._toCheck)-2:
			self._counter = 0
		else:
			if self._counter == 0:
				self._checking = self._toCheck
			self._checkCouple()
			self._counter += 1
			self.check(' '.join(self._checking))

	def _verifie_mot(self, mot, set_a_tester, tolerance, max_propositions, dist):
		if hasattr(distances, 'verifie_mot'):
			return distances.verifie_mot(mot, set_a_tester, tolerance, max_propositions, dist) # pylint: disable=no-member

		if not set_a_tester or not mot:
			return set([mot])
		max_ressemble = 0
		taille = len(mot)
		propositions = set()
		ressemble = 0
		if taille == 1:
			return set([mot])

		corrections = dict()
		for mot_test in set_a_tester:
			if dist == 0:
				ressemble = distances.distance_mai(mot, mot_test)
			elif dist == 1:
				ressemble = distances.distance_jar(mot, mot_test)
			elif dist == 2:
				ressemble = distances.distance_len(mot, mot_test)
			elif dist == 3:
				ressemble = round(1./3*(distances.distance_mai(mot, mot_test) + \
										distances.distance_jar(mot,mot_test) + \
										distances.distance_len(mot,mot_test)),2)
			if ressemble in corrections:
				corrections[ressemble] |= {mot_test}
			else:
				corrections[ressemble] =  {mot_test}
			if max_ressemble < ressemble:
				max_ressemble = ressemble
		if max_ressemble < 0.4:
			return set([mot])
		for ressemble, mots_ressemble in corrections.items():
			if ressemble > max_ressemble-tolerance :
				propositions |= mots_ressemble
		if len(propositions) <= max_propositions:
			return propositions
		return set([mot])

	def resetCache(self):
		self._cacheList.reset()
		self._cacheWord.reset()
