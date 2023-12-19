import psycopg2
from psycopg2 import OperationalError
import configparser

FALHA_CONEXAO = "ERRO AO CONECTAR AO BANCO DE DADOS"
SUCESSO_CONEXAO = "SUCESSO AO CONECTAR AO BANCO DE DADOS"
SUCESSO_CRIAR_BANCO = "SUCESSO AO CRIAR BANCO DE DADOS"

def create_connection():
    config = configparser.ConfigParser()
    config.read('db_config.ini')

    try:
        connection = psycopg2.connect(
            host=config['database']['host'],
            database=config['database']['dbname'],
            user=config['database']['user'],
            password=config['database']['password']
        )

        cursor = connection.cursor()        
        cursor.execute("SELECT version();")
        cursor.close()
        
        return SUCESSO_CONEXAO, connection
    except OperationalError as e:
        return FALHA_CONEXAO, str(e)
    
def create_database(connection, database_name):
    if (connection[0] == FALHA_CONEXAO):
        return
    
    try:
        COMANDO_SQL = "CREATE DATABASE {}".format(database_name)

        cursor = connection[1].cursor()
        
        connection[1].autocommit = True
        cursor.execute(COMANDO_SQL)
        connection[1].autocommit = False
        cursor.close()

        return SUCESSO_CRIAR_BANCO
    except OperationalError as e:
        return FALHA_CONEXAO, str(e)

connection = create_connection()
create_database(connection, "tp1_test")

connection[1].close()