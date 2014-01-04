# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 19:57:34 2014

@author: dan
"""

from Scanner.Run import Repository
from Parser.Parser import Parser

if __name__=='__main__':
    r = Repository('sample.cpp')
    p = Parser(r)