import psycopg2
from psycopg2 import OperationalError
import configparser
from commands_sql import SQLC

FALHA_CONEXAO = "ERRO AO CONECTAR AO BANCO DE DADOS"
SUCESSO_CONEXAO = "SUCESSO AO CONECTAR AO BANCO DE DADOS"
SUCESSO_CRIAR_BANCO = "SUCESSO AO CRIAR BANCO DE DADOS"

def create_connection(autocommit = False, database_name='postgres'):
    config = configparser.ConfigParser()
    config.read('db_config.ini')

    try:
        connection = psycopg2.connect(
            host=config['database']['host'],
            database= database_name,
            user=config['database']['user'],
            password=config['database']['password']
        )

        connection.autocommit = True

        cursor = connection.cursor()        
        cursor.execute("SELECT version();")
        cursor.close()
        return SUCESSO_CONEXAO, connection
    except OperationalError as e:
        return FALHA_CONEXAO, str(e)
    
def create_database(connection, database_name):
    
    print(connection)
    if (connection[0] == FALHA_CONEXAO):
        return
    
    try:
        COMANDO_SQL = SQLC.CRIAR_TABELA.format(database_name)
        
        cursor = connection[1].cursor()
        cursor.execute(COMANDO_SQL)
        cursor.close()

        return SUCESSO_CRIAR_BANCO
    except OperationalError as e:
        return FALHA_CONEXAO, str(e)
    finally:
        connection[1].commit()
        connection[1].close()

def create_tables(connection):
    if (connection[0] == FALHA_CONEXAO):
        return
    
    try:
        cursor = connection[1].cursor()
        
        cursor.execute(SQLC.TABELA_PRODUTO)
        cursor.execute(SQLC.TABELA_SIMILAR)
        cursor.execute(SQLC.TABELA_CATEGORIAS)
        cursor.execute(SQLC.TABELA_P_CATEGORIA)
        cursor.execute(SQLC.TABELA_AVALIACOES)
        #cursor.execute(SQLC.TESTE)

        cursor.close()
        connection[1].commit()

        return SUCESSO_CRIAR_BANCO
    except OperationalError as e:
        return FALHA_CONEXAO, str(e)
    finally:
        connection[1].close()

def insere_dados(connection):
    if (connection[0] == FALHA_CONEXAO):
        return
    try:
        cursor = connection[1].cursor()
        cursor.execute(SQLC.INSERE_PRODUTO_CATEGORIAS)

        cursor.close()
        connection[1].commit()

        return SUCESSO_CRIAR_BANCO
    except OperationalError as e:
        return FALHA_CONEXAO, str(e)
    finally:
        connection[1].close()
#teste = create_connection()
#create_database(teste,"teste1")
teste = create_connection(False,"teste1")
#create_tables(teste)
insere_dados(teste)