#Created by svenko11 on 7/21/15 12:08 AM
__author__ = 'Sven Vidak'

import pickle
import os

def save_object(filename, obj):
	if not os.path.exists(filename):
		os.makedirs(filename)
	pickle.dump(obj, open(filename, mode='wb'))

def load_object(filename):
	return pickle.load(open(filename, mode='rb'))