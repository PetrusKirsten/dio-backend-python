# desafio_03-sistema_bancario-v3/main-2.py
import textwrap
from datetime import datetime
from abc import ABC, abstractclassmethod, abstractproperty


# ----------------------------------------------------
# classes para representar clientes e contas bancárias
# ----------------------------------------------------

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
                "data"  : datetime.now().strftime("%Y-%m-%d %H:%M:%S")})


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


# ---------------------------
# sistema bancário interativo
# ---------------------------

def menu():

    menu = """\n
╔═════════════════════════════════╗
║         KIRSTEN BANK            ║
╠═════════════════════════════════╣
║ [1]  Depositar                  ║
║ [2]  Sacar                      ║
║ [3]  Extrato                    ║
║ [4]  Criar Usuário              ║
║ [5]  Criar Conta                ║
║ [6]  Listar Contas              ║
╠═════════════════════════════════╣
║ [0]  Sair                       ║
╚═════════════════════════════════╝
>> Escolha uma opção: """
    
    return input(menu).strip()


def filtrar_cliente(cpf, clientes):
    """Filtra o cliente pelo CPF."""
    
    clientes_filtrados = [
        cliente for cliente in clientes 
        if cliente.cpf == cpf]
    
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(clientes):
    if not clientes.contas:
        print("\n* Nenhuma conta encontrada para o cliente.")
        return None
    
    # FIXME: poder escolher conta específica se o cliente tiver mais de uma
    return clientes.contas[0]  # Retorna a primeira conta do cliente 


def depositar(clientes):
    """Realiza o depósito, atualizando o saldo e extrato."""
    
    cpf = input("\n>> Informe o CPF do usuário: ").strip()
    
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n* Usuário não encontrado. Verifique o CPF informado.")
        return
    
    valor = float(input("\n* Informe o valor do depósito: R$ ").strip())
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        print("\n* Conta não encontrada para o cliente.")
        return
    
    cliente.realizar_transacao(conta, transacao)
    

def sacar(clientes):
    """Realiza o saque, atualizando o saldo, extrato e número de saques."""
    
    cpf = input("\n>> Informe o CPF do usuário: ").strip()

    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n* Usuário não encontrado. Verifique o CPF informado.")
        return
    
    valor = float(input("\n* Informe o valor do saque: R$ ").strip())
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        print("\n* Conta não encontrada para o cliente.")
        return
    
    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    """Gera o extrato bancário formatado."""

    cpf = input("\n>> Informe o CPF do usuário: ").strip()
    
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n* Usuário não encontrado. Verifique o CPF informado.")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        print("\n* Conta não encontrada para o cliente.")
        return
    
    print("\n----------------------------------") 
    print("EXTRATO BANCÁRIO") 
    print("----------------------------------") 
          
    transacoes = conta.historico.transacoes
    extrato = ""

    if not transacoes:
        extrato = "\nNenhum lançamento realizado\n"
    else:
        for transacao in transacoes:
            extrato += (f"\n{transacao['data']} - {transacao['tipo']}: R$ {transacao['valor']:.2f}")

    print(extrato)
    print("\n----------------------------------")
    print(f"Saldo atual: R$ {conta.saldo:.2f}")
    print("----------------------------------\n")


def criar_cliente(clientes):
    """Cria um dicionário representando um usuário bancário."""

    cpf = input(">> Informe o CPF do usuário: ").strip()

    cliente = filtrar_cliente(cpf, clientes)
    if cliente:
        print("\n* Usuário já cadastrado.")
        return
    
    nome            = input(">> Informe o nome do usuário: ").strip()
    data_nascimento = input(">> Informe a data de nascimento (DD/MM/AAAA): ").strip()
    endereço        = input(">> Informe o endereço do usuário: ").strip()

    cliente = PessoaFisica(nome, data_nascimento, cpf, endereço)
    clientes.append(cliente)

    print("\n** Usuário cadastrado com sucesso! **")


def criar_conta(numero_conta, clientes, contas):
    """Cria uma conta bancária para um usuário existente."""
    
    cpf = input(">> Informe o CPF do usuário: ").strip()
    
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n* Usuário não encontrado. Verifique o CPF informado.")
        return
    
    conta = ContaCorrente.nova_conta(cliente, numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n** Conta criada com sucesso! **")


def listar_contas(contas):
    for conta in contas:
        print("\n----------------------------------")
        print(textwrap.dedent(str(conta)))
        print("----------------------------------")
        # print(f"Conta {conta.numero} "
        #       f"- Agência {conta.agencia} "
        #       f"- Cliente: {conta.cliente.nome} "
        #       f"- Saldo: R$ {conta.saldo:.2f}")


def main():
    """Função principal que executa o sistema bancário."""

    clientes = []
    contas   = []
        
    while True:
        
        opcao = menu()
    
        if opcao == "1":
            print("\n** Depósito **")
            depositar(clientes)

        elif opcao == "2":
            print("\n** Saque **")
            sacar(clientes)

        elif opcao == "3":
            print("\n** Extrato **")
            exibir_extrato(clientes)
            
        elif opcao == "4":
            criar_cliente(clientes)
        
        elif opcao == "5":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "6":
            print("\n** Listar Contas **")
            listar_contas(contas)

        elif opcao == "0":
            print("\n** Encerrando o sistema bancário... **")
            print("Obrigado por usar o KIRSTEN BANK!")
            
            break

        else:
            print("\n* Opção inválida, por favor, tente novamente.\n"
                  "* Escolha uma opção válida do menu.")


if __name__ == "__main__":
    main()