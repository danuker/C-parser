'''
Created on Oct 27, 2013

@author: Zehel
'''

class Token:
    '''
    classdocs
    '''


    def __init__(self, tkType, value, line, column, code):
        '''
        Constructor
        '''
        self.tkType = tkType
        self.value = value
        self.line = line
        self.column = column
        self.code = code

    def get_code(self):
        return self.code


    def set_code(self, value):
        self.code = value


    def del_code(self):
        del self.code


    def get_tk_type(self):
        return self.tkType


    def get_value(self):
        return self.value


    def get_line(self):
        return self.line


    def get_column(self):
        return self.column


    def set_tk_type(self, value):
        self.tkType = value


    def set_value(self, value):
        self.value = value


    def set_line(self, value):
        self.line = value


    def set_column(self, value):
        self.column = value


    def del_tk_type(self):
        del self.tkType


    def del_value(self):
        del self.value


    def del_line(self):
        del self.line


    def del_column(self):
        del self.column

    tkType = property(get_tk_type, set_tk_type, del_tk_type, "tkType's docstring")
    value = property(get_value, set_value, del_value, "value's docstring")
    line = property(get_line, set_line, del_line, "line's docstring")
    column = property(get_column, set_column, del_column, "column's docstring")
    code = property(get_code, set_code, del_code, "code's docstring")
        
