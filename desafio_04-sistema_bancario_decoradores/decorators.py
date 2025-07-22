# desafio_04-sistema_bancario_decoradores/decorators.py

from datetime import datetime

# -----------
# decoradores
# -----------

def sacar():
    pass

def depositar():
    pass

def criar_usuario():
    pass

def criar_conta():
    pass


def log_transacao(func):

    nome_funcao = func.__name__.capitalize()
    hora        = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f'{hora} | {nome_funcao}')

if __name__ == '__main__':
    log_transacao(sacar)
    log_transacao(depositar)
    log_transacao(criar_usuario)
    log_transacao(criar_conta)