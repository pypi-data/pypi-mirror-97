from random import choice


class CharAscii(object):
    def __init__(self):
        self.val = self.ascii()

    @staticmethod
    def _get_tables(table, a, b):
        for i in range(a, b):
            c = chr(i)
            table.append(c)
        return table
    
    def ascii(self, a=32, b=128):
        if a < 32:
            a = 32
        if b > 128:
            b = 128
        table = []
        table = self._get_tables(table, a, b)
        table.append('\n')
        self.val = table
        return table

    def num(self):
        table = []
        table = self._get_tables(table, 48, 58)
        self.val = table
        return table

    def lower(self, s=1):
        table = []
        table = self._get_tables(table, 97, 123)
        if s != 1:
            table.append(' ')
            table.append('\n')
        self.val = table
        return table

    def up(self, s=1):
        table = []
        table = self._get_tables(table, 65, 91)
        if s != 1:
            table.append(' ')
            table.append('\n')
        self.val = table
        return table

    def lower_up(self, s=1):
        table = self.lower(s)
        table += self.up()
        self.val = table
        return table

    def lower_up_num(self, s=1):
        table = self.lower_up(s)
        table += self.num()
        self.val = table
        return table

    def symbols(self):
        table = []
        table = self._get_tables(table, 32, 48)
        table += self.ascii(58, 65)
        table += self.ascii(91, 97)
        table += self.ascii(123, 128)
        self.val = table
        return table

    def as_str(self):
        self.val = "".join(self.val)
        return self.val


class WordGenerate(object):
    def __init__(self):
        self.__alf = CharAscii()
        self.__alf.val.remove(' ')
        self.__alf.val.remove('\n')
        self.__alf.val.remove('\x7f')
        self.val = 'CharQ'

    def _take(self, a, b, c):
        text = ''
        for i in range(0, a):
            text += choice(self.__alf.val[b:c])
        return text
        
    def _run(self, tam, typew):
        text = ''
        if typew == 0:
            text += self._take(tam, 64, 90)
        elif typew == 1:
            text += self._take(tam, 32, 58)
        elif typew == 2:
            text += choice(self.__alf.val[32:58])
            text += self._take((tam-1), 64, 90)
        elif typew == 3:
            text += self._take(tam, 15, 25)
        elif typew == 4:
            text += self._take(tam, 0, 94)
        self.val = text
        return text

    def word(self, tam=10, case='lower'):
        if case == 'lower':
            return self._run(tam, 0)
        elif case == 'up':
            return self._run(tam, 1)
        elif case == 'camel':
            return self._run(tam, 2)

    def num(self, tam=2, typen='int'):
        if typen == 'str':
            return self._run(tam, 3)
        elif typen == 'int':
            return int(self._run(tam, 3))

    def passw(self, tam=8):
        return self._run(tam, 4)

    def as_list(self):
        self.val = list(self.val)
        return self.val
