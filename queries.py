import psycopg2
from psycopg2 import OperationalError
from commands_sql import SQLD
from database_config import create_connection

FALHA_CONEXAO = "ERRO AO CONECTAR AO BANCO DE DADOS"
SUCESSO_CONEXAO = "SUCESSO AO CONECTAR AO BANCO DE DADOS"
SUCESSO_CRIAR_BANCO = "SUCESSO AO CRIAR BANCO DE DADOS"

def query_A(asin):
    connection = create_connection(False, "teste1")
    if (connection[0] == FALHA_CONEXAO):
        return
    
    cursor = connection[1].cursor()
    
    #Letra a) Dado um produto, listar os 5 comentários mais úteis e com maior avaliação e os 5 comentários mais úteis e com menor avaliação
    try:
        print("Respondendo questao letra a) \n")
        print("Os 5 comentarios mais uteis e com maior avaliacao:")
        cursor.execute(SQLD.LETRA_A1P,(asin,))
        print("ASIN | DATE (YMD) | COSTUME | NOTA | VOTOS | VOTOS UTEIS \n")
        linhas = cursor.fetchall()
    
        for linha in linhas:
            print(linha[1:])

        print("\nOs 5 comentarios mais uteis e com menor avaliacao:")    
        cursor.execute(SQLD.LETRA_A2P,(asin,))
        print("ASIN | DATE (YMD) | COSTUME | NOTA | VOTOS | VOTOS UTEIS \n")
        linhas = cursor.fetchall()
    
        for linha in linhas:
            print(linha[1:])

    except Exception as error:
        print("Aconteceu um erro ",error)        

def query_D():
    connection = create_connection(False, "teste1")
    if (connection[0] == FALHA_CONEXAO):
        return
    try:
        cursor = connection[1].cursor()
        
        cursor.execute("""SELECT DISTINCT grupo FROM produto""")
        grupos = cursor.fetchall()
        print("Respondendo questao letra b)\n")
        for grupo in grupos:
            print("Grupo: ",grupo[0])
            print("ASIN | TITULO | RANK DE VENDAS")
            cursor.execute(SQLD.LETRA_D,(grupo,))

            linhas = cursor.fetchall()
            for linha in linhas:
                print(linha[1:])
    except Exception as error:
        print(error)

def query_E():
    connection = create_connection(False, "teste1")
    if (connection[0] == FALHA_CONEXAO):
        return
    try:
        cursor = connection[1].cursor()
        cursor.execute(SQLD.LETRA_E)
        print("Respondendo letra e):\n")
        print("ASIN | MEDIA AVALIACOES POSITIVAS")

        listaTMP = {}
        linhas = cursor.fetchall()
        for linha in linhas:
            listaTMP = {"asin":linha[0],"media":linha[1]}
            print("{} {:.2f}".format(listaTMP['asin'],float(listaTMP['media'])))
        
    except Exception as error:
        print(error)