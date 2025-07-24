# desafio_04-sistema_bancario-v3/app.py
import textwrap

from sistema import (PessoaFisica, 
                     ContaCorrente,
                     Saque, 
                     Deposito)

from decorators import log_transacao as log

# ---------------------------
# sistema bancário interativo
# ---------------------------


# ------- Funções do menu

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

@log
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
    
@log
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

@log
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
    
    # TODO: implementar o gerador definido em Historico
    transacoes = conta.historico.transacoes
    extrato = ""

    if not transacoes:
        extrato = "\nNenhum lançamento realizado\n"
    else:
        for transacao in transacoes:
            extrato += (f"\n{transacao['data']} | {transacao['tipo']}: R$ {transacao['valor']:.2f}")

    print(extrato)
    print("\n----------------------------------")
    print(f"Saldo atual: R$ {conta.saldo:.2f}")
    print("----------------------------------\n")

@log
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

@log
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
    # TODO: alternar implementação para usar a classe ContaIterador

    for conta in contas:
        print("\n----------------------------------")
        print(textwrap.dedent(str(conta)))
        print("----------------------------------")

# ------- Layout do menu

def menu():

    menu = """\n
╔═════════════════════════════════════════╗
║               KIRSTEN BANK              ║
╠═════════════════════════════════════════╣
║                                         ║
║     [1]  Depositar                      ║
║     [2]  Sacar                          ║
║     [3]  Extrato                        ║
║     [4]  Criar Usuário                  ║
║     [5]  Criar Conta                    ║
║     [6]  Listar Contas                  ║
║                                         ║
╠═════════════════════════════════════════╣
║     [0]  Sair                           ║
╚═════════════════════════════════════════╝

>> Escolha uma opção: """
    
    return input(menu).strip()


# ------- Função principal

def main():
    """Função principal que executa o sistema bancário."""
    clientes = []
    contas   = []
        
    while True:
        
        opcao = menu()
    
        if opcao == "1":
            # print("\n** Depósito **")
            depositar(clientes)

        elif opcao == "2":
            # print("\n** Saque **")
            sacar(clientes)

        elif opcao == "3":
            # print("\n** Extrato **")
            exibir_extrato(clientes)
            
        elif opcao == "4":
            criar_cliente(clientes)
        
        elif opcao == "5":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "6":
            # print("\n** Listar Contas **")
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