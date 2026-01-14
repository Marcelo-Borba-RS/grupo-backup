# 📂 Portfólio de Projetos: Engenharia de Dados e Python

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Data_Viz-orange?style=for-the-badge)

Este repositório contém soluções desenvolvidas para **Engenharia de Dados** e **Automação de Sistemas**, utilizando Python e Banco de Dados NoSQL (MongoDB).

---

## 🛡️ Projeto 1: Pipeline de ETL Seguro (LGPD)
**Foco:** Engenharia de Dados, Segurança e Performance.

Sistema que automatiza a leitura de arquivos Excel, aplica criptografia em dados sensíveis (LGPD) e converte para formato Parquet.

### Funcionalidades
* **🕵️ Leitura Inteligente:** Processa múltiplos formatos (`.xlsx`, `.xlsb`).
* **🔒 Criptografia:** Protege dados pessoais (Nome, CNS, Telefone) usando algoritmo Fernet.
* **⚡ Alta Performance:** Consolidação de dados em **Parquet**.
* **☁️ Auditoria:** Logs de execução salvos no **MongoDB Atlas**.

---

## 🏥 Projeto 2: Sistema de Gestão - Clínica de Estética
**Foco:** CRUD, Integração de API e Dashboards.

Sistema completo para gerenciamento de clientes, profissionais e agendamentos, com geração de relatórios gráficos.

### Funcionalidades
* **🔌 Integração API:** Consulta automática de endereço via CEP (API **ViaCEP**).
* **📊 Dashboards:** Gráficos de barra e pizza com **Matplotlib** (Análise de idade, atendimentos e localidade).
* **🗄️ Banco de Dados:** CRUD completo (Create, Read, Update, Delete) conectado ao **MongoDB Atlas**.
* **📅 Agenda:** Controle de horários por profissional e procedimento.

---

## 🛠️ Tecnologias do Portfólio

* **Linguagem:** Python 3.x
* **Dados & ETL:** Pandas, NumPy, PyArrow (Parquet), OpenPyXL.
* **Visualização:** Matplotlib.
* **Web/API:** Requests (Consumo de APIs REST).
* **Banco de Dados:** PyMongo (MongoDB Atlas).
* **Segurança:** Cryptography (Fernet).

## 📞 Equipe de Desenvolvimento

| Desenvolvedor | GitHub |
| :--- | :--- |
| [**Marcelo Borba**](https://github.com/Marcelo-Borba-RS) | [![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white)](https://github.com/Marcelo-Borba-RS) |
| [**Marian Cordeiro**](https://github.com/mariscordeiro99-sudo) | [![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white)](https://github.com/mariscordeiro99-sudo) |
| [**Pablo Leonardo**](https://github.com/pabloleonardo93-png) | [![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white)](https://github.com/pabloleonardo93-png) |
| [**Philipe Félix**](https://github.com/philipe-felix) | [![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white)](https://github.com/philipe-felix) |

---

## ⚙️ Instalação e Configuração

Para rodar qualquer um dos projetos, siga os passos:

### 1. Clone o repositório
```bash
git clone https://github.com/Marcelo-Borba-RS/grupo-backup.git
cd grupo-backup

### 2. Instale todas as dependências
Atualizamos a lista para suportar os dois projetos:

```bash
pip install pandas pymongo[srv] cryptography openpyxl pyxlsb xlrd pyarrow matplotlib requests

### 3. Execução

**Para o Pipeline de ETL (Projeto 1):**

1. Crie o arquivo `segredos.txt` na raiz do projeto com seu usuário e senha do Mongo.
2. Execute o comando:

```bash
python pipeline_de_dados.py

**Para a Clínica de Estética (Projeto 2):**

Execute o script abaixo e insira suas credenciais quando solicitado pelo terminal:

```bash
python pipeline_com_agenda.py