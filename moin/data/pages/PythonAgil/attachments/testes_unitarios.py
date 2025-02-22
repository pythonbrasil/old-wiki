#!/usr/bin/env python

import unittest

class TestExemplo(unittest.TestCase):
    def setUp(self):
        self.calculadora=Calculadora()

    def testSoma(self):
        calc = self.calculadora
        self.assertEqual(calc.soma(2,2),4)

    def testSubtracao(self):    
        calc = self.calculadora
        self.assertEqual(calc.subtracao(4,2),2)

class Calculadora():
    def soma(self,a,b):
        return a+b

    def subtracao(self,a,b):
        return a-b

if __name__ == '__main__':
    unittest.main()

