# Created by svenko11 on 7/18/15 8:42 PM
__author__ = 'Sven Vidak'

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from src.data import Parser
import re
import numpy as np

STOPWORDS_LANGUAGE = 'english'

LOWER_YEAR = 0
UPPER_YEAR = 1

FINE_GRANULARITY = 'textF'
MEDIUM_GRANULARITY = 'textM'
COARSE_GRANULARITY = 'textC'

LOWER_YEAR_BOUND = 1700
UPPER_YEAR_BOUND = 2014


class Preprocessor:
	def __init__(self, *filenames):
		self.entries = Parser.parse(filenames)
		self.stopwords = set(stopwords.words(STOPWORDS_LANGUAGE))
		self.stemmer = PorterStemmer()

	def get_clean_data(self):
		lowercase_texts = self.__extract_text()
		clean_texts = self.__remove_punctuations(lowercase_texts)

		clean_data = []
		for text in clean_texts:
			words = text.split()
			words = self.__remove_stopwords(words)
			words = self.__stem_words(words)
			clean_data.append(' '.join(words))

		return clean_data

	def get_custom_labels(self, year_type):
		text_periods = self.__get_time_periods(year_type)
		time_span_length = self.__get_time_span_length(text_periods[0])
		custom_time_spans = self.__generate_custom_time_spans(time_span_length)
		labels_lower, labels_upper = [], []
		for text_period in text_periods:
			curr_time_span = text_period.yes_time_span()
			chosen_time_span = self.__find_correct_time_span(curr_time_span, custom_time_spans)
			labels_lower.append(chosen_time_span[LOWER_YEAR])
			labels_upper.append(chosen_time_span[UPPER_YEAR])
		return labels_lower, labels_upper

	def __extract_text(self):
		return [entry.body.lower() for entry in self.entries]

	def __remove_stopwords(self, words):
		return [word for word in words if self.__is_not_stopword(word)]

	def __stem_words(self, words):
		return [self.__stem_word(word) for word in words]

	def __stem_word(self, word):
		return self.stemmer.stem(word)

	def __is_not_stopword(self, word):
		return word not in self.stopwords

	def __get_time_periods(self, year_type):
		if year_type == FINE_GRANULARITY:
			return [entry.textF for entry in self.entries]
		elif year_type == MEDIUM_GRANULARITY:
			return [entry.textM for entry in self.entries]
		elif year_type == COARSE_GRANULARITY:
			return [entry.textC for entry in self.entries]
		else:
			raise Exception('wrong year type')

	def __get_time_span_length(self, text_period):
		time_span = text_period.yes_time_span()
		return time_span[1] - time_span[0]

	def __remove_punctuations(self, texts):
		return map(lambda text: re.sub(r"[^a-zA-Z0-9\-]", " ", text), texts)

	def __generate_custom_time_spans(self, time_span_length):
		spans = []
		start = LOWER_YEAR_BOUND
		while start <= UPPER_YEAR_BOUND:
			spans.append((start, start + time_span_length))
			start += time_span_length + 1
		return spans

	def __find_correct_time_span(self, time_span, custom_time_spans):
		intersecs = []  # intersections (amount of years)
		for custom_time_span in custom_time_spans:
			intersec = min(time_span[UPPER_YEAR], custom_time_span[UPPER_YEAR]) \
			           - max(time_span[LOWER_YEAR], custom_time_span[LOWER_YEAR])
			intersecs.append(intersec)
		# take time span for which intersection is largest
		return custom_time_spans[np.argmax(intersecs)]


if __name__ == '__main__':
	p = Preprocessor('../../data/t1data/trialT1.txt')
	p.get_clean_data()
