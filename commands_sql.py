
# Classe com as querys SLQ utilizadas no programa.
class SQLC:

    CRIAR_TABELA = """CREATE DATABASE {};"""

    TABELA_PRODUTO = """CREATE TABLE IF NOT EXISTS public.produto (
        asin character varying(15) COLLATE pg_catalog."default" NOT NULL,
        titulo character varying(500) COLLATE pg_catalog."default" NOT NULL,
        grupo character varying(20) COLLATE pg_catalog."default" NOT NULL,
        rank_vendas integer NOT NULL,
        PRIMARY KEY (asin)
    );
    """

    TABELA_SIMILAR = """CREATE TABLE IF NOT EXISTS produto_similar (
        asin VARCHAR(15) NOT NULL,
        asin_similar VARCHAR(15) NOT NULL,
        PRIMARY KEY (asin, asin_similar),
        FOREIGN KEY (asin) REFERENCES produto(asin) ON DELETE CASCADE
    );
    """

    TABELA_CATEGORIAS = """CREATE TABLE IF NOT EXISTS categorias (
        categoria_id integer NOT NULL,
        categoria_nome character varying(100) NOT NULL,
        PRIMARY KEY (categoria_id)
    );
    """

    TABELA_P_CATEGORIA = """CREATE TABLE IF NOT EXISTS produto_categoria (
        asin character varying(15) NOT NULL,
        categoria_id integer NOT NULL,
        PRIMARY KEY (asin, categoria_id),
        FOREIGN KEY (asin) REFERENCES produto(asin) ON DELETE CASCADE,
        FOREIGN KEY (categoria_id) REFERENCES categorias(categoria_id) ON DELETE CASCADE
    );
    """

    TABELA_AVALIACOES = """CREATE TABLE IF NOT EXISTS avaliacoes (
        avaliacao_id integer NOT NULL,
        asin character varying(15) NOT NULL,
        data date NOT NULL,
        id_usuario character varying(15) NOT NULL,
        nota integer NOT NULL,
        votos integer NOT NULL,
        votos_util integer NOT NULL,
        PRIMARY KEY (avaliacao_id, asin, id_usuario),
        FOREIGN KEY (asin) REFERENCES produto(asin) ON DELETE CASCADE
    );
    """

    INSERE_PRODUTO_CATEGORIA = """INSERT INTO produto_categoria(asin, categoria_id)
    VALUES %s;"""

    INSERE_PRODUTO_SIMILAR = """INSERT INTO produto_similar(asin, asin_similar) VALUES %s;"""

    INSERE_CATEGORIAS = """INSERT INTO categorias(categoria_id, categoria_nome) VALUES (%s,%s);"""

    INSERE_AVALIACOES = """INSERT INTO avaliacoes(avaliacao_id, asin, data, id_usuario, nota, votos, votos_util) VALUES %s;"""

    INSERE_PRODUTO = """INSERT INTO produto(asin, titulo, grupo, rank_vendas) VALUES %s;"""

# Classe com as query SQL para a dashboard do programa
class SQLD:
    LETRA_A1P = """SELECT * FROM avaliacoes
                WHERE asin = (%s)
                ORDER BY votos_util DESC, nota DESC
                LIMIT 5;"""
    
    LETRA_A2P = """ SELECT * FROM avaliacoes
                WHERE asin = %s
                ORDER BY votos_util DESC, nota ASC
                LIMIT 5; """
    
    LETRA_B = """ SELECT p2.* FROM produto_similar ps
                INNER JOIN produto p1 ON p1.asin = ps.asin
                INNER JOIN produto p2 ON p2.asin = ps.asin_similar
                WHERE p1.asin = %s AND p2.rank_vendas > p1.rank_vendas; """
    
    LETRA_C = """SELECT data, AVG(nota) as media_avaliacao
                FROM avaliacoes
                WHERE asin = %s'
                GROUP BY data
                ORDER BY data;"""
    
    LETRA_D = """
                SELECT grupo, asin, titulo, rank_vendas
                FROM produto
                WHERE grupo = %s
                ORDER BY grupo, rank_vendas ASC
                FETCH FIRST 10 ROWS ONLY;"""
    
    LETRA_E = """SELECT a.asin, AVG(a.votos_util) as media_votos_util
                FROM avaliacoes a
                INNER JOIN produto p ON p.asin = a.asin
                GROUP BY a.asin
                ORDER BY media_votos_util DESC
                LIMIT 10;"""
    
    LETRA_F = """SELECT c.categoria_nome, AVG(a.votos_util) as media_votos_util
                FROM avaliacoes a
                INNER JOIN produto_categoria pc ON pc.asin = a.asin
                INNER JOIN categorias c ON c.categoria_id = pc.categoria_id
                GROUP BY c.categoria_nome
                ORDER BY media_votos_util DESC
                LIMIT 5;"""

    LETRA_G = """SELECT p.grupo, a.id_usuario, COUNT(*) as total_comentarios
                FROM avaliacoes a
                INNER JOIN produto p ON p.asin = a.asin
                WHERE p.grupo = %s
                GROUP BY p.grupo, a.id_usuario
                ORDER BY p.grupo, total_comentarios DESC
                LIMIT 10;"""
    


"""SELECT p1.asin, p2.titulo,p2.rank_vendas as rank_vendas_similar FROM produto_similar p1
JOIN produto p2 ON p1.asin = p2.asin
WHERE p1.asin = '0878571256' AND p2.rank_vendas > (
SELECT rank_vendas FROM produto WHERE asin='0878571256'
);"""    