# Created by svenko11 on 8/6/15 12:57 AM
__author__ = 'Sven Vidak'

from scipy.sparse import hstack
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

def make_vectors(preprocessor, n_chars_extractor, pos_tag_extractor):
	texts = preprocessor.get_clean_data()
	vocab, data_vectors = __vectorize(texts)
	n_char_vectors = n_chars_extractor.get_n_char_vectors(vocab)
	pos_tag_vectors = pos_tag_extractor.get_pos_tag_vectors()
	vectors = hstack([hstack([data_vectors, n_char_vectors]), pos_tag_vectors])
	return vectors

def __vectorize(texts):
	count_vectorizer = CountVectorizer()
	data_counts = count_vectorizer.fit_transform(texts)
	data_tfidf = TfidfTransformer().fit_transform(data_counts)
	return count_vectorizer.vocabulary_, data_tfidf