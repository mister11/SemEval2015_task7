# Created by svenko11 on 7/25/15 9:31 PM
__author__ = 'Sven Vidak'

from scipy.sparse import hstack

from sklearn.grid_search import GridSearchCV
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

class Classifier:
	def __init__(self, classifier, preprocessor, year_type, n_chars_extractor, pos_tag_extractor):
		self.classifier = classifier
		self.preprocessor = preprocessor
		self.year_type = year_type
		self.n_chars_extractor = n_chars_extractor
		self.pos_tag_extractor = pos_tag_extractor

	def grid_search(self, params, folds=5, jobs=-1, verbose_level=3):
		gs = GridSearchCV(self.classifier, params, n_jobs=jobs, cv=folds, verbose=verbose_level)
		labels = self.preprocessor.get_custom_labels(self.year_type)[0]
		gs.fit(self.__make_vectors(), labels)
		print(gs.best_params_)

	def __make_vectors(self):
		texts = self.preprocessor.get_clean_data()
		vocab, data_vectors = self.__vectorize(texts)
		n_char_vectors = self.n_chars_extractor.get_n_char_vectors(vocab)
		pos_tag_vectors = self.pos_tag_extractor.get_pos_tag_vectors()

		return hstack([data_vectors, n_char_vectors, pos_tag_vectors])

	def __vectorize(self, texts):
		count_vectorizer = CountVectorizer()
		data_counts = count_vectorizer.fit_transform(texts)
		data_tfidf = TfidfTransformer().fit_transform(data_counts)
		return count_vectorizer.vocabulary_, data_tfidf

