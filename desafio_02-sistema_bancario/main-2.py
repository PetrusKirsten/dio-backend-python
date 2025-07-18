# desafio_02-sistema_bancario-v2/main-2.py

AGENCIA = "0001"
LIMITE_DE_SAQUES = 3

usuarios = []
contas   = []


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
╠═════════════════════════════════╣
║ [0]  Sair                       ║
╚═════════════════════════════════╝
>> Escolha uma opção: """
    
    return input(menu).strip()


def depositar(saldo, 
              valor, 
              extrato) -> tuple:
    """Realiza o depósito, atualizando o saldo e extrato."""
    
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print(f"\n* Depósito de R${valor:.2f} realizado com sucesso!")

    else:
        print("\n* Valor inválido para depósito.\n"
              "* Informe um valor maior que zero.")
        
    return saldo, extrato


def sacar(*,
          saldo,
          valor,
          extrato,
          limite,
          numero_saques,
          limite_saque) -> tuple:
    """Realiza o saque, atualizando o saldo, extrato e número de saques."""
    
    excedeu_saldo  = valor > saldo
    excedeu_saques = numero_saques >= limite    
    excedeu_limite = valor > limite_saque

    if excedeu_saldo:
        print("\n* Saldo insuficiente para saque.\n"
              f"* Seu saldo atual é de R$ {saldo:.2f}.")
        
    elif excedeu_limite:
        print(f"\n* Valor do saque excede o limite de R$ {limite_saque:.2f}.\n"
              "* Informe um valor menor ou igual ao limite.")
        
    elif excedeu_saques:
        print(f"\n* Número máximo de saques diários excedido.\n"
              f"* Você já realizou {numero_saques} saques hoje, o limite é de {limite} saques.")
        
    elif valor > 0:
        saldo         -= valor
        extrato       += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1

        print(f"\n* Saque de R${valor:.2f} realizado com sucesso!")

    else:
        print("\n* Valor inválido para saque.\n"
              "* Informe um valor maior que zero.")

    return saldo, extrato, numero_saques


def exibir_extrato(saldo, extrato='') -> str:
    """Gera o extrato bancário formatado."""

    menu_extrato = '''\n
-------------------------- 
EXTRATO
--------------------------
{extrato}
--------------------------
Saldo: R$ {saldo:.2f}
--------------------------'''
    
    return menu_extrato.format(
        saldo=saldo, 
        extrato=extrato if extrato 
        else "\nNenhum lançamento realizado\n")


def criar_usuario(usuarios) -> dict:
    """Cria um dicionário representando um usuário bancário."""
    
    print("\n** Cadastro de Usuário **\n")

    # if usuarios:
    #     print("\n* Usuários já cadastrados:")
    #     for usuario in usuarios:
    #         print(f"- {usuario['nome']} ({usuario['cpf']})")

    # else:
    #     print("\n* Nenhum usuário cadastrado ainda.")
    
    cpf             = input(">> Informe o CPF (apenas números): ").strip()
    # Validação do CPF
    if len(cpf) != 11 or not cpf.isdigit():
        print("\n* CPF inválido. Deve conter 11 dígitos numéricos.")
        return None
    # Verifica se o CPF já está cadastrado
    if any(usuario['cpf'] == cpf for usuario in usuarios):
        print("\n* CPF já cadastrado. Por favor, informe um CPF diferente.")
        return None
    
    nome            = input(">> Informe o nome completo: ").strip()
    data_nascimento = input(">> Informe a data de nascimento (DD/MM/AAAA): ").strip()
    endereco        = input(">> Informe o endereço (logradouro, número - bairro - cidade/UF): ").strip()

    usuario = {
        "cpf"             : cpf,
        "nome"            : nome,
        "data_nascimento" : data_nascimento,
        "endereco"        : endereco
    }

    return usuarios.append(usuario)


def criar_conta(contas, cc, /, usuarios=usuarios) -> None:
    """Cria uma conta bancária para um usuário existente."""
    
    print("\n** Criação de Conta **")
    
    if not usuarios:
        print("\n* Nenhum usuário cadastrado. Por favor, crie um usuário primeiro.")
        return
    
    cpf = input(">> Informe o CPF do usuário: ").strip()
    
    usuario = next((u for u in usuarios if u['cpf'] == cpf), None)
    
    if usuario:

        conta = {
            "agencia" : AGENCIA,
            "conta"   : cc,
            "usuario" : usuario}

        print(f"\n* Conta criada com sucesso para {usuario['nome']}!")
        print(f"* O número da conta é (Ag.-C.C.): {conta['agencia']}-{conta['conta']}")

        return contas.append(conta)
        
    else:
        print("\n* Usuário não encontrado. Verifique o CPF informado.")


def verificar_usuario():
    """Verifica se o usuário existe e retorna a conta."""

    if not usuarios:
        print("\n* Nenhum usuário cadastrado. Por favor, crie um usuário primeiro.")
        return

    usuario = input("\n* Informe o CPF do usuário: ").strip()
    if not usuario:
        print("\n* Usuário não encontrado. Verifique o CPF informado.")
        return
        
    conta = next((c for c in contas if c['usuario']['cpf'] == usuario), None)
    if not conta:
        print("\n* Conta não encontrada. Por favor, crie uma conta primeiro.")
        return
    
    print(f"\n* Conta encontrada: {conta['agencia']}-{conta['conta']}")
    print(f"* Nome do usuário:  {conta['usuario']['nome']}")
    
    return conta
            


def main():
    """Função principal que executa o sistema bancário."""

    cc            = 0
    saldo         = 0
    extrato       = ""
    limite_saque  = 500
    numero_saques = 0
        
    while True:
        
        opcao = menu()
    
        if opcao == "1":
            print("\n** Depósito **")
            
            conta = verificar_usuario()
            if not conta:
                continue

            valor = float(input("\n* Informe o valor do depósito: R$ ").strip())
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "2":
            print("\n** Saque **")

            conta = verificar_usuario()
            if not conta:
                continue
            
            valor = float(input("\n* Informe o valor do saque: R$ ").strip())
            saldo, extrato, numero_saques = sacar(
                saldo         = saldo,
                valor         = valor,
                extrato       = extrato,
                limite        = LIMITE_DE_SAQUES,
                numero_saques = numero_saques,
                limite_saque  = limite_saque)

        elif opcao == "3":
            print("\n** Extrato **")

            conta = verificar_usuario()  
            if not conta:
                continue
                      
            print(exibir_extrato(saldo, extrato))
            
        elif opcao == "4":
            criar_usuario(usuarios)
        
        elif opcao == "5":
            cc += 1
            conta = criar_conta(contas, cc, usuarios=usuarios)
            if conta:
                print(f"\n* Conta criada com sucesso: {conta['agencia']}-{conta['cc']}")

        elif opcao == "0":
            print("\n* Obrigado por utilizar o Kirsten Bank!\n"
                  "* Até a próxima!")
            break

        else:
            print("\n* Opção inválida, por favor, tente novamente.\n"
                  "* Escolha uma opção válida do menu.")


if __name__ == "__main__":
    main()