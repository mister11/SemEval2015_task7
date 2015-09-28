# Created by svenko11 on 8/2/15 2:59 PM
__author__ = 'Sven Vidak'

from src.data.Preprocessor import Preprocessor
from src.features.NCharsExtractor import NCharsExtractor
from src.features.POSExtractor import POSExtractor
from src.util import Utils

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
	return [join(path, f) for f in listdir(path) if isfile(join(path, f))]


if __name__ == '__main__':
	preprocessor = Preprocessor(__get_files(T1_TASK))
	n_chars_extractor = NCharsExtractor(preprocessor)
	pos_tag_extractor = POSExtractor(preprocessor, 'train_' + T1_TASK)
