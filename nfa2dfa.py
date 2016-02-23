# Theory of Computing
# Project 1
# 2/25/16

import sys

def load_csv(nfa_file):

		f = open(nfa_file, 'r')
		for line in f:
			line = line.rstrip()
			line = line.replace(' ','')
			components = line.split(',')

			if components[0] == '':
				for piece in components[1:]:
					alphabet.append(piece)
			else:
				if components[0][0] == '>':
					start = components[0][1:]
					components[0] = components[0].replace('>','')
				elif components[0][0] == '@':
					accept.append(components[0][1:])
					components[0] = components[0].replace('@','')

				possible = {}
				for index, piece in enumerate(components[1:]):
					if piece != '':
						piece = piece.split('|')
						possible[alphabet[index]] = piece
				transitions[components[0]] = possible

		f.close()

alphabet = []
transitions = {}
start = 0
accept = []

load_csv(str(sys.argv[1]))

print
print "Alphabet: " + str(alphabet)
print "Transitions: " + str(transitions)
print "Start: " + str(start)
print "Accept: " + str(accept)
print