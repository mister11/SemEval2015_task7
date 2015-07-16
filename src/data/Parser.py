# Created by svenko11 on 7/16/15 11:51 PM
__author__ = 'Sven Vidak'

from src.data.Models import TextPeriod, TextEntry
import re


def parse(*file_names):
	text_entries = []
	for file_name in file_names:
		text_entries.extend(__parse_file(file_name))
	return text_entries


def __parse_file(file_name):
	file = open(file_name, mode='r', encoding='utf-8')
	items = __get_items(file)
	regex = __item_regex()
	text_entries = []
	for item in items:
		matcher = re.match(regex, item)
		text_entries.append(__build_text_entry(matcher))
	return text_entries


# item is TextEntry in raw format (id, spans and body)
# each item is separated with an empty line (in the datasets)
def __get_items(file):
	items = []
	item = ""
	for line in file.readlines():
		line = line.strip()
		if len(line) == 0:
			items.append(item)
			item = ""
		else:
			item += line
	return items


def __item_regex():
	return r"<text id=\"(.*)\"><textF (.*)><textM (.*)><textC (.*)>(.*)</text>"


def __build_text_entry(matcher):
	entry_id = matcher.group(1)
	textF = __create_text_period(matcher.group(2))
	textM = __create_text_period(matcher.group(3))
	textC = __create_text_period(matcher.group(4))
	body = matcher.group(5)
	return TextEntry(entry_id, body, textF, textM, textC)


# raw_string is smth like: ...no="year-year" no="year-year"...yes="year-year"...
def __create_text_period(raw_string):
	parts = raw_string.strip().split()  # split by spaces, easier than to match all with regex
	yes = None
	no = []
	regex = r"(.*)=\"(.*)\""  # matching spans one by one... maches format: no="year=year" or yes="year=year"
	for part in parts:
		keyword, span = __match_spans(regex, part)
		if keyword == 'no':
			no.append(span)
		else:
			yes = span
	return TextPeriod(yes, no)


def __match_spans(regex, part):
	matcher = re.match(regex, part)
	return matcher.group(1), matcher.group(2)
