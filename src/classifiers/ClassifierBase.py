# Created by svenko11 on 7/25/15 9:31 PM
__author__ = 'Sven Vidak'

from sklearn.grid_search import GridSearchCV

def train(classifier, data):
	classifier.fit(data)
	# todo - no return?
	return classifier

def grid_search(classifier, data, labels, params, folds=5, jobs=-1, verbose_level=3):
	gs = GridSearchCV(classifier, params, n_jobs=jobs, cv=folds, verbose=verbose_level)
	gs.fit(data, labels)
	return gs.best_params_
