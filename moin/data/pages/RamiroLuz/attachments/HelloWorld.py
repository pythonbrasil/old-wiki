#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# Exemplos retirados do artigo: Python Cheat Sheet
# http://www.yukoncollege.yk.ca/~ttopper/COMP118/rCheatSheet.html
print "s = \"Hello World!\""
s = "Hello World!"
print "suffix = \".py\""
suffix = ".py"
print "prefix = \"py_\""
prefix = "py_"
print "substring = \"lo\""
substring = "lo"
print "chars = \"H\""
chars = "H"
print "list = []"
list = []

# Testing string contents:
print ">>> print \"Hello World!\".isalnum()"
print "Hello World!".isalnum()
print ">>> print \"Hello World!\".isalpha()"
print "Hello World!".isalpha()
print ">>> print \"Hello World!\".isdigit()"
print "Hello World!".isdigit()
print ">>> print \"Hello World!\".isspace()"
print "Hello World!".isspace()
print ">>> print \"Hello World!\".islower()"
print "Hello World!".islower()
print ">>> print \"Hello World!\".isupper()"
print "Hello World!".isupper()
print ">>> print \"Hello World!\".istitle()"
print "Hello World!".istitle()
print ">>> print \"Hello World!\".endswith( suffix )"
print "Hello World!".endswith( suffix )
print ">>> print \"Hello World!\".startswith( prefix )"
print "Hello World!".startswith( prefix ) 

# Finding things in strings:
print ">>> print \"Hello World!\".count( substring )"
print "Hello World!".count( substring )
print ">>> print \"Hello World!\".find( substring )"
print "Hello World!".find( substring )
print ">>> print \"Hello World!\".index( substring )"
print "Hello World!".index( substring )
print ">>> print \"Hello World!\".rfind( substring )"
print "Hello World!".rfind( substring )
print ">>> print \"Hello World!\".rindex( substring )"
print "Hello World!".rindex( substring )

# Changing stringprint s. Remember that strings are immutable so to make a change "stick" you have to do, e.g. s = print s.title().
print ">>> print \"Hello World!\".swapcase()"
print "Hello World!".swapcase()
print ">>> print \"Hello World!\".upper()"
print "Hello World!".upper()
print ">>> print \"Hello World!\".lower()"
print "Hello World!".lower()
print ">>> print \"Hello World!\".title()"
print "Hello World!".title()
print ">>> print \"Hello World!\".capitalize()"
print "Hello World!".capitalize()
print ">>> print \"Hello World!\".center(30)"
print "Hello World!".center(30)
print ">>> print \"Hello World!\".ljust(10)"
print "Hello World!".ljust(10)
print ">>> print \"Hello World!\".rjust(15)"
print "Hello World!".rjust(15)
print ">>> print \"Hello World!\".strip()"
print "Hello World!".strip()
print ">>> print \"Hello World!\".lstrip( chars )"
print "Hello World!".lstrip( chars )
print ">>> print \"Hello World!\".rstrip( chars )" 
print "Hello World!".rstrip( chars ) 
# Mudança didatica.
chars = "Hel"
print ">>> print \"Hello World!\".lstrip( chars )"
print "Hello World!".lstrip( chars )
print ">>> print \"Hello World!\".rstrip( chars )" 
print "Hello World!".rstrip( chars ) 
# Nova mudança didatica.
chars = "ld!"
print ">>> print \"Hello World!\".lstrip( chars )"
print "Hello World!".lstrip( chars )
print ">>> print \"Hello World!\".rstrip( chars )" 
print "Hello World!".rstrip( chars ) 

# String to list:

print ">>> list = \"Hello World!\".split()"
print ">>> print list"
list = "Hello World!".split() 
print list

# List to string:
print ">>> print s.join( list ) # where s is the string to join the elements of list with."
print s.join( list ) # where s is the string to join the elements of list with. 
