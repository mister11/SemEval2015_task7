# Created by svenko11 on 7/23/15 12:31 AM
__author__ = 'Sven Vidak'

import numpy as np
from collections import Counter
import os.path as path
from src.serialization import Serializer
from src.util import Utils

# todo - extract code to methods

class NCharsExtractor:

	def __init__(self, preprocessor, sizes, freq_threshold, remove_stopwords=True):
		self.preprocessor = preprocessor
		self.sizes = sizes
		self.freq_threshold = freq_threshold
		self.remove_stopwords = remove_stopwords
		self.texts = None

	def get_n_char_vectors(self):
		filename = self.__get_filename(Utils.N_CHAR_VECTORS)
		if path.exists(filename):
			return Serializer.load_object(filename)
		n_chars = self.__get_n_chars()
		n_char_vecs = []
		n_char_count = len(n_chars)
		self.texts = self.preprocessor.get_raw_words() if self.texts is None else self.texts
		for i, text in enumerate(self.texts):
			words = text.split()
			n_char_vec = np.zeros(n_char_count)
			for word in words:
				for size in self.sizes:
					word_n_chars = [word[j:j + size] for j in range(len(word) - size + 1)]
					word_n_chars_with_freqs = Counter(word_n_chars)
					for n_char, freq in word_n_chars_with_freqs.items():
						if n_char in n_chars:
							n_char_vec[n_chars.index(n_char)] = freq / len(words)  # py3 does division right!
			n_char_vecs.append(n_char_vec)

		numpy_array = np.array(n_char_vecs) # creates numpy array from python array
		Serializer.save_object(filename, numpy_array)
		return numpy_array

	def __get_n_chars(self):
		filename = self.__get_filename(Utils.N_CHARS_LOCATION)
		if path.exists(filename):
			return Serializer.load_object(filename)
		self.texts = self.preprocessor.get_raw_words() if self.texts is None else self.texts
		n_chars = {}
		for text in self.texts:
			words = text.split()
			if self.remove_stopwords:
				words = self.preprocessor.remove_stopwords(words)
			self.__extract_n_chars(words, n_chars)
		final_n_chars = self.__filter_by_freq_threshold(n_chars)
		Serializer.save_object(filename, final_n_chars)
		return final_n_chars

	def __extract_n_chars(self, words, n_chars):
		for word in words:
			for size in self.sizes:
				curr_n_chars = [word[i:i + size] for i in range(len(word) - size + 1)]
				for curr_n_char in curr_n_chars:
					n_chars[curr_n_char] = n_chars.get(curr_n_char, 0) + 1

	def __filter_by_freq_threshold(self, n_chars):
		return [n_char for n_char, n_char_freq in n_chars.items() if n_char_freq > self.freq_threshold]

	def __get_filename(self, base):
		return base + 'size_' + str(self.sizes) + '_thresh_' + str(self.freq_threshold) \
		            + '_rm_stopwords_' + str(self.remove_stopwords)