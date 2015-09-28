# Created by svenko11 on 7/23/15 12:37 AM
__author__ = 'Sven Vidak'

import numpy as np
import os.path as path
from collections import Counter
from nltk.tag.stanford import StanfordPOSTagger
from src.serialization import Serializer

from src.util import Utils

POS_TAGS = ['CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNS', 'NNP', 'NNPS', 'PDT',
            'POS', 'PRP', 'PRP$', 'RB', 'RBR', 'RBS', 'RP', 'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN', 'VBP',
            'VBZ', 'WDT', 'WP', 'WP$', 'WRB']

POS_MODEL, POS_JAR = '/home/svenko11/documents/prog/Python/SemEval2015_task7/data/pos_tagger/english-bidirectional-distsim.tagger', \
                     '/home/svenko11/documents/prog/Python/SemEval2015_task7/data/pos_tagger/stanford-postagger.jar'

class POSExtractor:
	# desc is a description of dataset (e.g. 'train_task1', 'test_task2', ...)
	def __init__(self, preprocessor, desc):
		self.preprocessor = preprocessor
		self.desc = desc

	def get_pos_tag_vectors(self):
		filename = 'POS_vectors_' + self.desc + '.ser'
		if path.exists(Utils.POS_TAG_VECTORS + filename):
			return Serializer.load_object(Utils.POS_TAG_VECTORS, filename)
		tagger = StanfordPOSTagger(POS_MODEL, POS_JAR, java_options='-mx4000m')
		texts = self.preprocessor.get_raw_words()
		num_of_tags = len(POS_TAGS)
		tag_vectors = []
		print('wait for ' + str(len(texts)))
		for i, text in enumerate(texts):
			if i % 20 == 0:
				print(i)
			words = text.split()
			word_tag_tuples = tagger.tag(words)
			only_tags = [tag for _, tag in word_tag_tuples]
			tags_with_freqs = Counter(only_tags)
			tag_vector = np.zeros(num_of_tags)
			num_of_words = len(words)
			for tag, freq in tags_with_freqs.items():
				if tag in POS_TAGS:
					tag_vector[POS_TAGS.index(tag)] = freq / num_of_words
			tag_vectors.append(tag_vector)
		Serializer.save_object(Utils.POS_TAG_VECTORS, filename, np.array(tag_vectors))
