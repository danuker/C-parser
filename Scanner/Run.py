'''
Created on Oct 27, 2013

@author: Zehel
'''
from Repository.Repository import Repository
if __name__ == '__main__':
    rep = Repository("../sample.cpp")
    
    for token in rep.tokenize():
        print token
