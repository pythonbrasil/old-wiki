from WebKit.Page import Page

class Main(Page):
    def writeContent(self, msg=''):
        fruits = self.session().value('fruits', [])
        
        self.writeln('<h1>Cesta de Frutas</h1>')
        
        if fruits:
            self.writeln('Disponível na cesta:<ul>')
            for fruit in fruits:
                self.writeln('<li>' + fruit)
            self.writeln('</ul>')
        
        self.writeln('''
        <form action="Main" method="POST">
        <table>
        <tr>
          <td><input type="submit" name="_action_add" value="Adicionar">
          <td><input type="text" name="new_fruit">
        <tr>
          <td><input type="submit" name="_action_remove" value="Remover">
          <td><input type="text" name="remove_fruit">
        <tr>
          <td><input type="submit" name="_action_clear" value="Limpar"
          <td>
        </table>
        </form>
        ''')
        
        if msg:
            self.writeln('<small>Resultado da última operação: %s</small>'
                         % msg)

    def actions(self):
        return Page.actions(self) + ['add', 'remove', 'clear']

    def add(self):
        fruits = self.session().value('fruits', [])
        new_fruit = self.request().field('new_fruit')
        if not new_fruit in fruits:
            fruits.append(new_fruit)
            self.session().setValue('fruits', fruits)
            msg = 'Adicionei a fruta na cesta.'
        else:
            msg = 'A fruta já está na cesta.'
        self.writeContent(msg)

    def remove(self):
        fruits = self.session().value('fruits', [])
        rm_fruit = self.request().field('remove_fruit')
        if rm_fruit in fruits:
            fruits.remove(rm_fruit)
            self.session().setValue('fruits', fruits)
            msg = 'A fruta foi removida.'
        else:
            msg = 'A fruta não estava na cesta.'
        self.writeContent(msg)

    def clear(self):
        if self.session().hasValue('fruits'):
            self.session().delValue('fruits')
        self.writeContent('A cesta foi limpa.')
        
