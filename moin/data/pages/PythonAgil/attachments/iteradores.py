#!/usr/bin/env python
# http://docs.python.org/tutorial/classes.html#iterators

s = 'abc'
it = iter(s)
it.next()
it.next()
it.next()
it.next()

class Reverse:
    "Iterator for looping over a sequence backwards"
    def __init__(self, data):
        self.data = data
        self.index = len(data)
    def __iter__(self):
        return self
    def next(self):
        if self.index == 0:
            raise StopIteration
        self.index = self.index - 1
        return self.data[self.index]

rev = Reverse('spam')
for char in rev:
    print char

