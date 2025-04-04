#!/usr/bin/env python3
#
#  simpletable.py
#  
#  Copyright 2025 Nap0
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
# This module simpletable.py contains the following class definitions:
#  
# class SimpleTable
# -----------------
#   a class that generates a simple table with optional header, title 
#   and optionally specified column width.
#
#   Simpletable(*columns, **kwargs)  
#   
#   Positional arguments, optional:
#       columns: a number of iterables each containing a variable number of column items,
#                   the iterables can be lists, tuples or numpy ndarrays
#
#   Keyword arguments, optional: 
#       header: an iterable containing the headers above each column
#
#       title: a string which appears above the columns
#
#       columnwidth: the width to be used for each column, 
#           if omitted the length of the longest item is used
#
#   returns:
#       an SimpleTable object
#   
#   Instance methods:
#       set(**kwargs)
#           allows adding keyword arguments after the object is created
#
#       transpose()
#           modifies the table so that columns become rows including the header if it exists
#
#   Example:
#   
#   import simpletable as st
#   mytable = st.SimpleTable( 
#       ["CPU","RAM","Storage","screen","Disk OS","Prog. language","sound","colors"], 
#       ["Z80","1KB","Cassette","TV","","Sinclair basic","B/W"], 
#       ["Z80","48KB","Cassette","TV","","Sinclair basic","beeps","16 colors?"],
#       ["Z80","128KB","3.5\" floppy","Monitor","MSX-DOS","MSX-BASIC","soundchip","256 colors"],
#       header = ["", "ZX-81", "ZX-Spectrum", "MSX2"],
#       )
#   mytable.set(columnwidth=14, title="Computers of the past")
#   print(mytable)
#   mytable.transpose()
#   print(mytable)
#
#

from itertools import zip_longest

class SimpleTable:
    
    # special characters to be used
    hor_char = "-"
    ver_char = "|"
       
           
    # instance initialisation method
    def __init__(self, *columns, **kwargs):
        self.title = None
        self.header = None
        self.columns = []
        self.rows = None
        self.columnwidth = None
        self.auto_columnwidth = None
        
        # colums are positional arguments
        for column in columns:
            if isinstance(column, (tuple, list, set)):
                self.columns.append(list(column))
            else:
                try:
                    iter(column)
                except TypeError:
                    raise TypeError("column must be iterable")
                else:
                    self.columns.append(list(column))
                
        # other settings are keyword arguments
        self.__parse_keyword_arguments(kwargs)
        
        # if the columnwidth is not given, automatically determine it                        
        if self.columnwidth is None:
            self.__automatic_columnwidth()
            
       
    # returns a representation of the function call        
    def __repr__(self):
        table_repr = f"SimpleTable("
        for column in self.columns:
            if column is not None:
                table_repr += f"{column},"
        if self.header is not None:
            table_repr += f"header = {self.header},"
        if self.title is not None:
            table_repr += f"title = '{self.title}',"
        if self.columnwidth is not None:
            table_repr += f"columnwidth = {self.columnwidth}"
        table_repr += ")"
        return(table_repr)
            
       
    # returns table as one string, is called for example by print() function
    def __str__(self):
        # if the columnwidth is not given, automatically determine it                        
        if self.columnwidth is None:
            self.__automatic_columnwidth()
            cw = self.auto_columnwidth
        else:
            cw = self.columnwidth 
        tablewidth = self._get_table_width()
        # generate horizontal line of correct length
        line_str = SimpleTable.hor_char * tablewidth
        table_str = ""  
        # first the title if one exists  
        if self.title is not None:
            table_str += f"{line_str}\n"
            table_str += f"{self.title:^{(tablewidth - 1)}}{SimpleTable.ver_char}\n"
        # then the header if one exists    
        if self.header is not None:
            header_str = ""
            for header_item in self.header:
                header_str += f"{str(header_item):>{cw}s}{SimpleTable.ver_char}"
            table_str += f"{line_str}\n{header_str}\n" 
        table_str += f"{line_str}\n"
        # the columns    
        if self.columns is not None:
            rows = list( zip_longest( *self.columns , fillvalue="") ) 
            for row in rows:
                for row_item in row:
                    table_str += f"{str(row_item):>{cw}s}{SimpleTable.ver_char}"
                table_str +="\n"
        table_str += f"{line_str}\n"
        return table_str
        
    
    # dunder method for calling len(), returns number of items in longest column plus header
    def __len__(self):
        max_len = 0
        for column in self.columns:
            if len(column) > max_len:
                max_len = len(column)
        if self.header is not None: max_len += 1
        return(max_len)
        
        
    # dunder method for == operator    
    def __eq__(self, y):
        equal = (self.columns == y.columns) and (self.header == y.header) \
            and (self.title == y.title) and (self.columnwidth == self.columnwidth)
        return(equal)
        
        
    # instance method to determine table width
    def _get_table_width(self):
        table_width_title = 0
        if self.title is not None:
            table_width_title = len(self.title) + 2
        table_width_header = 0
        if self.header is not None:
            for header_item in self.header:
                if self.columnwidth  is None:
                    table_width_header += len(str(header_item)) + 1
                else:
                    table_width_header += self.columnwidth  + 1
        table_width_columns = 0
        if self.columns != []:
            if self.columnwidth  is None:
                self.__automatic_columnwidth()
                table_width_columns = (self.auto_columnwidth + 1) * len(self.columns)
            else:
                table_width_columns = (self.columnwidth + 1) * len(self.columns)
            

        table_width = table_width_header if table_width_header > table_width_columns else table_width_columns
        if table_width_title > table_width: table_width = table_width_title
        return(table_width)
                

    
    
    # instance method to parse keyword arguments
    def __parse_keyword_arguments(self, kwargs):
        for arg_name in kwargs:
            match arg_name:
                case "title":
                    self.title = kwargs.get("title")
                    if not isinstance(self.title, str):
                        raise TypeError("title must be of type string")
                case "header":
                    self.header = kwargs.get("header")
                    if not isinstance(self.header, (tuple, list, set)):
                        raise TypeError("header must be of type tuple, list or set")
                case "columnwidth":
                    self.columnwidth = kwargs.get("columnwidth")
                    if not isinstance(self.columnwidth, int):
                        raise TypeError("columnwidth must be of type int")
        
                    
    # instance method to set columnwidth to widest element, used if columnwidth was not specified        
    def __automatic_columnwidth(self):
        widest_item = 0
        if self.header is not None:
            for item in self.header:
                if len(str(item)) > widest_item:
                    widest_item = len(str(item)) 
        for column in self.columns:
            for item in column:
                if len(str(item)) > widest_item:
                    widest_item = len(str(item)) 
        self.auto_columnwidth = widest_item
        
    
    # transpose the complete table, columns become rows   
    def transpose(self):
        if self.header is None:
            self.columns = list( zip_longest( *self.columns , fillvalue="") )
        else:
            for index, item in enumerate(self.header):
                if index < len(self.columns):
                    self.columns[index].insert(0, item)
                else:
                    self.columns.append([item])                   
            self.columns = list( zip_longest( *self.columns , fillvalue="") )
            self.header = []
            for column in self.columns:
                self.header.append(column[0])
            for index,column in enumerate(self.columns):
                self.columns[index] = list(column[1:])
                
                
    # Allows adding keyword arguments after the object is created           
    def set(self, **kwargs):
        self.__parse_keyword_arguments(kwargs)

     
     
     
# test code, if this file is running as main           

if __name__ == "__main__":
    table_classes = SimpleTable(
        ("__init__()","__repr__()","__len__()","__eq__()","__str__()","set()","transpose()"),
        ("Initialise with arguments"," returns SimpleTable call","length of table","is content equal?","returns table as string","columns become rows","modify keyword args. of existing object"),
        ("( *columns, **kwargs)","","(other SimpleTable object)","","(**kwargs)"),
        header = ("Method","Purpose","Arguments")
        )
    table_classes.set(title = "Methods of the class SimpleTable", columnwidth = 40)
    print(table_classes)
    
    table_kwargs = SimpleTable(
        ("positional","keyword","keyword","keyword"),
        ("","header","title","columnwidth"),
        ("iterable(s) = columns","text at top of columns","text at top of table","width of columns")
        )
    table_kwargs.set(header = ("kind of arguments","keyword","function"))  
    table_kwargs.set(title = "Arguments of SimpleTable")  
    print(table_kwargs)
    
    import simpletable as st
    mytable = st.SimpleTable( 
       ["CPU","RAM","Storage","screen","Disk OS","Prog. language","sound","colors"], 
       ["Z80","1KB","Cassette","TV","","Sinclair basic","B/W"], 
       ["Z80","48KB","Cassette","TV","","Sinclair basic","beeps","16 colors?"],
       ["Z80","128KB","3.5\" floppy","Monitor","MSX-DOS","MSX-BASIC","soundchip","256 colors"],
       header = ["", "ZX-81", "ZX-Spectrum", "MSX2"],
       )
    mytable.set(columnwidth=14, title="Computers of the past")
    print(mytable)
    mytable.transpose()
    print(mytable)
    
    

    
    
    

