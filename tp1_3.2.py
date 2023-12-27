from database_config import *

#Criar a database     
teste = create_connection()
create_database(teste,"teste1")

#Criar as tabelas
teste = create_connection(False,"teste1")
create_tables(teste)

#Ler o arquivo de entrada e povoar as tabelas
teste = create_connection(False,"teste1")
products = parse_products("amazon-meta-sample.txt")
insert_data(teste, products)