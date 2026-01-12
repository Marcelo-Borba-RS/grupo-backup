import os
import glob
import pandas as pd
import xlrd
import pymongo
from datetime import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from cryptography.fernet import Fernet
import sys  # Importado para encerrar o programa caso falte a senha

# ==============================
# CONFIGURAÇÕES GERAIS E SEGURANÇA
# ==============================

def solicita_caminho_dados():
    """Solicita ao usuário o diretório onde os arquivos estão localizados."""
    while True:
        caminho = input("\nDigite o caminho completo da pasta de dados: ").strip()
        # Remove aspas caso o usuário tenha copiado o caminho com elas
        caminho = caminho.replace('"', '').replace("'", "")

        if os.path.exists(caminho):
            print(f"✅ Pasta selecionada: {caminho}")
            return caminho
        else:
            print(f"❌ Erro: O caminho '{caminho}' não existe. Tente novamente.")


# Chamada inicial para configurar o ambiente
PASTA = solicita_caminho_dados()
PADRAO = "Boletim_Diario_dos_Atendimentos_*"
COLS_FORCE_STR = ["Nr. Registro", "CNS"]
COLS_SENSIVEIS = ["Paciente", "CNS", "Data Nascimento", "Telefone", "Profissional"]
CSV_CHUNK_SIZE = 500_000
PARQUET_SAIDA = os.path.join(PASTA, "consolidado.parquet")

# Chave de Criptografia
CHAVE_CRIPTOGRAFIA = Fernet.generate_key()
cipher_suite = Fernet(CHAVE_CRIPTOGRAFIA)


# ==============================
# SEGURANÇA E CONEXÃO
# ==============================

def solicita_senha():
    print("-------------------------------------")
    print("##### Carregando Credenciais #####")

    # Caminho do arquivo de senhas (na mesma pasta do script)
    caminho_segredos = "segredos.txt"

    try:
        with open(caminho_segredos, "r") as arquivo:
            linhas = arquivo.readlines()

            # Verifica se o arquivo tem pelo menos 2 linhas
            if len(linhas) < 2:
                print("❌ Erro: O arquivo 'segredos.txt' deve ter Usuário na linha 1 e Senha na linha 2.")
                return None

            # .strip() remove espaços e quebras de linha (\n)
            usuario = linhas[0].strip()
            senha = linhas[1].strip()

            uri = f"mongodb+srv://{usuario}:{senha}@cluster0.5vugpvf.mongodb.net/?appName=Cluster0"
            print("✓ Credenciais carregadas com segurança!")
            return uri

    except FileNotFoundError:
        print(f"❌ Erro Crítico: O arquivo '{caminho_segredos}' não foi encontrado.")
        print("Crie o arquivo com seu usuário na linha 1 e senha na linha 2.")
        return None


# Carrega a URI. Se falhar, encerra o programa para evitar erros depois.
MONGO_URI = solicita_senha()

if MONGO_URI is None:
    print("\nEncerrando o programa por falta de credenciais.")
    sys.exit()  # Para a execução aqui se não tiver senha


# ==============================
# FUNÇÕES DE SEGURANÇA E LOG
# ==============================

def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")


def encriptar_valor(valor):
    if pd.isna(valor) or str(valor).strip() == "":
        return ""
    conteudo_bytes = str(valor).encode('utf-8')
    token = cipher_suite.encrypt(conteudo_bytes)
    return token.decode('utf-8')


def aplicar_criptografia(df):
    for col in COLS_SENSIVEIS:
        if col in df.columns:
            df[col] = df[col].apply(encriptar_valor)
    return df


# ==============================
# PROCESSAMENTO (REUTILIZADO)
# ==============================

def read_xls_old(path):
    book = xlrd.open_workbook(path)
    sheet = book.sheet_by_index(0)
    data = [sheet.row_values(r) for r in range(sheet.nrows)]
    return pd.DataFrame(data[1:], columns=data[0])


def safe_read_excel(arquivo):
    ext = os.path.splitext(arquivo)[1].lower()
    try:
        if ext == ".xls":
            return read_xls_old(arquivo)
        elif ext in [".xlsx", ".xlsm"]:
            return pd.read_excel(arquivo, engine="openpyxl")
        elif ext == ".xlsb":
            return pd.read_excel(arquivo, engine="pyxlsb")
        else:
            raise ValueError(f"Extensão não suportada: {ext}")
    except Exception as e:
        raise RuntimeError(f"Falha ao ler {arquivo}: {e}")


def carregar_arquivos():
    arquivos = glob.glob(os.path.join(PASTA, PADRAO))
    arquivos = [a for a in arquivos if a.lower().endswith((".xls", ".xlsx", ".xlsm", ".xlsb"))]
    log(f"{len(arquivos)} arquivos encontrados em {PASTA}.")

    dfs = []
    for arq in arquivos:
        try:
            df = safe_read_excel(arq)
            # Normalização básica
            for col in COLS_FORCE_STR:
                if col in df.columns: df[col] = df[col].astype(str).fillna("")

            df = aplicar_criptografia(df)
            df["arquivo_origem"] = os.path.basename(arq)
            dfs.append(df)
            log(f"  ✓ {os.path.basename(arq)} lido.")
        except Exception as e:
            log(f"  ✗ Erro em {arq}: {e}")

    if not dfs: raise RuntimeError("Nenhum arquivo válido carregado.")
    return pd.concat(dfs, ignore_index=True)


def gerar_parquet():
    try:
        df = carregar_arquivos()
        df.to_parquet(PARQUET_SAIDA, index=False)
        log(f"✓ Sucesso: {PARQUET_SAIDA}")
    except Exception as e:
        log(f"ERRO: {e}")


# ==============================
# FUNÇÕES MONGO E MENU
# ==============================

def salvar_log_mongo():
    if not os.path.exists(PARQUET_SAIDA):
        print("\n❌ Parquet não encontrado.\n")
        return
    m_time = datetime.fromtimestamp(os.path.getmtime(PARQUET_SAIDA))
    client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
    db = client["meu_banco"]
    collection = db["modificacoes_arquivos"]
    documento = {
        "file_path": PARQUET_SAIDA,
        "last_modified": m_time,
        "status": "Criptografado"
    }
    collection.insert_one(documento)
    print(f"\n✅ Log salvo no MongoDB para o arquivo em: {PASTA}\n")


def menu():
    while True:
        print(f"\n========== MENU (Pasta: {PASTA}) ==========")
        print("1 - Gerar arquivo Parquet (Criptografado)")
        print("2 - Salvar log no MongoDB")
        print("0 - Sair")
        opcao = input("Escolha: ")
        if opcao == "1":
            gerar_parquet()
        elif opcao == "2":
            salvar_log_mongo()
        elif opcao == "0":
            break


if __name__ == "__main__":
    menu()