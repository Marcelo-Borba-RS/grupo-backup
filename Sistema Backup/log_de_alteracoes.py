import os
from datetime import datetime


file_path = 'C:\\Users\\Administrador\\Documents\\Dados\\consolidado.parquet'


# Get the modification time as a timestamp (float)

m_time_timestamp = os.path.getmtime(file_path)


# Convert the timestamp to a readable datetime object

m_time_datetime = datetime.fromtimestamp(m_time_timestamp)


print(f"Last modified date: {m_time_datetime}")

# You can format the output string as needed

print(f"Formatted date: {m_time_datetime.strftime('%Y-%m-%d')}")