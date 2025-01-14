import psycopg2
import faker
import random

FORCE_NEW = True

def create_database(force_new=True):

    conn = psycopg2.connect(
        dbname="postgres",  # Default DB
        user="user",
        password="password",
        host="localhost",
        port="5432"
    )
    conn.autocommit = True
    cur = conn.cursor()

    if force_new: 
        try: 
            cur.execute("DROP DATABASE authdb;")
        except psycopg2.errors.InvalidCatalogName:
            print("Ou você está executando isso pela primeira vez ou o FORCE_NEW não funcionou")

    try:
        cur.execute("CREATE DATABASE authdb;")
    except Exception as e:
        print(f"Das três uma: você esqueceu de abrir o servidor; você já rodou esse script; ou deu erro mesmo")
        print(f"Erro: {e}")
        exit(1)
    print("Suçesso no database.")

    cur.close()
    conn.close()

def setup_tables():
    conn = psycopg2.connect(
        dbname="authdb",  # Default DB
        user="user",
        password="password",
        host="localhost",
        port="5432"
    )
    conn.autocommit = True
    cur = conn.cursor()

    query="""CREATE TABLE AUTENTICACAO (
    usuario VARCHAR(255) PRIMARY KEY,
    senha VARCHAR(255) NOT NULL
);"""
    cur.execute(query)

    query="""CREATE TABLE INTEGRACOES (
    usuario VARCHAR(255) NOT NULL,
    servico VARCHAR(255) NOT NULL,
    token VARCHAR(255) NOT NULL,
    PRIMARY KEY (usuario, servico),
    FOREIGN KEY (usuario) REFERENCES AUTENTICACAO(usuario)
);"""
    cur.execute(query)
    
    cur.execute("""
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';
""")

    if len(cur.fetchall()) == 2:
        print("Susseço nas tabelas.")
    else:
        print("Algo de errado aconteceu nas tabelas")

def populate_tables(N=10):
    fake = faker.Faker()
    users = [
        (fake.user_name(),
        "coxinha"+fake.date_of_birth(pattern="%d%m")) for _ in range(N)
    ]

    options = ["Spotify", "Deezer", "YtMusic", "Shazam"]

    tokens = [
        (info[0], random.choice(options), fake.uuid4()) for info in users
    ]
    
    conn = psycopg2.connect(
        dbname="authdb",  # Default DB
        user="user",
        password="password",
        host="localhost",
        port="5432"
    )
    conn.autocommit = True
    cur = conn.cursor()

    query = f"""INSERT INTO AUTENTICACAO VALUES
    """ + ",\n    ".join(map(str, users)) + ";"
    cur.execute(query)
    
    query = f"""INSERT INTO INTEGRACOES VALUES
    """ + ",\n    ".join(map(str, tokens)) + ";"
    cur.execute(query)

    #print(users)
    #print(tokens)

    query = "SELECT * FROM AUTENTICACAO"
    cur.execute(query)
    res1 = len(cur.fetchall())
    
    query = "SELECT * FROM INTEGRACOES"
    cur.execute(query)
    res2 = len(cur.fetchall())
    if res1 == res2 and res1 > 0:
        print("Çusseso nas insercões.")
    else:
        print("ish (inserção)")

create_database(FORCE_NEW)
setup_tables()
populate_tables()