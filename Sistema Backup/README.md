# 🛡️ Pipeline de ETL Seguro: Excel para Parquet com MongoDB

Este projeto consiste em um script Python de **Engenharia de Dados** focado no processamento seguro de informações sensíveis (em conformidade com a **LGPD**). 

O sistema automatiza a leitura de múltiplos arquivos Excel (legados e modernos), aplica criptografia em dados pessoais, consolida as informações em formato performático (**Parquet**) para uso em Power BI e registra logs de auditoria em um banco de dados na nuvem (**MongoDB Atlas**).

---

## 🚀 Funcionalidades Principais

* **🕵️ Leitura Inteligente:** Detecta e processa automaticamente arquivos `.xls`, `.xlsx`, `.xlsm` e `.xlsb` em uma pasta dinâmica.
* **🔒 Segurança e Privacidade (LGPD):** * Utiliza a biblioteca `cryptography` (Algoritmo Fernet) para criptografar colunas sensíveis como *Nome, CNS, Telefone e Profissional*.
    * Credenciais de banco de dados segregadas do código fonte via leitura de arquivo local (`segredos.txt`).
* **⚡ Alta Performance:** Converte bases de dados volumosas para **Parquet** (formato colunar), ideal para leituras rápidas em ferramentas de BI.
* **☁️ Auditoria em Nuvem:** Registra logs de execução e modificação de arquivos diretamente no **MongoDB Atlas**, permitindo rastreabilidade do processo.
* **🛡️ Tratamento de Erros:** Sistema robusto de logs locais e tratamento de exceções para arquivos corrompidos ou extensões inválidas.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.x
* **Manipulação de Dados:** Pandas, NumPy
* **Formatos e Drivers:** PyArrow (Parquet), OpenPyXL, XLRD, PyXLSB
* **Banco de Dados NoSQL:** PyMongo (MongoDB Atlas)
* **Criptografia:** Cryptography (Fernet)
* **Sistema:** OS, Glob, Sys

---

## ⚙️ Pré-requisitos e Instalação

Para rodar este projeto localmente, siga os passos abaixo:

### 1. Clone o repositório
```bash
git clone [https://github.com/Marcelo-Borba-RS/grupo-backup]