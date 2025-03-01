# Backup da Wiki Antiga

Backup da wiki antiga para guardar o historico.

A wiki rodava em MoinMoin com python 2.7

* A Pasta de usuarios foi removida para evitar vazamento de lista de hash de senhas

## Exportando Para Markdown

Foi adicionado no repositório um script (`moin2markdown.sh`) bash para exportar o conteúdo das páginas para markdown.

Para roda-lo é preciso ter o [pandoc](https://pandoc.org/installing.html) instalado no sistema.

Exemplo:

```shell
./moin2markdown.sh ListaDeExercicios moin exported
```

O primeiro parametro é o nome da pagina que pode ser encontrado em `moin/data/pages`.

O segundo parametro é o root do moin.

E o terceiro parametro é a pasta de destino.

Para mais informações o script original pode ser encontrado em https://github.com/phlash/moin2markdown
