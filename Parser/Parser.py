# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 20:07:54 2014

@author: dan
"""

from Grammar import Grammar

class Parser:
    ''' Parses sequences of symbols according to a context-free grammar ''''
    def __init__(self, repo):
        self.repo = repo