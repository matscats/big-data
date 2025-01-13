import psycopg2
import faker
import random
import atexit

conn = psycopg2.connect(
        dbname="authdb",  # Default DB
        user="user",
        password="password",
        host="localhost",
        port="5432"
    )
conn.autocommit = True
cur = conn.cursor()
fake = faker.Faker()

def registerFake(login=None, password=None):
    username = login
    pswd = password
    if login is None:
        username = fake.user_name()
    if password is None:
        pswd = "coxinha"+fake.date_of_birth(pattern="%d%m")
    
    user = (username, pswd)

    query = f"""INSERT INTO AUTENTICACAO VALUES
    {user};"""
    try:
        cur.execute(query)
    except psycopg2.errors.UniqueViolation as e:
        print(f"O usuário {e.diag.message_detail.split("=")[1].split(")")[0][1:] } já existe")
        return -1
    return 0

def addIntegration(user=None, type=None, genUser=True):
    username = user
    option = type

    if genUser:
        if user is None:
            username = fake.user_name() 
        if registerFake(username) == -1:
            print("desabilite a geração aleatória ou escolha outro nome")
            return

    if username is None:
        print("Forneça o nome do usuário ou habilite a geração aleatória de usuários")

    if type is None:
        options = ["Spotify", "Deezer", "YtMusic", "Shazam"]
        option = random.choice(options)

    token = (username, option, fake.uuid4())
    
    query = f"""INSERT INTO INTEGRACOES VALUES
    {token};"""
    try: 
        cur.execute(query)
    except psycopg2.errors.UniqueViolation as e:
        print(f"A tupla ({e.diag.message_detail.split("=")[1].split(")")[0][1:]}) já existe")
        return -1
    return

def showTables():
    query = "SELECT * FROM AUTENTICACAO"
    cur.execute(query)
    res = cur.fetchall()
    cols = [desc[0] for desc in cur.description]
    print("TABELA AUTENTICACOES " +40*"-")
    print("\t".join(map(lambda i: str(i)[:12].ljust(12, " "), cols)))
    for tupla in res:
        print("\t".join(map(lambda i: str(i)[:12].ljust(12, " "), tupla)))
    
    print("\nTABELA INTEGRACOES " +40*"-")
    query = "SELECT * FROM INTEGRACOES"
    cur.execute(query)
    res = cur.fetchall()
    cols = [desc[0] for desc in cur.description]
    print("\t".join(map(lambda i: str(i)[:10].ljust(10, " "), cols)))
    for tupla in res:
        print("\t".join(map(lambda i: str(i)[:10].ljust(10, " "), tupla)))


registerFake("O TESTE")
addIntegration("O TESTE", "TESTANDO", genUser=False)
showTables()

def cleanup():
    cur.close()
    conn.close()
atexit.register(cleanup)