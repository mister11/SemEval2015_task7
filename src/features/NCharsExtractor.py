# Created by svenko11 on 7/23/15 12:31 AM
__author__ = 'Sven Vidak'

import os.path as path
from src.serialization import Serializer

NCHARS_LOCATION = '../../data/saves/'

class NCharsExtractor:

	def __init__(self, preprocessor):
		self.preprocessor = preprocessor

	def getNChars(self, sizes=(2, 3), freq_threshold=0, remove_stopwords=True):
		filename = NCHARS_LOCATION + '_size ' + str(sizes)
		if path.exists(filename):
			return Serializer.load_object(filename)
		texts = self.preprocessor.get_raw_words()
		nchars = {}
		for text in texts:
			words = text.split()
			if remove_stopwords:
				words = self.preprocessor.remove_stopwords(words)
			self.__extract_nchars(words, sizes, nchars)
		final_nchars = [nchar for nchar, nchar_freq in nchars.items() if nchar_freq > freq_threshold]
		Serializer.save_object(filename, final_nchars)
		return final_nchars

	def __extract_nchars(self, words, sizes, nchars):
		for word in words:
			for size in sizes:
				curr_nchars = [word[i:i + size] for i in range(len(word) - size + 1)]
				for curr_nchar in curr_nchars:
					nchars[curr_nchar] = nchars.get(curr_nchar, 0) + 1
