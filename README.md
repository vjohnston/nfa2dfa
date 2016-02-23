Victoria Johnston and Mitchell Patin
2/25/16 - Theory of Computing - CSE30151



nfa2dfa is a simple python program which converts NFAs to DFAs. To use nfa2dfa simply run the following command, specifying the NFA file you'd like to convert:

$ python nfa2dfa.py nfa-1.csv



nfa2dfa accepts csv files in the following format:

- a table-like structure where column headers are symbols and the row headers are states
- cells in the table should be seperated using commas
- the start state is indicated with the (>) symbol
- accept states are indicated with the (@) symbol
- states should be integers (0-99)
- symbols should be alphabet characters (a-z)
- if an input symbol has multiple transition paths, they can be indicated with the (|) symbol
- epsilon is representd using the (&) symbol


Example:
    , a , b   , &    
 >1 , 1 , 1|2 ,
  2 , 3 ,     , 3
  3 ,   , 4   ,      
 @4 , 4 , 4   ,      