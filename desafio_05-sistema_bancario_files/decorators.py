# desafio_04-sistema_bancario_decoradores/decorators.py

from datetime import datetime

# -----------
# decoradores
# -----------

def log_transacao(func):

    # def show_log(data, nome):
    #     log = f'╔══ [{data}] {nome} ══╗'
    #     print()
    #     print(f'{log}')
    #     print(f'╚' + '═'*(len(log) - 2) + '╝\n')

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        nome_funcao = func.__name__.upper()
        data_hora   = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_write = f"[{data_hora}] Funcao: {nome_funcao} ( '*args': {args} | '**kwargs': {kwargs} ) -> {result}\n"
        
        with open('log.txt', 'a') as file:
            file.write(log_write)
        # show_log(nome_funcao, data_hora)
        return result
    
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