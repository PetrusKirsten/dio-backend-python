# Entrada do número de pacientes
n = int(input().strip())

# Lista para armazenar pacientes
pacientes = []

# Loop para entrada de dados
for _ in range(n):
    nome, idade, status = input().strip().split(", ")
    idade = int(idade)
    pacientes.append((nome, idade, status))

# TODO: Ordene por prioridade: urgente > idosos > demais:
def ordenar_pacientes(lista: list):
    """Ordena a lista de pacientes por prioridade."""

    pacientes_ordenados = sorted(
        lista,
        key=lambda p: (p[2] != 'urgente',   # urgentes (False) vêm antes de normais (True)
                       -p[1],               # idade decrescente
                       p[0].lower())        # nome em ordem alfabética
    )
    return [nome for nome, _, _ in pacientes_ordenados]

pacientes_ordenados = ordenar_pacientes(pacientes)

# TODO: Exiba a ordem de atendimento com título e vírgulas:
print("Ordem de atendimento:", ", ".join(f"{paciente}" for paciente in pacientes_ordenados))

