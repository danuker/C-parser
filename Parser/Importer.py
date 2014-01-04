'''
Created on Jan 4, 2014

@author: Drone
'''
from Grammar import Grammar
import re
import collections
import sys

class Importer:
    '''
    scans the grammar from the doc and gets terminals/non-terminals
    '''
    stream = ""
    Token = collections.namedtuple('Token', ['type', 'value'])
    def __init__(self, gram):
        self.gram = gram
        self.readFromFile()
        
    def parse(self):
        pos = lineStart = 0
             
        # ... as well as the current line.
        line = 1
        tokenSpec = [
        # Relation operators
        ('NONTERMINAL', r'(?<=<)[a-zA-z]+(?=>)'),
        ('TERMINAL', r'(?<=\n\d\n).+|(?<=\n\d\d\n).+'),
        ('SKIP', r'[ \t]')
        ]
        tokenRegex = '|'.join('(?P<%s>%s)' % pair for pair in tokenSpec)
        
        nextToken = re.compile(tokenRegex).search
        token = nextToken(self.stream)
        while token is not None:
            typ = token.lastgroup
            value = token.group(typ)
            if typ == 'NEWLINE':
                lineStart = pos
                line += 1
            elif typ != 'NONTERMINAL' and typ != 'TERMINAL':
                pos = token.end()
                token = nextToken(self.stream, pos)
            elif typ != 'SKIP':
                # Fetch the token value ...
                value = token.group(typ)
                if typ == 'NONTERMINAL':
                    self.gram.add_nonterminal(value)
                elif typ == 'TEMRMINAL':
                    self.gram.add_terminal(value)
                yield self.Token(typ, value)
            
            pos = token.end()
            token = nextToken(self.stream, pos)
            
            
    def readFromFile(self):
        f = open('../bnf2')
        for line in f:
            self.stream += line
            
grammar = Grammar()
sc = Importer(grammar)
for token in sc.parse():
    print token
