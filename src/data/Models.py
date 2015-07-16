# Created by svenko11 on 7/16/15 12:07 AM
__author__ = 'Sven Vidak'


class TextPeriod:
	def __init__(self, yes, no):
		self.no = no
		self.yes = yes

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
		self.textF = textF
		self.textM = textM
		self.textC = textC
