class MyLibCalculadora(object):

    def __init__(self):
        self._result = None

    def some(self, a, b):
        self._result = float(a) + float(b)
        print(f'Operando a soma dos valores de {a} e ${b}')

    def multiplique(self, a, b):
        self._result = float(a) * float(b)
        print(f'Operando a multiplicação dos valores de {a} por ${b}')

    def o_resultado_deve_ser(self, esperado):
        if self._result != float(esperado):
            raise AssertionError(f'O resultado da operação {self._result} é diferente do esperado: {esperado}')
        print(f'O resultado da operação {self._result} é o esperado: {esperado}')

    def o_resultado_nao_deve_ser(self, valor):
        if self._result == float(valor):
            raise AssertionError(f'O resultado da operação {self._result} deve ser diferente do valor: {valor}')
        print(f'O resultado da operação {self._result} é diferente do valor: {valor}')
