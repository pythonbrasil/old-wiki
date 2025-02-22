#!/usr/bin/env python
# http://docs.python.org/tutorial/classes.html#generators

def reverse(data):
    for index in range(len(data)-1, -1, -1):
        yield data[index]

for char in reverse('golf'):
    print char

# ** Atenção esse exemplo é apenas didático.
# ** Para inverter uma string há uma maneira mais
# ** simples:
# print 'golf'[::-1]
