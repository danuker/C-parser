# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 20:29:48 2014

@author: dan
"""

class Grammar:
    ''' Grammar: holds nonterminals, terminals, productions, and start symbol
    '''
    
    def __init__(self):
        
        # Productions: prods[nonterm] -> sequence it converts to
        self.prods = {}
        
        # Terminals: all allowed terminals
        self.terms = set()
    
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
        assert( isinstance(sequence, list) or isinstance(sequence, tuple) )
        assert( len(sequence) >= 1 )
        assert( nonterm != sequence[0] ) # Make sure the grammar is safe
        
        for term in sequence:
            assert((term in self.terms and term not in self.prods) or
                   (term in self.prods and term not in self.terms))
        self.prods[nonterm].add(sequence)
    
    def _check_input_partial(self, input_sequence, start_nonterm):
        '''     Check the input against the grammar, starting with the starting
            symbol nonterminal, 
            
            BUT don't care if symbols remain at the end!
            
                Returns the parsed structure if the input is valid
            or None otherwise
        '''        
        
        # Iterate through productions of start_nonterm
            # And recursively perform _check_input_partial
        # TODO: make sure production check is made from longest to shortest
        # TODO: return remaining sequence and structure so far
    
    
    def check_input(self, input_sequence):
        '''     Check the input against the grammar, starting with the starting
            symbol nonterminal.
                Makes sure all symbols are parsed, so that the whole input
            corresponds to the grammar.
                Returns the parsed structure if the input is valid
            or None otherwise
        '''
        
        remaining_toks, tree = \
            self._check_input_partial(input_sequence, self.start)
        
        return tree if len(remaining_toks) == 0 else None
    
    # TODO: read grammar from file (via the add_/set_ functions!)