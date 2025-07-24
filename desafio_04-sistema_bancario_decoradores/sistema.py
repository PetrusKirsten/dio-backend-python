# desafio_04-sistema_bancario-v3/main-2.py

from datetime import datetime
from abc import ABC, abstractclassmethod, abstractproperty

# ----------------------------------------------------
# classes para representar clientes e contas bancárias
# ----------------------------------------------------

class ContaIterador:
    def __init__(self, contas):
        self.contas = contas

    def __iter__(self):
        return self

    def __next__(self):
        pass


class Cliente:
    """Classe base para representar um cliente do banco.
    Esta classe pode ser estendida para diferentes tipos de clientes,
    como Pessoa Física ou Pessoa Jurídica."""
    def __init__(self, endereço):
        self.endereço = endereço
        self.contas   = []
    
    def __str__(self):
        return f"Cliente com endereço: {self.endereço}, Contas: {len(self.contas)}"
    
    def realizar_transacao(self, conta, transacao):
        
        if len(conta.historico.get_transacoes()) >= 10:
            print("\n ** Você excedeu o número de transações permitidas para hoje! **")
            return
        
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)
    

class PessoaFisica(Cliente):
    """
    Classe para representar uma pessoa física como cliente do banco.
    """
    def __init__(self, nome, data_nascimento, cpf, endereço):
        super().__init__(endereço)

        self.nome            = nome
        self.data_nascimento = data_nascimento
        self.cpf             = cpf
    
    def __str__(self):
        return f"Pessoa Física: {self.nome}, CPF: {self.cpf}, Nascimento: {self.data_nascimento}, Endereço: {self.endereço}"


class Conta:
    """
    Classe base para contas bancárias.
    """    
    def __init__(self, numero, cliente):
        
        self._saldo     = 0.0
        self._numero    = numero
        self._agencia   = "0001"
        self._cliente   = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls (numero, cliente)

    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero 
    
    @property
    def agencia(self):  
        return self._agencia
    
    @property
    def cliente(self):  
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        """
        Realiza o saque da conta, atualizando o saldo e o histórico.
        Retorna True se o saque for bem-sucedido, False caso contrário.        
        """

        if valor <= 0:
            print(f"* O valor do saque deve ser positivo.")
        
        elif valor > self._saldo:
            print(f"* Saldo insuficiente para saque.")
        
        else:
            self._saldo -= valor
            print(f"* Saque de R$ {valor:.2f} realizado com sucesso.")

            return True
        
        return False

    def depositar(self, valor):
        """
        Realiza o depósito na conta, atualizando o saldo e o histórico.
        Retorna True se o depósito for bem-sucedido, False caso contrário.  
        """

        if valor > 0:
            self._saldo += valor
            print(f"* Depósito de R$ {valor:.2f} realizado com sucesso.")
            
            return True

        else:
            print(f"* O valor do depósito deve ser positivo.")
            
            return False
        

class ContaCorrente(Conta):
    """
    Classe para representar uma conta corrente.
    Esta classe herda de Conta e adiciona funcionalidades específicas
    como limite de saque e número máximo de saques.
    """
    
    def __init__(self, numero, cliente, limite=500, limite_de_saques=3):
        super().__init__(numero, cliente)
        
        self.limite_de_saques = limite_de_saques
        self.limite           = limite
    
    def __str__(self):
        return (f"Conta Corrente {self.numero} - Agência {self.agencia}\n"
                f"Cliente: {self.cliente.nome}, Saldo: R$ {self.saldo:.2f}, "
                f"Limite: R$ {self.limite:.2f}, Saques: {self.limite_de_saques}")

    def sacar(self, valor):
        """
        Realiza o saque na conta corrente, respeitando o limite e o número de saques.
        Retorna True se o saque for bem-sucedido, False caso contrário.        
        """

        numero_saques = len([
            transacao for transacao 
            in self.historico.transacoes 
            if transacao["tipo"] == Saque.__name__
        ])

        if valor > self.limite:
            print(f"* O valor do saque não pode exceder o limite de R$ {self.limite:.2f}.")
        
        elif numero_saques >= self.limite_de_saques:
            print(f"* Número máximo de saques ({self.limite_de_saques}) atingido.")
        
        else:
            return super().sacar(valor)
        
        return False
    

class Historico:
    """
    Classe para gerenciar o histórico de transações de uma conta.
    """
    def __init__(self):
        self._transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):

        self._transacoes.append({
                "tipo"  : transacao.__class__.__name__,
                "valor" : transacao.valor,
                "data"  : datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")})

    def get_relatorio(self, tipo_transacao=None):

        if tipo_transacao:
            return True
        
        return None

    def get_transacoes(self):
        """ Retorna as transações do dia """

        data_atual = datetime.utcnow().date()
        transacoes = []

        for transacao in self._transacoes:
            data_transacao = datetime.strptime(transacao['data'],
                                               "%d-%m-%Y %H:%M:%S").date()
            
            if data_atual == data_transacao:
                transacoes.append(transacao)
            
        return transacoes


class Transacao(ABC):
    """
    Classe base para transações bancárias.
    Esta classe deve ser estendida para criar transações específicas,
    como Saque, Depósito, etc.
    """
    
    @property
    @abstractproperty
    def valor(self):
        pass
    
    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    """
    Classe para representar uma transação de saque.
    """
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.sacar(self._valor):
            conta.historico.adicionar_transacao(self)

        else:
            print(f"* Não foi possível registrar o saque de R$ {self._valor:.2f}.")


class Deposito(Transacao):
    """
    Classe para representar uma transação de depósito.
    """
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self._valor):
            conta.historico.adicionar_transacao(self)

        else:
            print(f"* Não foi possível registrar o depósito de R$ {self._valor:.2f}.")
