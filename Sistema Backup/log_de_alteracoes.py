"""
Módulo de Auditoria de Arquivos.

Este script é responsável por verificar os metadados do sistema operacional
para identificar quando o arquivo consolidado (Parquet) foi modificado
pela última vez. Essas informações são essenciais para o Log de Auditoria.
"""

import os
from datetime import datetime

# Caminho absoluto do arquivo que será monitorado
# Nota: O uso de 'r' antes da string evita problemas com as barras invertidas do Windows
file_path = r'C:\Users\Administrador\Documents\Dados\consolidado.parquet'

try:
    # 1. Obtém o tempo de modificação do arquivo (getmtime)
    # O retorno é um 'timestamp' (número float representando segundos desde 1970)
    m_time_timestamp = os.path.getmtime(file_path)

    # 2. Converte o timestamp bruto para um objeto de data legível (datetime)
    m_time_datetime = datetime.fromtimestamp(m_time_timestamp)

    # Exibe a data completa (Data + Hora + Milissegundos)
    print(f"Data completa da última modificação: {m_time_datetime}")

    # Exibe apenas a data formatada (Ano-Mês-Dia), ideal para relatórios
    print(f"Data formatada (YYYY-MM-DD): {m_time_datetime.strftime('%Y-%m-%d')}")

except FileNotFoundError:
    print(f"Erro: O arquivo não foi encontrado no caminho: {file_path}")
except Exception as e:
    print(f"Ocorreu um erro ao ler os metadados: {e}")