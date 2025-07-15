# desafio_01-sistema_bancario/main.py

def menu():

    menu = '''\n
==========================
        KIRSTEN BANK       
==========================
[1]\tDepositar
[2]\tSacar
[3]\tExtrato
[0]\tSair
==========================
>> Escolha uma opção: '''
    
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


def main():
    
    AGENCIA = "0001"
    LIMITE_DE_SAQUES = 3

    saldo         = 0
    extrato       = ""
    limite_saque  = 500
    numero_saques = 0

    while True:
        opcao = menu()
    
        if opcao == "1":
            valor = float(input("\n* Informe o valor do depósito: R$ ").strip())
            saldo, extrato = depositar(saldo, valor, extrato)


        elif opcao == "2":
            valor = float(input("\n* Informe o valor do saque: R$ ").strip())
            saldo, extrato, numero_saques = sacar(
                saldo         = saldo,
                valor         = valor,
                extrato       = extrato,
                limite        = LIMITE_DE_SAQUES,
                numero_saques = numero_saques,
                limite_saque  = limite_saque)

        elif opcao == "3":
            print(exibir_extrato(saldo, extrato))
            
        elif opcao == "0":
            print("\n* Obrigado por utilizar o Kirsten Bank!\n"
                  "* Até a próxima!")
            break

        else:
            print("\n* Opção inválida, por favor, tente novamente.\n"
                  "* Escolha uma opção válida do menu.")


if __name__ == "__main__":
    main()