import os
import json
import logging
from dotenv import load_dotenv
from modules.mysql.extractor import *
from modules.msqlserver.extractor import *

# Carrega as variaveis de ambiente do arquivo .env
load_dotenv()
json_config_mysql = os.getenv("JSON_CONFIG_BIGQUERY_DBNAME")
json_config_mysql = json.loads(json_config_mysql)

# Verifica se o diretório 'logs' existe, se não, cria o diretório
log_directory = 'logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Caminho completo do arquivo de log
log_file_path = os.path.join(log_directory, 'process.log')

# Verifica se o arquivo de log existe, se não, cria o arquivo
if not os.path.exists(log_file_path):
    with open(log_file_path, 'w') as file:
        pass  # Cria um arquivo vazio

# Configura o log
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')