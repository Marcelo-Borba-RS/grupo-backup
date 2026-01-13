from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
import matplotlib.pyplot as plt
import requests

# ============================================
# Conexão com MongoDB
# ============================================

def solicita_senha():
    print("-------------------------------------")
    print("##### Conexão com o Banco de Dados #####")
    usuario = input("Digite o usuario do mongo: ")
    senha = input("Digite sua senha do mongo: ")
    return f"mongodb+srv://{usuario}:{senha}@cluster0.5vugpvf.mongodb.net/?appName=Cluster0"

MONGO_URI = solicita_senha()

client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
db = client["clinica_estetica"]

col_clientes = db["clientes"]
col_profissionais = db["profissionais"]
col_fornecedores = db["fornecedores"]
col_procedimentos = db["procedimentos"]
col_agenda = db["agenda"]

# ============================================
# Funções Auxiliares
# ============================================

def calcular_idade(data_nasc):
    try:
        nascimento = datetime.strptime(data_nasc, "%d/%m/%Y")
        hoje = datetime.now()
        idade = hoje.year - nascimento.year
        if (hoje.month, hoje.day) < (nascimento.month, nascimento.day):
            idade -= 1
        return idade
    except:
        return None

def consultar_cep(cep):
    try:
        r = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
        if r.status_code == 200 and "erro" not in r.json():
            return r.json()
    except:
        pass
    return {}

# ============================================
# CADASTROS
# ============================================

def cadastrar_cliente():
    print("\n=== CADASTRO DE CLIENTE ===")
    nome = input("Nome: ")
    telefone = input("Telefone: ")
    email = input("Email: ")
    nascimento = input("Nascimento (DD/MM/AAAA): ")
    cep = input("CEP: ")

    endereco = consultar_cep(cep)
    if endereco:
        endereco["numero"] = input("Número: ")

    cliente = {
        "nome": nome,
        "telefone": telefone,
        "email": email,
        "nascimento": nascimento,
        "cep": cep,
        "endereco": endereco,
        "data_cadastro": datetime.now()
    }

    col_clientes.insert_one(cliente)
    print("✔ Cliente cadastrado!\n")

def cadastrar_profissional():
    print("\n=== CADASTRO DE PROFISSIONAL ===")
    col_profissionais.insert_one({
        "nome": input("Nome: "),
        "especialidade": input("Especialidade: "),
        "registro": input("Registro profissional: "),
        "data_cadastro": datetime.now()
    })
    print("✔ Profissional cadastrado!\n")

def cadastrar_fornecedor():
    print("\n=== CADASTRO DE FORNECEDOR ===")
    col_fornecedores.insert_one({
        "nome": input("Empresa: "),
        "cnpj": input("CNPJ: "),
        "telefone": input("Telefone: "),
        "cidade": input("Cidade: "),
        "data_cadastro": datetime.now()
    })
    print("✔ Fornecedor cadastrado!\n")

def cadastrar_procedimento():
    print("\n=== CADASTRO DE PROCEDIMENTO ===")
    col_procedimentos.insert_one({
        "nome": input("Nome do procedimento: "),
        "duracao": input("Duração (min): "),
        "valor": float(input("Valor (R$): ")),
        "data_cadastro": datetime.now()
    })
    print("✔ Procedimento cadastrado!\n")

# ============================================
# AGENDA
# ============================================

def cadastrar_agendamento():
    print("\n=== CADASTRAR AGENDAMENTO ===")
    col_agenda.insert_one({
        "profissional": input("Profissional: "),
        "procedimento": input("Procedimento: "),
        "data": input("Data (DD/MM/AAAA): "),
        "horario": input("Horário (HH:MM): "),
        "paciente": input("Paciente: "),
        "data_cadastro": datetime.now()
    })
    print("✔ Agendamento cadastrado!\n")

def listar_agenda_por_profissional():
    print("\n=== AGENDA POR PROFISSIONAL ===")
    nome = input("Nome do profissional: ")

    agendamentos = col_agenda.find(
        {"profissional": {"$regex": nome, "$options": "i"}}
    ).sort([("data", 1), ("horario", 1)])

    encontrou = False
    for a in agendamentos:
        encontrou = True
        print("-" * 40)
        print(f"Paciente     : {a['paciente']}")
        print(f"Procedimento : {a['procedimento']}")
        print(f"Data         : {a['data']}")
        print(f"Horário      : {a['horario']}")

    if not encontrou:
        print("Nenhum agendamento encontrado.")
    print()

# ============================================
# RELATÓRIOS
# ============================================

def relatorio_clientes_por_idade():
    contagem = {}
    for c in col_clientes.find():
        idade = calcular_idade(c.get("nascimento", ""))
        if idade is not None:
            contagem[idade] = contagem.get(idade, 0) + 1

    if not contagem:
        print("Nenhum dado válido.")
        return

    plt.bar(contagem.keys(), contagem.values())
    plt.xlabel("Idade")
    plt.ylabel("Quantidade")
    plt.title("Clientes por Idade")
    plt.show()

def relatorio_atendimentos_por_profissional():
    print("\n=== RELATÓRIO DE ATENDIMENTOS POR PROFISSIONAL ===")

    contagem = {}
    for a in col_agenda.find():
        prof = a.get("profissional", "Não Informado")
        contagem[prof] = contagem.get(prof, 0) + 1

    if not contagem:
        print("Nenhum atendimento registrado.")
        return

    for prof, qtd in contagem.items():
        print(f"- {prof}: {qtd} atendimento(s)")

    plt.figure(figsize=(10, 5))
    plt.bar(contagem.keys(), contagem.values())
    plt.xticks(rotation=30, ha="right")
    plt.title("Atendimentos por Profissional")
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(8, 8))
    plt.pie(contagem.values(), labels=contagem.keys(), autopct="%1.1f%%")
    plt.title("Distribuição de Atendimentos por Profissional")
    plt.axis("equal")
    plt.show()

def relatorio_pizza_clientes_por_localidade():
    print("\n=== RELATÓRIO DE CLIENTES POR LOCALIDADE ===")

    contagem = {}

    for c in col_clientes.find():
        endereco = c.get("endereco", {})
        cidade = endereco.get("localidade", "Não Informado")
        contagem[cidade] = contagem.get(cidade, 0) + 1

    if not contagem:
        print("Nenhum cliente com localidade registrada.")
        return

    for cidade, qtd in contagem.items():
        print(f"- {cidade}: {qtd} cliente(s)")

    plt.figure(figsize=(8, 8))
    plt.pie(
        contagem.values(),
        labels=contagem.keys(),
        autopct="%1.1f%%",
        startangle=90
    )
    plt.title("Clientes por Localidade")
    plt.axis("equal")
    plt.show()

# ============================================
# LISTAGENS
# ============================================

def listar_clientes():
    for c in col_clientes.find():
        print(c["nome"], "-", c["telefone"])

def listar_profissionais():
    for p in col_profissionais.find():
        print(p["nome"], "-", p["especialidade"])

def listar_procedimentos():
    for p in col_procedimentos.find():
        print(p["nome"], "- R$", p["valor"])

# ============================================
# MENU
# ============================================

def menu():
    while True:
        print("""
======= MENU – CLÍNICA ESTÉTICA =======
1  - Cadastrar Cliente
2  - Cadastrar Profissional
3  - Cadastrar Fornecedor
4  - Cadastrar Procedimento
5  - Cadastrar Agendamento
6  - Listar Clientes
7  - Listar Profissionais
8  - Listar Procedimentos
9  - Listar Agenda por Profissional
10 - Relatório Clientes por Idade
11 - Relatório Atendimentos por Profissional
12 - Relatório Clientes por Localidade (Pizza)
0  - Sair
=====================================
""")
        op = input("Opção: ")

        if op == "1": cadastrar_cliente()
        elif op == "2": cadastrar_profissional()
        elif op == "3": cadastrar_fornecedor()
        elif op == "4": cadastrar_procedimento()
        elif op == "5": cadastrar_agendamento()
        elif op == "6": listar_clientes()
        elif op == "7": listar_profissionais()
        elif op == "8": listar_procedimentos()
        elif op == "9": listar_agenda_por_profissional()
        elif op == "10": relatorio_clientes_por_idade()
        elif op == "11": relatorio_atendimentos_por_profissional()
        elif op == "12": relatorio_pizza_clientes_por_localidade()
        elif op == "0":
            print("Saindo...")
            break
        else:
            print("❌ Opção inválida")

# ============================================
# INICIALIZAÇÃO
# ============================================

if __name__ == "__main__":
    menu()

