# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 20:29:48 2014

@author: dan
"""

from collections import deque

class Grammar:
    ''' Grammar: holds nonterminals, terminals, productions, and start symbol
    '''
    
    def __init__(self):
        
        # Productions: prods[nonterm] -> sequence it converts to
        self.prods = {}
        
        # Terminals: all allowed terminals
        self.terms = set()
        
        self.start = None
        self._best_prods = None
    
    def add_nonterminal(self, nonterm):
        assert(nonterm not in self.prods and nonterm not in self.terms)
        self.prods[nonterm] = set()
    
    def add_terminal(self, term):
        assert(term not in self.prods and term not in self.terms)
        self.terms.add(term)
        
    def set_start_symbol(self, nonterm):
        ''' Set the symbol as the starting symbol '''
        assert(nonterm in self.prods)
        self.start = nonterm
        
    def add_production(self, nonterm, sequence):
        assert( isinstance(sequence, tuple) or
                isinstance(sequence, str))
                
        assert( len(sequence) >= 1 )
        assert( nonterm != sequence[0] ) # Make sure the grammar is safe
        
        for term in sequence:
            assert((term in self.terms and term not in self.prods) or
                   (term in self.prods and term not in self.terms))
        self.prods[nonterm].add(sequence)
   
    
    def _check_input_aux(self, nonterm):
        
        if (len(self._input_stack) > 0):
            # Backup the global data before we break them            
            input_backup = deque(self._input_stack)
            prods_backup = deque(self._prods_so_far)
            
            for prod in sorted(self.prods[nonterm], key=lambda x: -len(x)):
                # Try a prod!
                self._prods_so_far.append(str(nonterm)+'->'+str(prod))
                print 'Trying', self._prods_so_far
                
                lasti = 0
                for i, x in enumerate(prod):
                    lasti = i
                    # Check every token (x) of the prod
                    if x in self.prods:
                        print x, 'is a nonterm'
                        if not self._check_input_aux(x): 
                        # This had side effects!!!
                        # We undo them.
                            print x,'failed.'
                            print self._prods_so_far, self._input_stack
                            self._input_stack = deque(input_backup)
                            self._prods_so_far = deque(prods_backup)
                            break
                        
                    elif x in self.terms:
                        if x == '':
                            print 'okaying empty'
                            
                        elif len(self._input_stack) > 0 and x == self._input_stack[0]:
                            self._input_stack.popleft()
                        
                        else:
                            self._input_stack = deque(input_backup)
                            self._prods_so_far = deque(prods_backup)
                            break
                    else:
                        # Error
                        print 'Error'
                        self._input_stack = deque(input_backup)
                        self._prods_so_far = deque(prods_backup)
                        break
            if (lasti == (len(prod)-1)) and len(self._input_stack)==0:
                if self._best_prods == None:
                    print 'best prods:', self._prods_so_far
                    self._best_prods = deque(self._prods_so_far)
                return True
            else:
                return False
        else:
            # We got to length 0, and no return False. We finished!
            
            return True
            
        
    def check_input(self, input_sequence):
    # TODO: read grammar from file (via the add_/set_ functions!)
    
        '''     Check the input against the grammar, starting with the starting
            symbol nonterminal.
                Makes sure all symbols are parsed, so that the whole input
            corresponds to the grammar.
                Returns:
            if the input is valid:
                - the list of used productions (in order)
                - the rest of the input sequence
                if the input is not valid:
                    Raises exception
        '''
        # Make sure there exists a start element
        assert(self.start)
        
        self._prods_so_far = deque([])                      # working stack, starts empty
        self._input_stack = deque(input_sequence) # input stack, starts with input    
        
        return self._check_input_aux(self.start)
        
    
    
if __name__ == '__main__':
    g = Grammar()
    
    '''
    Gramatica exemplu din curs:
    ({S}, {a,b,c}, {S->aSbS|aS|c}, S)
    
    Gramatica pe care am folosit-o aici:
    http://jflap.org/tutorial/grammar/LL/index.html
    
    '''

    
    '''
    g.add_terminal('a')
    g.add_terminal('b')
    g.add_terminal('')
    g.add_nonterminal('A')
    g.add_nonterminal('B')
    g.add_nonterminal('S')
    g.add_production('S', 'A')
    g.add_production('S', 'B')
    g.add_production('A', ('a','A'))
    g.add_production('A', ('',))
    g.add_production('B', 'bS')
    g.set_start_symbol('S')
    g.check_input('aaa')
    print g._best_prods
    '''
    '''
    Should show:
    S->A, A->aA, A->aA, A->aA, A->''  - WORKS!
    '''


    g.add_terminal('a')
    g.add_terminal('b')
    g.add_terminal('c')
    g.add_nonterminal('S')
    g.add_production('S', 'aSbS')
    g.add_production('S', 'aS')
    g.add_production('S', 'c')
    g.set_start_symbol('S')
    print g.check_input('aacbc')
    print g._prods_so_far
  
    '''
    Should show:
    S->aSbS, S->aS, S->c, S->c
    
    '''