# Created by svenko11 on 7/16/15 12:07 AM
__author__ = 'Sven Vidak'


"""
	There are two ways to implement this class.

	First is this way where a time span tuple is calculated when it's needed.

	On the other hand, if there are lots and lots of calls for those two methods, it's better to
	convert time spans into tuples at object creation (init method).

	--> see todo

"""

# todo - so far, there are no many calls to methods
class TextPeriod:
	def __init__(self, yes, no):
		self.no = no  # array of spans in format 'year1-year2'
		self.yes = yes  # one year in a format same as above

	def yes_time_span(self):
		return _extract_time_span(self.yes)

	def no_time_span(self, index):
		return _extract_time_span(self.no[index])


def _extract_time_span(span):
	parts = span.split('-')
	return int(parts[0]), int(parts[1])


class TextEntry:
	def __init__(self, entry_id, body, textF, textM, textC):
		self.id = entry_id
		self.body = body
		# TextPeriod-s for each granularity
		self.textF = textF
		self.textM = textM
		self.textC = textC
