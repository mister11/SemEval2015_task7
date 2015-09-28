# Created by svenko11 on 8/9/15 2:04 PM
__author__ = 'Sven Vidak'

from src.vectors import VectorCreator
from src.classifiers import ClassifierBase

from sklearn.svm import SVC


class SVMClassifier:

	def __init__(self, preprocessor, n_chars_extractor, pos_tag_extractor):
		self.preprocessor = preprocessor
		self.n_chars_extractor = n_chars_extractor
		self.pos_tag_extractor = pos_tag_extractor

	def train(self, kernel, params):
		C = params['C']
		gamma = params['gamma']
		svc = SVC(C=C, gamma=gamma, kernel=kernel)
		data = VectorCreator.make_vectors(self.preprocessor, self.n_chars_extractor, self.pos_tag_extractor)
		ClassifierBase.train(svc, data)

	def grid_search(self, kernel, labels, C_range=(-15, 15), gamma_range=(-15, 15)):
		C_min = C_range[0]
		C_max = C_range[1]
		params = {'C': [2 ** i for i in range(C_min, C_max, 1)]}
		if gamma_range:
			gamma_min = gamma_range[0]
			gamma_max = gamma_range[1]
			params['gamma'] = [2 ** i for i in range(gamma_min, gamma_max, 1)]
		data = VectorCreator.make_vectors(self.preprocessor, self.n_chars_extractor, self.pos_tag_extractor)
		return ClassifierBase.grid_search(SVC(kernel=kernel), data, labels, params)
