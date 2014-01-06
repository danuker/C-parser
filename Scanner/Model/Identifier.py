'''
Created on Oct 28, 2013

@author: Zehel
'''

class Identifier:
    '''
    classdocs
    '''
    

    def __init__(self, dataType, name, line, column):
        '''
        Constructor
        '''
        self.dataType = dataType
        self.name = name
        self.line = line
        self.column = column

    def get_data_type(self):
        return self.dataType


    def get_name(self):
        return self.name


    def get_line(self):
        return self.line


    def get_column(self):
        return self.column


    def set_data_type(self, value):
        self.dataType = value


    def set_name(self, value):
        self.name = value


    def set_line(self, value):
        self.line = value


    def set_column(self, value):
        self.column = value


    def del_data_type(self):
        del self.dataType


    def del_name(self):
        del self.name


    def del_line(self):
        del self.line


    def del_column(self):
        del self.column

    dataType = property(get_data_type, set_data_type, del_data_type, "dataType's docstring")
    name = property(get_name, set_name, del_name, "name's docstring")
    line = property(get_line, set_line, del_line, "line's docstring")
    column = property(get_column, set_column, del_column, "column's docstring")
        
