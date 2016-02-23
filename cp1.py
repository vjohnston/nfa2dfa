# starting nfa example
#nfa = {'p': {0:'p',1:['p','q']}, 'q':{}}
#nfa = {'1': {'a':'2', 'c':'4'}, '2': {'b':'3', '&':'1'}, '3': {'a':'2'}, '4': {'c':'3', '&':'3'}}
#alphabet = ['a','b','c']
#nfa = {'a': {'1': ['a','b'], '0': 'a'}, 'c': {'1': 'd'}, 'b': {'0': 'c', '&': 'c'}, 'd': {'1': 'd', '0': 'd'}}
#alphabet = ['0','1']
#nfa = {'12':{'a':['12','24'],'b':'24'},'24':{'b':'12'}}
#nfa = {'1':{'a':'3', '&':'2'},'2':{'a':'1'},'3':{'a':'2','b':['2','3']}}
alphabet = ['a','b']
#nfa = {'1':{'a':['3'], '&':['2']},'2':{'a':['1']},'3':{'a':['2'],'b':['2','3']}}
nfa = {'1':{'a':['3'], '&':['2']},'2':{'a':['1']},'3':{'a':['2'],'b':['2','3']}}
start = '1'

print nfa

# function which goes through the states in the nfa and converts all the & transitions to &*
def modify_epsilon_transitions():
	for state in nfa:
		# The &* transition contains itself
		nfa[state]['&*'] = [state]
		# if there is an epsilon transition, add states to &*
		# then remove & transition
		if '&' in nfa[state]:
			for nextstate in nfa[state]['&']:
				nfa[state]['&*'].append(nextstate)
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
dfa = {} # dfa starts as an empty dictionary
stack = [start]	# stack keeps track of which dfa states have to be added
oldstates = [] # old states stores all states which have been added to the dfa

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
		# go through all the states in the new state
		for childstate in newstate:
			# get all the next states which the childstate goes to with the symbol
			add_next_states(childstate,symbol,transitions)
			# if the newstate is not a list it is an original state in the nfa
			# nfa original states may have epsilon transitions that need to be added
			if not isinstance(newstate,list):
				add_epsilon_transitions(childstate,symbol,transitions)
	
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

#	print_debug(newstate,transitions,stack,oldstates)	

print dfa
