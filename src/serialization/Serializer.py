#Created by svenko11 on 7/21/15 12:08 AM
__author__ = 'Sven Vidak'

import pickle
import os

def save_object(directroy, filename, obj):
	if not os.path.exists(directroy):
		os.makedirs(directroy)
	pickle.dump(obj, open(directroy + filename, mode='wb'))

def load_object(directory, filename):
	return pickle.load(open(directory + filename, mode='rb'))