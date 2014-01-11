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
        assert(nonterm not in self.terms)
        if nonterm not in self.prods:
            self.prods[nonterm] = []
    
    def add_terminal(self, term):
        assert(term not in self.prods)
        self.terms.add(term)
        
    def set_start_symbol(self, nonterm):
        ''' Set the symbol as the starting symbol '''
        assert(nonterm in self.prods)
        self.start = nonterm
        
    def add_production(self, nonterm, sequence):
        assert(isinstance(sequence, tuple) or
                isinstance(sequence, str))
                
        assert(len(sequence) >= 1)
        assert(nonterm != sequence[0])  # Make sure the grammar is safe
        
        for term in sequence:
            assert((term in self.terms and term not in self.prods) or
                   (term in self.prods and term not in self.terms))
        self.prods[nonterm].append(sequence)
   
        
    def parse(self, input):
        index = 0
        state = 'q'
        self.alpha = []
        self.beta = [self.start]
        
        
        while state in ['q', 'b']:
            if(state == 'q'):
                
                if (len(self.beta) == 1 and self.beta[0] == '' or len(self.beta) == 0):
                    return 't', index , self.alpha
                # expand
                
                elif(self.beta[0] in self.prods):
                    self.alpha.append((self.beta[0], 0))
                    prod = self.prods[self.beta[0]][0]
                    self.beta.pop(0)
                    self.beta = [x for x in prod] + self.beta
                
               
                elif(len(input) == index):
                    state = 'b'  
                # advance  
                elif(self.beta[0] in self.terms and input[index] == self.beta[0]):
                    
                    index += 1
                    self.alpha.append(self.beta[0])
                    self.beta.pop(0)
                
                # insuccess
                elif (len(self.alpha) > 0 and self.alpha[-1] != input[index]):
                    
                    state = 'b'
                else:
                    print "you dun goofed"
                
                
                
            elif(state == 'b'):
                # back
                try:
                    self.alpha[-1]
                except Exception as e:
                    print self.alpha 
                if(len(self.alpha) > 0 and self.alpha[-1] in self.terms):
                    index -= 1
                    self.beta.insert(0, self.alpha[-1])
                    self.alpha.pop()
                # another try
                elif len(self.alpha) > 0 and isinstance(self.alpha[-1], tuple):
                    NT, j = self.alpha.pop()
                    
                    prod = self.prods[NT][j]
                    for _ in prod:
                        assert(_ == self.beta[0])
                        self.beta.pop(0)
                    if index >= 0 and self.beta[0] != self.start:
                        # branch 1
                        # clean up the production from beta
                        if j < len(self.prods[NT]) - 1:
                            j += 1
                            self.alpha.append((NT, j))
                            self.beta = [x for x in self.prods[NT][j]] + self.beta
                            state = 'q'
                            
                        # branch 2
                        # retreaaat                            
                        elif j >= len(self.prods[NT]) - 1:
                            
                            self.beta.insert(0, NT)
                    else:
                        # branch 3
                        # error
                        return 'e', index, self.alpha, self.beta
            else:
                print "shit went wrong 2 " + state 
        
                
            
            
            
        
    
if __name__ == '__main__':
    g = Grammar()
    
    '''
    Gramatica exemplu din curs:
    ({S}, {a,b,c}, {S->aSbS|aS|c}, S)
    
    Gramatica pe care am folosit-o aici:
    http://jflap.org/tutorial/grammar/LL/index.html
    
    '''

    
    
    g.add_terminal('a')
    g.add_terminal('b')
    g.add_terminal('')
    g.add_nonterminal('A')
    g.add_nonterminal('B')
    g.add_nonterminal('S')
    g.add_production('S', 'A')
    g.add_production('S', 'B')
    g.add_production('A', ('a', 'A'))
    g.add_production('A', ('',))
    g.add_production('B', 'bS')
    g.set_start_symbol('S')
    print g.parse('aaa')
    
    '''
    Should show:
    S->A, A->aA, A->aA, A->aA, A->''  - WORKS!
    '''

    g = Grammar()
    g.add_terminal('a')
    g.add_terminal('b')
    g.add_terminal('c')
    g.add_nonterminal('S')
    g.add_production('S', 'aSbS')
    g.add_production('S', 'aS')
    g.add_production('S', 'c')
    g.set_start_symbol('S')
    print g.parse('aacbc')
    '''
    Should show:
    S->aSbS, S->aS, S->c, S->c
    
    '''
