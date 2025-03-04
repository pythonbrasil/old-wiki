#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import socket
from urllib import urlopen
import re

class magic_velox:
    """Estabelecer uma conexao automatica com o Velox.
    
    os atributos velox, comercial, provedor, login, senha devem
    ser alterados para a necessidade de cada pessoa
    Para vc saber qual valor utilizar para os atributos comercial e provedor,
    a configuracao e simples, a variavel "velox" recebe o valor 'r' para residencial
    e 'c' para comercial, se o "velox" for 'comercial', a variavel "comercial"
    devera ser alterada para o seu tipo de velox comercial, se o "velox" for 
    'residencial' a variavel "provedor" devera receber o valor de seu provedor,
    para saber qual seu provedor, execute "#python magic-velox.py -l" na linha
    de comando ou consulte o codigo fonte da pagina de autenticacao do velox
    Para facilitar, estou postando alguns valores possiveis para a variavel "provedor"

    'SUPERIG3'    
    'GLOBO'
    'GLOBO3'
    'GLOBO6'
    """
    
    def __init__(self,debug=1):
        
        self.velox = 'r' #Alterar: define o tipo do velox
                         #pode ser 'r' para residencial
                         #ou 'c' para comercial
                         
        self.comercial='AARJ' #Alterar: caso velox igual a 'c' (preciso de mais testes)
        
        self.provedor ='SUPERIG' #Altear: caso velox igual a 'r'
        
        self.login = 'seu_login' #Alterar: Login no Provedor
        
        self.senha = 'sua_senha' #Alterar: Senha no Provedor
        
        #Nao alterar mais nada, configurar somente ate aqui!
        self.url = self.post = self.data = ''
        self.objSock = None
        self.servidor = 'www.veloxzone.com.br'
        self.url_lst_servidor = 'http://www.veloxzone.com.br/user/pages/serviceList.jsp'
        self.porta = 80
        self.res_url='/vfile/pages/serviceLogon.jsp'
        self.res_post='service=internet_%s&fcn=serviceLogon&ac=home&usr=&username=%s&password=%s&OK=OK' % (self.provedor,self.login,self.senha)
        self.com_url='/serviceStart?service=internet_%s' % (self.comercial)
        self.com_post='confirmed=true'
        self.debug = debug

    def autentica(self):
        """Efetua a autenticacao com o Velox."""
      
        print '----------------------------------------------------------'
        print '************  Autenticacao Automatica do Velox ***********'
        print '----------------------------------------------------------'
        print '            magic-velox.py v1.0.0 [05/05/2005]            '
        print '     Marcel Portela, marcel{.}portela(a)gmail{.}com       '
        print '----------------------------------------------------------'
        if (self.velox=='r'):
            if self.debug:
                print ' - Modo Residencial'
                print ' - Provedor: %s' % (self.provedor)
                print ' - Login: %s' % (self.login)
            self.url=self.res_url
            self.post=self.res_post
        elif (self.velox=='c'): #necessito de mais testes neste tipo de conexao
            if self.debug:
                print ' - Modo Comercial'
                print ' - Regiao : %s' % (self.comercial)
            self.url=self.com_url
            self.post=self.com_post
        else:
            if self.debug:
              print '  **  ERRO DE ATRIBUTO - variavel velox devera ser \'r\' ou \'c\'  **'
        if (self.url != ''):
            try:
                self.objSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.objSock.connect((self.servidor, self.porta))
                self.objSock.send('POST %s HTTP/1.0\r\n'% (self.url))
                self.objSock.send('Content-Type: application/x-www-form-urlencoded\r\n')
                self.objSock.send('Host: %s\r\n' % (self.servidor))
                self.objSock.send('Content-Length: %s\r\n'% (len(self.post))) 
                self.objSock.send('\r\n%s\r\n\r\n\r\n'% (self.post)) 
                self.data = self.objSock.recv(1024)
                self.objSock.close()
                self.objSock = None
                
                if (self.data.find('veloxzone.com.br/home') > 0) : #confirma conexao
                    return 1
                else:
                    return -1
                    
            except Exception,e:
                if self.debug:
                    print '  **  ERRO - Servidor inacessivel - verifique sua rede e/o edite este script!'
                    print e
                try: #certifica-se que servidor foi desconectado
                    self.objSock.close()
                except Exception,e:
                    pass
                self.objSock = None
                return -1
        else:
            return -1

    def retorna_servidores(self):
        """Retorna a lista dos servidores do Velox.

        o velox deve estar desconectado para este metodo funcionar!
        """
        str_source = ''
        lista_achados = []
        padrao = re.compile("<option value='/.*internet_(.*)'",re.M|re.I)
        try:
            pagina = urlopen(self.url_lst_servidor)
            str_source = pagina.read()
        except Exception, e:
            if self.debug:
                print '  **  ERRO - Falha ao obter lista de servidores, verifique sua conexao com a internet!  **'

        if (str_source != ''):#se recebeu a pagina dos servidores 
            lista_achados = padrao.findall(str_source)
            if ((lista_achados == []) and (self.debug)):
                if (str_source.find('Desconectar') > 0):
                    print '  ** ERRO - Para obter a lista dos servidores o velox nao pode estar conectado! **'
                else:
                    #print str_source
                    print '  ** ERRO - Padrao nao encontrado  **'

        return lista_achados

def print_uso():
    print "Erro, opcao invalida, para brincar:"
    print "$ python magic-velox.py -c --> (Conectar Velox)"
    print "$ python magic-velox.py -l --> (Listar Servidores - o velox deve estar desconectado)"

def main():
    conectorVelox = magic_velox()
    if (len(sys.argv) == 2):
        if (sys.argv[1] == '-l'):
            for i in conectorVelox.retorna_servidores():
                print i
        elif (sys.argv[1] == '-c'):
            if (conectorVelox.autentica()==1):
                print '  --=(  Velox conectado!  )=--'
            else:
                print '  **  Problema conectando velox!  **'
        else:
            print_uso()
    else:
        print_uso()
    conectorVelox = None
    sys.exit(0)

if (__name__=='__main__'):
    main()
