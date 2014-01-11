'''
Created on Oct 27, 2013

@author: Zehel
'''
#!/usr/bin/python
from Model.Token import Token
from Model.Identifier import Identifier
import collections
import re
import sys
class Repository:
    '''
    classdocs
    '''
    stream = ""
#    Variable = collections.namedtuple('VariableDeclaration', ['datatype', 'name', 'line', 'column', 'code'])
    Token = collections.namedtuple('Token', ['type', 'value', 'line', 'column', 'code'])
    identifiers = {}
    tokens = {}
    tokensWithCodes = {}
    tokenCode = 0
    identifierCode = 0
    tokenSpec = [
        # Relation operators
        ('RELATION', r'[<|<=|==|=>|>|\!=]{1,2}'),
        # Arithmetic operators
        ('OPERATOR', r'[\+=|\-=]{2}|(?<![\+\-\^\*\/%])[\+\-]|[\^\*/%!]'),
        # Function identifiers
        ('FUNCTIONID', r'[a-zA-Z_][a-zA-Z0-9_]*(?=([ \t]+)?\()'),
        # Variable identifiers
        ('VARIABLEID', r'[+-]?[a-zA-Z_][a-zA-Z0-9_]{0,7}(?=\W)(?!([ \t]+)?\()'),
        # Any numeric value (decimal or floating point)
        ('NUMBER', r'0(?=\D)|[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?'),
        # Left brace
        ('LBRACE', r'[(]'),
        # Right brace
        ('RBRACE', r'[)]'),
        # Left curly brace
        ('LCURL', r'[{]'),
        # Right curly brace
        ('RCURL', r'[}]'),
        # Assignment operator
        ('ASSIGN', r'='),
        # End line operator
        ('END', r';'),
        # Line endings
        ('NEWLINE', r'\n'),
        # Skip over spaces and tabs
        ('SKIP', r'[ \t]'),
        ('QUOTE', r'[\"]{1}[+-]?[a-zA-Z_][a-zA-Z0-9_]{0,7}(?=\W)(?!([ \t]+)?\()[\"\']{1}'),
        ('APOSTROPHE', r'[\']{1}[a-zA-Z_]{1}[\']{1}')
    ]
 
    tokenRegex = '|'.join('(?P<%s>%s)' % pair for pair in tokenSpec)
    keywords = {
        '+': 'PLUS', '-': 'MINUS', '*': 'TIMES', '/': 'DIV',
        '^': 'EXP', '%': 'MOD', '!': 'FAC'
    }
    dataTypes = ['bool', 'char', 'int', 'string', 'real', 'void']

    def __init__(self, fileName):
        '''
        Constructor
        '''
        self.readFromFile(fileName)
        self.loadTokenCodesFromFile()
        self.identifierCode = len(self.tokensWithCodes)
        
    def tokenize(self):
        nextToken = re.compile(self.tokenRegex).match
        # Setup the line start and current position ...
        pos = lineStart = 0
             
        # ... as well as the current line.
        line = 1
             
        # Fetch the first token ...
        token = nextToken(self.stream)
        f = open("ST", 'w')     
        # ... and start the processing.
        while token is not None:
            # Fetch the token type ...
            typ = token.lastgroup
            # ... and increment line counter if it is a newline.
            if typ == 'NEWLINE':
                lineStart = pos
                line += 1
            elif typ != 'SKIP':
                # Fetch the token value ...
                value = token.group(typ)
                # ... and handle keywords.
                if typ == 'OPERATOR' and value in self.keywords.keys():
                    typ = 'OPERATOR'
                elif typ == 'VARIABLEID' and value in self.dataTypes:
                    typ = 'DATATYPE'
#                    dataT = token.group()
#                    pos = token.end()
#                    token = nextToken(self.stream, pos)
#                    while token is not None:
#                        typ = token.lastgroup
#                        if typ == 'NEWLINE':
#                            lineStart = pos
#                            line += 1
#                        elif typ != 'SKIP':
#                            # Fetch the token value ...
#                            value = token.group(typ)
#                            if typ == 'VARIABLEID' and value not in self.dataTypes:
#                                vname = value
#                                if (len(vname) > 8):
#                                    raise Exception('Variable %s on line %d exceeds 8 characters.' % (value, line))
#                                var = Variable(dataT, vname, line, token.start() - lineStart)
#                                self.variables[self.variableCode] = var
#                                self.variableCode += 1
#                                yield self.VariableDeclaration(dataT, vname, line, token.start() - lineStart)
#                            elif typ == 'END':
#                                pos = token.end()
#                                token = nextToken(self.stream, pos)
#                                break  
#                        pos = token.end()
#                        token = nextToken(self.stream, pos)
                code = 0
                
                for elem in self.tokensWithCodes:
                    if (self.tokensWithCodes[elem].strip() == value):
                        code = elem
                        
                if(code == 0 and value not in self.identifiers and typ != 'NUMBER'):
                    savestr = "{0:13} code:{1}\n".format(value, self.identifierCode)
                    f.write(savestr)
                    self.identifiers[value] = self.identifierCode
                    code = self.identifierCode
                    self.identifierCode += 1
                elif(code == 0 and value not in self.identifiers and typ == 'NUMBER'):
                    code = 1
                elif(code == 0 and value in self.identifiers and typ != 'NUMBER'):
                    code = self.identifiers[value]
                    
                    
                tk = Token(typ, value, line, token.start() - lineStart, code)
                self.tokens[self.tokenCode] = tk
                self.tokenCode += 1  
                yield self.Token(typ, value, line, token.start() - lineStart, code)
                
            pos = token.end()
            token = nextToken(self.stream, pos)
        if pos != len(self.stream):
            raise Exception('Unexpected character %r on line %d' % (self.stream[pos], line))
        f.close()
        f = open("PIF", 'w')
        for token in self.tokens:
            savestr = "{0:4}:  Type: {1:13} Value: {2:10} Line: {3:4} Column: {4:4} Code: {5:4}\n".format(str(token), self.tokens[token].get_tk_type(), self.tokens[token].get_value(), str(self.tokens[token].get_line()), str(self.tokens[token].get_column()), str(self.tokens[token].get_code()))
            f.write(savestr)
        f.close()
        
    def readFromFile(self, fileName):
        f = open(fileName)
        for line in f:
            self.stream += line
            
    def loadTokenCodesFromFile(self):
        f = open("../Scanner/tokenCodes")
        i = 0
        for line in f:
            self.tokensWithCodes[i] = line
            i += 1
        
            
