import argparse
import collections
import codecs
import os

letter_info = ['Most frequent: E T A O I N S H R D L U\nInitial: T O A W B C D S F M R H I Y E G L N P U J K\nfinal: E S T D N R Y F L O G H A K M P U W\nWords: a, I']
sequence_info = ['Digraphs: th er on an re he in ed nd ha at en es of or nt ea ti to it st io le is ou ar as de rt ve\nWords: of, to, in, it, is, be, as, at, so, we, he, by, or, on, do, if, me, my, up, an, go, no, us, am\nDoubles: ss ee tt ff ll mm oo',
		'Trigraphs: the and tha ent ion tio for nde has nce edt tis oft sth men\nWords: the, and, for, are, but, not, you, all, any, can, had, her, was, one, our, out, day, get, has, him, his, how, man, new, now, old, see, two, way, who, boy, did, its, let, put, say, she, too, use',
'Words: that, with, have, this, will, your, from, they, know, want, been, good, much, some, time']

def parse_arg():
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', type=str, required=True)
	parser.add_argument('-s', '--sequence', default=4, type=int)
	parser.add_argument('-o', '--occurences', default=3 ,type=int)
	parser.add_argument('-m', '--max', default=26, type=int)
	parser.add_argument('-n', '--nth', default=1, type=int)
	parser.add_argument('-i', '--info', action='store_true')
	args = parser.parse_args()
	main(args)

def main(args):
	text = read_file(args.file, False)
	get_file_info(args, text)
	analyze_letter(text, args.occurences, args.max, args.nth, args.info)
	analyze_sequence(text, args.sequence, args.occurences, args.max, args.info)

""" Prints basic information about the file analyzed """
def get_file_info(args, text):
	print('Frequency analysis report of: %s' % os.path.abspath(args.file))
	textLen = len(read_file(args.file, False))
	textLenSpace = len(read_file(args.file, True))
	print('Characters (including space): %d' % textLen)
	print('Characters (excluding space): %d' % textLenSpace)
	print('\nSETTINGS')
	print('Sequence: %d' % args.sequence)
	print('Occurences: %d' % args.occurences)
	print('Max: %d' % args.max)
	print('nth: %d' % args.nth)
	print('Info: %r' % args.info)
	print('')

""" Frequency analysis of a sequence of x length """
def analyze_sequence(text, seq, occ, max, info):
	if seq < 2 or seq > len(text):
		seq = 2

	for s in range(2, seq+1):
		print('Sequence frequency | length: %d, min occurences: %d, max results: %d' % (s, occ, max))
		if info:
			i = s - 2
			if i < len(sequence_info):
				print(sequence_info[i])
		seqList = get_sequence_list(text, s)
		freq = collections.Counter(seqList)
		freq = freq.most_common(max)
		print_collection(freq)


""" Returns a list with all posibilities of x sequence """
def get_sequence_list(text, sequence):
	seqList = []
	for i in range(0, len(text) + 1 - sequence):
		seqList.append(text[i:i+sequence])
	return seqList


""" Analyzes individual letters """
def analyze_letter(text, occ, max, nth, info):
	if nth < 1 or nth > len(text):
		nth = 1

	for n in range(1, nth + 1):
		print('Letter frequency of every %d letter' %n)
		if info:
			print(letter_info[0])
		freq = collections.Counter(text[::n])
		freq = freq.most_common(max)
		print_collection(freq)

def print_collection(collection):
	for i in range(len(collection)):
		print('%s => %d' % (collection[i][0], collection[i][1]))
	print('')


""" Reads text from a file, returns the file content """
def read_file(file, ws):
	text = codecs.open(file, 'r', encoding='utf-8').read()
	if ws is False:
		text = ''.join(text.split())
	return text


if __name__ == '__main__':
	parse_arg()
