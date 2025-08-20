# desafio_04-sistema_bancario_decoradores/decorators.py

from datetime import datetime

# -----------
# decoradores
# -----------

def log_transacao(func):

    def wrapper(*args, **kwargs):

        nome_funcao = func.__name__.capitalize()
        hora        = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log = f'╔══ [{hora}] {nome_funcao} ══╗'

        # TODO: alterar a implementação para salvar em arquivo

        print()
        print(f'{log}')
        print(f'╚' + '═'*(len(log) - 2) + '╝\n')
        # print(f'='*len(log))

        return func(*args, **kwargs)
    
    return wrapper

# ------ funções testes

def sacar():
    pass

def depositar():
    pass

def criar_usuario():
    pass

def criar_conta():
    pass


if __name__ == '__main__':
    log_transacao(sacar)
    log_transacao(depositar)
    log_transacao(criar_usuario)
    log_transacao(criar_conta)