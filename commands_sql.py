
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
        id_usuario integer NOT NULL,
        nota integer NOT NULL,
        votos integer NOT NULL,
        votos_util integer NOT NULL,
        PRIMARY KEY (avaliacao_id, asin, id_usuario),
        FOREIGN KEY (asin) REFERENCES produto(asin) ON DELETE CASCADE
    );
    """

# Classe com as query SQL para a dashboard do programa
class SQLD:
    pass