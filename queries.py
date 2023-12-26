import psycopg2
from psycopg2 import OperationalError
from commands_sql import SQLD
from database_config import create_connection

FALHA_CONEXAO = "ERRO AO CONECTAR AO BANCO DE DADOS"
SUCESSO_CONEXAO = "SUCESSO AO CONECTAR AO BANCO DE DADOS"
SUCESSO_CRIAR_BANCO = "SUCESSO AO CRIAR BANCO DE DADOS"

#Letra a) Dado um produto, listar os 5 comentários mais úteis e com maior avaliação e os 5 comentários mais úteis e com menor avaliação
def query_A(asin): 
    connection = create_connection(False, "teste1")
    if (connection[0] == FALHA_CONEXAO):
        return
    cursor = connection[1].cursor()
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
        print("\n") 
    except Exception as error:
        print("Aconteceu um erro: ",error) 
    finally:
        cursor.close()
        connection[1].close() 

# Letra b) Dado um produto, listar os produtos similares com maiores vendas do que ele              
def query_B(asin):
    connection = create_connection(False, "teste1")
    if (connection[0] == FALHA_CONEXAO):
        return
    cursor = connection[1].cursor()
    try:
        cursor.execute(SQLD.LETRA_B,(asin,))
        print("Respondendo a letra b): \n")
        print("\nASIN | PRODUTO SIMILAR\n")
        linhas = cursor.fetchall()
        for linha in linhas:
            print(linha)
        print("\n")    
    except Exception as error:
        print("Aconteceu um erro: ",error)
    finally:
        cursor.close()
        connection[1].close() 

#Letra c) Dado um produto, mostrar a evolução diária das médias de avaliação ao longo do intervalo de tempo coberto no arquivo de entrada 
def query_C(asin): 
    connection = create_connection(False, "teste1")
    if (connection[0] == FALHA_CONEXAO):
        return
    cursor = connection[1].cursor()
    try:
        cursor.execute(SQLD.LETRA_C,(asin,))
        print("Respondendo a letra c): \nProduto: {}".format(asin))
        print("Data YMD   | Media das Avaliacoes")
        dict_aux = {}
        linhas = cursor.fetchall()
        for linha in linhas:
            dict_aux = {"data":linha[0], "media":linha[1]}
            print("{} | {:.2f}".format(dict_aux['data'],dict_aux['media']))
    except Exception as error:
        print("Aconteceu um erro: ",error)
    finally:    
        cursor.close()
        connection[1].close()

#Letra d) Listar os 10 produtos líderes de venda em cada grupo de produtos
def query_D():
    connection = create_connection(False, "teste1")
    if (connection[0] == FALHA_CONEXAO):
        return
    cursor = connection[1].cursor()
    try:
        cursor.execute("""SELECT DISTINCT grupo FROM produto""")
        grupos = cursor.fetchall()
        
        print("Respondendo questao letra b)\nOs itens estão descrito na ordem decrescente, ou seja, do mais vendido pro menos vendido")
        for grupo in grupos:
            print("Grupo: ",grupo[0])
            print("ASIN | TITULO | RANK DE VENDAS")
            cursor.execute(SQLD.LETRA_D,(grupo,))
            linhas = cursor.fetchall()
            
            for linha in linhas:
                print(linha[1:])   
    except Exception as error:
        print(error)
    finally:
        cursor.close()
        connection[1].close() 

#Letra e) Listar os 10 produtos com a maior média de avaliações úteis positivas por produto
def query_E():
    connection = create_connection(False, "teste1")
    if (connection[0] == FALHA_CONEXAO):
        return
    cursor = connection[1].cursor()
    try:
        cursor.execute(SQLD.LETRA_E)
        print("Respondendo letra e):\n")
        print("ASIN | MEDIA AVALIACOES POSITIVAS")

        dict_aux = {}
        linhas = cursor.fetchall()
        for linha in linhas:
            dict_aux = {"asin":linha[0],"media":linha[1]}
            print("{}  {:.2f}".format(dict_aux['asin'],float(dict_aux['media'])))
        
    except Exception as error:
        print(error)
    finally:
        cursor.close()
        connection[1].close() 

#Letra f) Listar a 5 categorias de produto com a maior média de avaliações úteis positivas por produto
def query_F():
    connection = create_connection(False, "teste1")
    if (connection[0] == FALHA_CONEXAO):
        return 
    cursor = connection[1].cursor()
    try:
        cursor.execute(SQLD.LETRA_F)
        print("Respondendo a questao f):\n")
        print("CATEGORIAS | MEDIA AVALIACAO UTIL")
        linhas = cursor.fetchall()

        dict_aux = {}
        for linha in linhas:
            dict_aux = {"categories":linha[0],"media":linha[1]}
            print("{}  {:.2f}".format(dict_aux['categories'],float(dict_aux['media'])))
    except Exception as error:
        print("Aconteceu um erro: ",error)
    finally:   
        cursor.close()
        connection[1].close()

#Letra g) Listar os 10 clientes que mais fizeram comentários por grupo de produto
def query_G():
    connection = create_connection(False, "teste1")
    if (connection[0] == FALHA_CONEXAO):
        return 
    cursor = connection[1].cursor()
    try:    
        print("Respondendo a questao g): \n")
        print("GRUPO | ID_USUARIO | TOTAL COMENTARIOS")
        cursor.execute("""SELECT DISTINCT grupo FROM produto""")
        grupos = cursor.fetchall()
        for grupo in grupos:
            print("\nGRUPO: {}".format(grupo[0]))
            cursor.execute(SQLD.LETRA_G,(grupo,))
            linhas = cursor.fetchall()
            for linha in linhas:
                print(linha)
    except Exception as error:
        print("Aconteceu um erro: ",error)
    finally:
        cursor.close()
        connection[1].close()
