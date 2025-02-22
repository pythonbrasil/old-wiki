#!/usr/bin/env python
  
tabelas = [{'nome':'tabela_cliente','campos':[('id','serial'),('nome','varchar(100)')]},
           {'nome':'tabela_fornecedor','campos':[('id','serial'),('nome','varchar(100)'),('fone','varchar(20)')]}]

create_table_template = '''CREATE TABLE %(nome)s (%(estrutura)s);'''
estrutura_template = '''%s %s'''

lista = [{'nome':x['nome'],'estrutura': ','.join([estrutura_template % y for y in x['campos']])} for x in tabelas]

for i in lista:
    print(create_table_template % i)
    
