import csv
from sistema import PessoaFisica, ContaCorrente

CLIENTES_FILE = 'clientes.csv'
CONTAS_FILE   = 'contas.csv'

def load_clientes():
    """
    Lê o arquivo clientes.csv e retorna uma lista de instâncias PessoaFisica.
    """
    clientes = []

    try:
        with open(CLIENTES_FILE, newline='', encoding='utf-8') as f:

            reader = csv.DictReader(f)

            for row in reader:
                cliente = PessoaFisica(
                    nome            = row['nome'],
                    data_nascimento = row['data_nascimento'],
                    cpf             = row['cpf'],
                    endereço        = row['endereco'])
                
                clientes.append(cliente)

    except FileNotFoundError:
        pass

    return clientes


def save_clientes(clientes):
    """
    Salva todos os clientes no arquivo clientes.csv.
    """
    with open(CLIENTES_FILE, 'w', newline='', encoding='utf-8') as f:

        fieldnames = ['cpf', 'nome', 'data_nascimento', 'endereco']

        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for c in clientes:
            writer.writerow({
                'cpf'             : c.cpf,
                'nome'            : c.nome,
                'data_nascimento' : c.data_nascimento,
                'endereco'        : c.endereço})


def load_contas(clientes):
    """
    Lê o arquivo contas.csv e retorna uma lista de instâncias ContaCorrente,
    associando-as ao respectivo PessoaFisica já carregado.
    """

    contas = []

    try:
        with open(CONTAS_FILE, newline='', encoding='utf-8') as f:

            reader = csv.DictReader(f)

            for row in reader:
                cpf = row['cpf']
                cliente = next((c for c in clientes if c.cpf == cpf), None)

                if not cliente:
                    continue  # ignora contas sem cliente cadastrado

                conta = ContaCorrente.nova_conta(cliente, int(row['numero']))
                # conta.saldo = float(row['saldo'])

                # TODO: se quiser carregar histórico

                cliente.contas.append(conta)
                contas.append(conta)

    except FileNotFoundError:
        pass

    return contas

def save_contas(contas):
    """
    Salva todas as contas no arquivo contas.csv.
    """

    with open(CONTAS_FILE, 'w', newline='', encoding='utf-8') as f:

        fieldnames = ['numero', 'cpf', 'saldo']
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()

        for c in contas:

            writer.writerow({
                'numero': c.numero,
                'cpf': c.cliente.cpf,
                'saldo': f"{c.saldo:.2f}"})
