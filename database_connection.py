
import psycopg2
from psycopg2 import OperationalError
import configparser

# Definindo constantes públicas para o status da conexão
CONNECTION_SUCCESS = "Conexão bem-sucedida"
CONNECTION_FAILURE = "Erro ao conectar ao banco de dados"

def connect_to_database():
    """Tenta estabelecer uma conexão com o banco de dados usando configurações de um arquivo externo."""
    # Lendo as configurações do arquivo
    config = configparser.ConfigParser()
    config.read('db_config.ini')

    try:
        # Conectar ao banco de dados usando as informações do arquivo de configuração
        connection = psycopg2.connect(
            host=config['DATABASE']['HOST'],
            database=config['DATABASE']['DBNAME'],
            user=config['DATABASE']['USER'],
            password=config['DATABASE']['PASSWORD']
        )
        
        # Cria um cursor para realizar operações no banco de dados
        cursor = connection.cursor()
        
        # Executar um comando SQL para testar a conexão
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        
        # Fechar a conexão
        cursor.close()
        connection.close()
        
        return CONNECTION_SUCCESS, db_version
    
    except OperationalError as e:
        return CONNECTION_FAILURE, str(e)


print(connect_to_database())