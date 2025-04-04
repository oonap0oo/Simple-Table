# This module simpletable.py contains the following class definitions:

## class SimpleTable

a class that generates a simple table with optional header, title 
and optionally specified column width.

### Simpletable(*columns, **kwargs)  

### Positional arguments, optional:
columns: a number of iterables each containing a variable number of column items,
the iterables can be lists, tuples or numpy ndarrays

### Keyword arguments, optional: 
#### header: 
an iterable containing the headers above each column

#### title: 
a string which appears above the columns

#### columnwidth: 
the width to be used for each column, 
if omitted the length of the longest item is used

### returns:
an SimpleTable object

### Instance methods:
#### set(**kwargs)
allows adding keyword arguments after the object is created

#### transpose()
modifies the table so that columns become rows including the header if it exists

### Example:
```
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
```
