# Victoria Johnston and Mitchell Patin
# 2/25/16 - Theory of Computing - CSE30151 - CP1

import sys

# function that converts a csv file into an nfa, returns start state
def load_csv(nfa_file):
	f = open(nfa_file, 'r')

	for line in f:
		line = line.rstrip()
		line = line.replace(' ','') # remove all spaces
		components = line.split(',') # seperate cells using ',' as delimiter

		# looking at the first row, add column headerst to the alphabet
		if components[0] == '':
			for piece in components[1:]:
				alphabet.append(piece)
		# for all other rows
		else:
			# check if state is start state
			if components[0][0] == '>':
				start = components[0][1:]
				components[0] = components[0].replace('>','')
			# check if state is an accept state
			elif components[0][0] == '@':
				accept.append(components[0][1:])
				components[0] = components[0].replace('@','')
			# temporary dictionary 'possible': key = alphabet symbol, value = list of next states
			possible = {}
			for index, piece in enumerate(components[1:]):
				# if the cell is not empty, create list of possible next states
				if piece != '':
					piece = piece.split('|')
					possible[alphabet[index]] = piece
			# add sub dictionary to larger dictionary 'nfa' : key = initial state, value = 'possible' dicitonary
			nfa[components[0]] = possible

	# remove epsilon, indicated with &, from the alphabet
	if '&' in alphabet:
		alphabet.remove('&')
	f.close()
	# return the start state
	return start

# function that converts answer back into the table format
def print_table():
	# cellwidth represents the longest state string, plus 2 for possible '@' and '>'
	cellwidth = len(max(oldstates, key=len)) + 2
	# print empty top-left cell
	print '{0:<{1}}'.format('', cellwidth) + ',' ,
	# print rest of the top row, which will be all symbols in the alphabet
	for symbol in alphabet:
		print '{0:<{1}}'.format(symbol, cellwidth) ,
		# unless the symbol is the last in the alphabet, add a ',' to the end of the cell
		if symbol != alphabet[-1]:
				print ',' ,
	print # go to next line
	for state, symbol in dfa.items():
		cell = ''
		# add '>' symbol to the start state's cell
		if state in start:
			cell += '>'
		# add '@' symbol to accept states' cells
		if state in newaccept:
			cell += '@'
		# add initial state which will be in the left column
		cell += str(state) 
		print '{0:<{1}}'.format(cell, cellwidth) + ',' ,
		# fill in the table where each cell represents the next state
		# at the intersection of initial state and input symbol
		for s in alphabet:
			print '{0:<{1}}'.format(symbol[s], cellwidth) ,
			if s != alphabet[-1]:
				print ',' ,
		print

# function which goes through the states in the nfa and converts all the & transitions to &*
def modify_epsilon_transitions():
	for state in nfa:
		# The &* transition contains itself
		nfa[state]['&*'] = [state]
		# if there is an epsilon transition, add states to &*
		# then remove & transition
		if '&' in nfa[state]:
			if isinstance(nfa[state]['&'], list):
				for nextstate in nfa[state]['&']:
					nfa[state]['&*'].append(nextstate)
			else:
				nfa[state]['&*'].append(nfa[state]['&'])
			nfa[state].pop('&',None)

# function gets all the transitions for parent state and symbol based on childtate transitions in nfa
# e.g. parent might be 12 so the childstates would be 1 and 2. If the symbol is 'a', check what states the children state point to with 'a'
def add_next_states(childstate,symbol,transitions):
	nextstates = [] # stores all the next states of the child
	# check the childstate has a transition with the symbol
	if symbol in nfa[childstate]:
		# check if childstate leads to multiple states
		# if it does, all all those states to the list of nextstates
		if isinstance(nfa[childstate][symbol],list):
			for nextstate in nfa[childstate][symbol]:
				nextstates.append(nextstate)
		# if the childstate only goes to one state, add that state to nextstates
		else:
			nextstates.append(nfa[childstate][symbol])
		# Go through all the states in the next state and add them to the transition for the parent state
		while (len(nextstates)):
			checkstate = nextstates.pop()
			for state in nfa[checkstate]['&*']:
				if state not in transitions[symbol]:
					transitions[symbol].append(state)

# functions adds all the &* states to the transition of parent states
def add_epsilon_transitions(childstate,symbol,transitions):
	if len(nfa[childstate]['&*']) > 1:
		for estate in nfa[childstate]['&*']:
			if estate not in transitions[symbol]:
				transitions[symbol].append(estate)

# add the newstate to the list of old states
# if new states is a list, sort it first so that the states are in order in the old state
def add_to_oldstate(oldstates,newstate):
	if isinstance(newstate,list):
		newstate.sort()
	oldstates.append(newstate)

# function that converts everything in a list to a string
def get_list_string(ls):
	string = ""
	for s in ls:
		string = string + s
	return string

def print_debug(newstate,transitions,stack,oldstates):
	print "newstate"
	print newstate
	print "transitions"
	print transitions
	print "stack"
	print stack
	print "oldstates"
	print oldstates



# Initialize variables
alphabet = []
nfa = {}
accept = []

dfa = {} # dfa starts as an empty dictionary
oldstates = [] # old states stores all states which have been added to the dfa

# read in csv file
start = load_csv(str(sys.argv[1]))

stack = [start] # stack keeps track of which dfa states have to be added

# print nfa
print "=============="
print "NFA:"
print "=============="
print "Alphabet: " + str(alphabet)
print "Transitions: " + str(nfa)
print "Start: " + str(start)
print "Accept: " + str(accept)
print

# Turn all & transitions on all states to &* transitions
modify_epsilon_transitions()

# stay in while as long as there are still states to add to the dfa
while (len(stack)):
	# get the next state to be added to the dfa
	newstate = stack.pop()

	# create the transitions for the next state to be added
	transitions = {}
	for symbol in alphabet:
		# the transition for each symbol starts off as an empty list
		transitions[symbol] = []
		if isinstance(newstate,list):
			# go through all the states in the new state
			for childstate in newstate:
				# get all the next states which the childstate goes to with the symbol
				add_next_states(childstate,symbol,transitions)
		# if the newstate is not a list it is an original state in the nfa
		# nfa original states may have epsilon transitions that need to be added
		else:
			add_next_states(newstate,symbol,transitions)
			add_epsilon_transitions(newstate,symbol,transitions)
	# add the new dfa state to the list of old states
	add_to_oldstate(oldstates,newstate)
	
	# go through all the transitions for the state to be added to the dfa
	for t in transitions:
		# if the state has transition states, append the transition states to the stack
		# convert the transitions from a list to a string
		# if the state does not have any transition stats, make transition an empty string
		if (len(transitions[t])):
			transitions[t].sort()
			if transitions[t] not in oldstates and transitions[t] not in stack:
				stack.append(transitions[t])
			transitions[t] = get_list_string(transitions[t])
		else:
			transitions[t] = ""
	
	# put the newstate and its transitions into the dfa
	# if the newstate is a list, convert it to a string
	if isinstance(newstate,list):
		dfa[get_list_string(newstate)] = transitions
	else:
		dfa[newstate] = transitions

	#print_debug(newstate,transitions,stack,oldstates)	

# get end states
newaccept = []
for state in dfa:
	for acceptstate in accept:
		if acceptstate in state:
			newaccept.append(state)

# sort dictionary alphabetically
#print dfa
#for state, symbol in dfa.items():
#		symbol = sorted(symbol)
#		print symbol

# sort alphabet alphabetically
alphabet.sort()

# print final dfa
print "=============="
print "DFA:"
print "=============="
print "Alphabet: " + str(alphabet)
print "Transitions: " + str(dfa)
print "Start: " + str(start)
print "Accept: " + str(newaccept)
print

print_table()
