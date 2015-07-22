# Created by svenko11 on 7/23/15 12:37 AM
__author__ = 'Sven Vidak'

import numpy as np
import os.path as path
from collections import Counter
from nltk.tag.stanford import POSTagger
from src.serialization import Serializer

POS_TAGS = ['CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNS', 'NNP', 'NNPS', 'PDT',
            'POS', 'PRP', 'PRP$', 'RB', 'RBR', 'RBS', 'RP', 'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN', 'VBP',
            'VBZ', 'WDT', 'WP', 'WP$', 'WRB']

POS_MODEL, POS_JAR = '../data/pos_tagger/english-bidirectional-distsim.tagger', \
                     '../data/pos_tagger/stanford-postagger.jar'

PICKLES_LOCATION = '../data/pickles/'


class POSExtractor:
	# desc is a description of dataset (e.g. 'train_task1', 'test_task2', ...)
	def __init__(self, preprocessor, desc):
		self.preprocessor = preprocessor
		self.desc = desc

	def getPOSTagVectors(self):
		filename = 'POS_vectors_' + self.desc
		if path.exists(filename):
			return Serializer.load_object(filename)
		tagger = POSTagger(POS_MODEL, POS_JAR, java_options='-mx4000m')
		texts = self.preprocessor.get_raw_words()
		num_of_tags = len(POS_TAGS)
		tag_vectors = []
		for text in texts:
			words = text.split()
			word_tag_tuples = tagger.tag(words)
			only_tags = [tag for _, tag in word_tag_tuples]
			tags_with_freqs = Counter(only_tags)
			tag_vector = np.zeros(num_of_tags)
			num_of_words = len(words)
			for tag, freq in tags_with_freqs.items():
				tag_vector[POS_TAGS.index(tag)] = freq / num_of_words
			tag_vectors.append(tag_vector)
		Serializer.save_object(filename, np.array(tag_vectors))
