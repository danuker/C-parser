'''
Created on Jan 4, 2014

@author: Drone
'''
import collections
import re
import sys

from Grammar import Grammar


class Importer:
    '''
    scans the grammar from the doc and gets terminals/non-terminals
    '''
    terminals = []
    nonterminals = []
    stream = ""
    Token = collections.namedtuple('Token', ['type', 'value'])
    def __init__(self, gram):
        self.gram = gram
        self.readFromFile()
        
    def parse(self):
        pos = 0
             
        line = 1
        tokenSpec = [
        ('NONTERMINAL', r'<[a-z_|A-Z_]+>'),
        ('TERMINAL', r'(?<=\n\d\n).+|(?<=\n\d\d\n).+|(?<=\")[a-z|A-Z]+(?=\")|(?<=\")[^\"\ \||.]{1,2}(?=\")'),
        ('SKIP', r'[ \t]')
        ]
        tokenRegex = '|'.join('(?P<%s>%s)' % pair for pair in tokenSpec)
        
        nextToken = re.compile(tokenRegex).search
        token = nextToken(self.stream)
        while token is not None:
            typ = token.lastgroup
            value = token.group(typ)
            if typ == 'NEWLINE':
                line += 1
            elif typ != 'NONTERMINAL' and typ != 'TERMINAL':
                pos = token.end()
                token = nextToken(self.stream, pos)
            elif typ != 'SKIP':
                # Fetch the token value ...
                value = token.group(typ)
                if typ == 'NONTERMINAL' and value not in self.nonterminals and value not in self.terminals:
                    self.nonterminals.append(value)
                    self.gram.add_nonterminal(value)
                elif typ == 'TERMINAL' and value not in self.terminals and value not in self.nonterminals:
                    self.terminals.append(value)
                    self.gram.add_terminal(value)
                yield self.Token(typ, value)
            
            pos = token.end()
            token = nextToken(self.stream, pos)
    
    def readProductions(self):
        pos = 0
             
        line = 1
        tokenSpec = [
        ('PRODUCTION', r'<.+>(?=::=)'),
        ('NONTERMINAL', r'<[a-z_|A-Z_]+>'),
        ('TERMINAL', r'(?<=\n\d\n).+|(?<=\n\d\d\n).+|(?<=\")[a-z|A-Z]+(?=\")|(?<=\")[^\"\ \||.]{1,2}(?=\")'),
        ('SKIP', r'[ \t]')
        ]
        tokenRegex = '|'.join('(?P<%s>%s)' % pair for pair in tokenSpec)
        
        nextToken = re.compile(tokenRegex).search
        token = nextToken(self.stream)
        while token is not None:
            typ = token.lastgroup
            value = token.group(typ)
            if typ == 'NEWLINE':
                line += 1
            elif typ != 'NONTERMINAL' and typ != 'TERMINAL' and typ != 'PRODUCTION':
                pos = token.end()
                token = nextToken(self.stream, pos)
            elif typ != 'SKIP':
                # Fetch the token value ...
                value = token.group(typ)
                if typ == 'PRODUCTION':
                    start = value
                    sequence = []
                    pos = token.end()
                    token = nextToken(self.stream, pos)
                    typ = token.lastgroup
                    value = token.group(typ)
                    while typ != 'PRODUCTION' and typ != '':
                        if typ != 'SKIP':
                            sequence.append(value)
                            pos = token.end()
                            token = nextToken(self.stream, pos)
                            if token is None:
                                sequence = tuple(sequence)
                                print "START: " + start + "\nSequence:"
                                for elem in sequence:
                                    sys.stdout.write(elem + ',')
                                print "\n"
                                self.gram.add_production(start, sequence)
                                break
                            typ = token.lastgroup
                            value = token.group(typ)
                        else:
                            pos = token.end()
                            token = nextToken(self.stream, pos)
                            typ = token.lastgroup
                            value = token.group(typ)
                    sequence = tuple(sequence)
                    print "START: " + start + "\nSequence:"
                    for elem in sequence:
                        sys.stdout.write(elem + ',')
                    print "\n"
                    self.gram.add_production(start, sequence)
            
            
    def readFromFile(self):
        f = open('../bnf2')
        for line in f:
            self.stream += line
            
grammar = Grammar()
sc = Importer(grammar)
for token in sc.parse():
    print token
    
print "\n\n"
sc.readProductions()

