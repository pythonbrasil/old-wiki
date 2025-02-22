#!/usr/bin/env python

class Calculadora():
    def soma(self,a,b):
        ''' Soma os valores a e b.
        >>> calc = Calculadora()
        >>> calc.soma(2,2)
        4
        '''
        return a+b

    def subtracao(self,a,b):
        ''' Subtrai os valores a e b.
        >>> calc = Calculadora()
        >>> calc.subtracao(4,2)
        2
        '''
        return a-b

if __name__ == '__main__':
    import doctest
    doctest.testmod()

