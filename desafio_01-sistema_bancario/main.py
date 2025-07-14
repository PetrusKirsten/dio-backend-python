
def main():
    
    LIMITE_DE_SAQUES = 3

    saldo         = 0
    extrato       = ""
    limite_saque  = 500
    numero_saques = 0

    menu = '''
==========================
    SISTEMA BANCÁRIO
==========================
[1] Depositar
[2] Sacar
[3] Extrato
[0] Sair
==========================
>> Escolha uma opção: '''

    while True:
        opcao = input(menu)
    
        if opcao == "1":
            valor = float(input("\n>> Informe o valor do depósito: R$"))

            if valor > 0:
                saldo   += valor
                extrato += f"Depósito: R$ {valor:.2f}\n"

                print(f"\n* Depósito de R${valor:.2f} realizado com sucesso!")
            
            else:
                print("\n* Valor inválido para depósito.\n"
                      "* Informe um valor maior que zero.")
                
        elif opcao == "2":
            valor = float(input("\n>> Informe o valor do saque: R$"))

            excedeu_saldo  = valor > saldo
            excedeu_limite = valor > limite_saque
            excedeu_saques = numero_saques >= LIMITE_DE_SAQUES

            if excedeu_saldo:
                print("\n* Saldo insuficiente para saque.\n"
                      f"* Seu saldo atual é de R$ {saldo:.2f}.")
            
            elif excedeu_limite:
                print(f"\n* Valor do saque excede o limite de R$ {limite_saque:.2f}.\n"
                      "* Informe um valor menor ou igual ao limite.")
            
            elif excedeu_saques:
                print(f"\n* Número máximo de saques diários excedido.\n"
                      f"* Você já realizou {numero_saques} saques hoje, o limite é de {LIMITE_DE_SAQUES} saques.")
            
            elif valor > 0:
                saldo -= valor
                extrato += f"Saque: R$ {valor:.2f}\n"
                numero_saques += 1
                print(f"\n* Saque de R${valor:.2f} realizado com sucesso!")

            else:
                print("\n* Valor inválido para saque.\n"
                      "* Informe um valor maior que zero.")
        
        elif opcao == "3":
            menu_extrato = '''
========================== 
   EXTRATO
==========================
{extrato}
--------------------------
Saldo: R$ {saldo:.2f}
=========================='''

            print(menu_extrato.format(saldo=saldo, extrato=extrato if extrato else "\nNenhum lançamento realizado\n"))

        elif opcao == "0":
            print("\n* Sistema bancário encerrado. Até logo!\n")
            break
        
        else:
            print("\n* Opção inválida. Por favor, escolha uma opção válida.")


if __name__ == "__main__":
    main()