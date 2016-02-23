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

def modify_epsilon_transitions():
	# create a new nfa with transitions from each symbol in alphabet
	for state in nfa:
		# create &*
		# create a list and add the state as the first element
		nfa[state]['&*'] = [state]
		# if there is an epsilon transition, add states to ep*
		if '&' in nfa[state]:
			for nextstate in nfa[state]['&']:
				nfa[state]['&*'].append(nextstate)
			# remove & transition
			nfa[state].pop('&',None)

def add_next_states(childstate,symbol,transitions):
	nextstates = []
	if symbol in nfa[childstate]:
		if isinstance(nfa[childstate][symbol],list):
			for nextstate in nfa[childstate][symbol]:
				nextstates.append(nextstate)
		else:
			nextstates.append(nfa[childstate][symbol])
		while (len(nextstates)):
			checkstate = nextstates.pop()
			for state in nfa[checkstate]['&*']:
				if state not in transitions[symbol]:
					transitions[symbol].append(state)

def add_epsilon_transitions(childstate,symbol,transitions):
	if len(nfa[childstate]['&*']) > 1:
		for estate in nfa[childstate]['&*']:
			if estate not in transitions[symbol]:
				transitions[symbol].append(estate)

dfa = {}
queue = [start]
oldstates = []
count = 0

modify_epsilon_transitions()

# stay in while until there are no more states to add
while (len(queue)):
	# get first element from the list
	newstate = queue.pop()
	print "newstate"
	print newstate

	# create dictionary for new state
	transitions = {}
	for symbol in alphabet:
		transitions[symbol] = []
		states_to_check = []
		for childstate in newstate:
			# check if the symbol is in the nfa
			print symbol
			print childstate
			#if symbol in nfa[childstate]:
				# check if the symbol is a list
			#	if isinstance(nfa[childstate][symbol],list):
			#		# if a symbol maps to a list of states, add each state to the transition
			#		for s in nfa[childstate][symbol]:
			#			states_to_check.append(s)
			#	else:
			#		states_to_check.append(nfa[childstate][symbol])
			#	print states_to_check
			#	print nfa
			#	while (len(states_to_check)):
			#		state = states_to_check.pop()
					# add &* transitions to transitions
			#		for s in nfa[state]['&*']:
			#			if s not in transitions[symbol]:
			#				print "Push " + s
			#				transitions[symbol].append(s)
			add_next_states(childstate,symbol,transitions)
			if not isinstance(newstate,list):
				add_epsilon_transitions(childstate,symbol,transitions)
				#if newstate in nfa:
			#	if len(nfa[childstate]['&*']) > 1:
			#		for s in nfa[childstate]['&*']:
		#		if symbol in nfa[childstate]:
			#			if s not in transitions[symbol]:
			#				print "push " + s
			#				transitions[symbol].append(s)
				#print transitions[symbol]
	
	if isinstance(newstate,list):
		newstate.sort()
	oldstates.append(newstate)
	for a in transitions:
		statestr = ""
		if (len(transitions[a])):
			transitions[a].sort()
			for n in transitions[a]:
				statestr = statestr + n
			if transitions[a] not in oldstates and transitions[a] not in queue:
				queue.append(transitions[a])
			transitions[a] = statestr
		else:
			transitions[a] = ""
	
	newstatestr = ""
	if isinstance(newstate,list):
		for state in newstate:
			newstatestr = newstatestr + state
		dfa[newstatestr] = transitions
	else:
		dfa[newstate] = transitions
	print "newstate"
	print newstate
	print "transitions"
	print transitions
	print "queue"
	print queue
	print "oldstates"
	print oldstates
	#if count == 3:
	#	break
	#count = count + 1
print dfa
