#!/usr/bin/env python
    
def meu_decorador(funcao):
    def funcao_retorno(*args,**kwargs):
        print( 'Entrou no decorador, funcao retorno')
        print(args)
        print(kwargs)
        funcao(*args)
        print('Saindo do decorador, funcao retorno')
    return funcao_retorno

@meu_decorador
def teste(numero):
    print(numero)
    
teste(10)

def meu_decorador_com_argumentos(texto):
    def decorador_interno(funcao):
        print('Entrada do decorador, decorador com argumentos')
        def funcao_retorno(*args,**kwargs):
            print('Entrada do decorador, funcao retorno')
            print(args)
            print(kwargs)
            funcao(*args)
            print('Saindo do decorador, funcao retorno - ',texto)
        return funcao_retorno

    print('Saindo do decorador, decorador com argumentos')
    return decorador_interno

@meu_decorador_com_argumentos('teste')
def teste(numero):
    print(numero)
    
teste(1)
