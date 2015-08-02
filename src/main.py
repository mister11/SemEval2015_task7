# Created by svenko11 on 8/2/15 2:59 PM
__author__ = 'Sven Vidak'

from src.classifiers.Classifier import Classifier
from src.data.Preprocessor import Preprocessor
from src.features.NCharsExtractor import NCharsExtractor
from src.features.POSExtractor import  POSExtractor
from src.util import Utils

from sklearn.svm import SVC

T1_TASK = 't1'
T2_TASK = 't2'

def __get_files(task):
	if task == T1_TASK:
		return __list_files(Utils.T1_FILES)
	elif task == T2_TASK:
		return __list_files(Utils.T2_FILES)

def __list_files(path):
	from os import listdir
	from os.path import isfile, join
	return [f for f in listdir(path) if isfile(join(path, f))]

def run_svc_grid_search(preprocessor, n_chars_extractor, pos_tag_extractor, year_type):
	svc = SVC(kernel='rbf')
	grid_search_params = __get_grid_search_params(C_range=(-10, 10), gamma_range=(-10, 10), is_rbf=svc.kernel == 'rbf')
	classifier = Classifier(svc, preprocessor, year_type, n_chars_extractor, pos_tag_extractor)
	classifier.grid_search(grid_search_params)

def __get_grid_search_params(C_range=(-20, 20), gamma_range=(-20, 20), is_rbf=True):
	C_low = C_range[0]
	C_up = C_range[1]
	gamma_low = gamma_range[0]
	gamma_up = gamma_range[1]
	C = [2 ** i for i in range(C_low, C_up, 1)]
	if is_rbf:
		gamma = [2 ** i for i in range(gamma_low, gamma_up, 1)]
		return {'C': C, 'gamma': gamma}
	return {'C': C}

if __name__ == '__main__':
	preprocessor = Preprocessor(__get_files(T1_TASK))
	n_chars_extractor = NCharsExtractor(preprocessor)
	pos_tag_extractor = POSExtractor(preprocessor, 'train_' + T1_TASK)

	run_svc_grid_search(preprocessor, n_chars_extractor, pos_tag_extractor, year_type='textC')