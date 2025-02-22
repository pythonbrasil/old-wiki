# Python 3 Patterns, Recipes and Idioms
#                           Release 1.0
#                           Bruce Eckel
#
# python-3-patterns-idioms/code/PythonDecorators/entry_exit_class.py

class entry_exit(object):

    def __init__(self, f):
        self.f = f

    def __call__(self):
        print("Entering", self.f.__name__)
        self.f()
        print("Exited", self.f.__name__)

@entry_exit
def func1():
    print("inside func1()")

@entry_exit
def func2():
    print("inside func2()")

func1()
func2()output = '''
('Entering', 'func1')
inside func1()
('Exited', 'func1')
('Entering', 'func2')
inside func2()
('Exited', 'func2')
'''
