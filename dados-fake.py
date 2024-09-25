import random
import psycopg2
from faker import Faker

fake = Faker('pt_BR')

def connect():
    conn = psycopg2.connect(
        host="SEU-HOST",
        database="SEU-BANCO",
        user="SEU-USUARIO",
        password="SUA-SENHA"
    )
    return conn

def dados_artista():
    nome = fake.name()
    data_nascimento = fake.date_of_birth()
    return nome, data_nascimento

def dados_musica():
    titulo = fake.word()
    duracao = random.randint(90, 360)
    return titulo, duracao

def dados_disco():
    titulo = fake.sentence(nb_words=4)
    data_lancamento = fake.date()
    return titulo, data_lancamento 

def insere_artista(conn, nome, data_nascimento):
    cur = conn.cursor()
    cur.execute("INSERT INTO artista (nome, data_nascimento) VALUES (%s, %s)", (nome, data_nascimento))
    conn.commit()
    cur.close()

def insere_musica(conn, titulo, duracao):
    cur = conn.cursor()
    cur.execute("INSERT INTO musica (titulo, duracao) VALUES (%s, %s)", (titulo, duracao))
    conn.commit()
    cur.close()

def insere_disco(conn, titulo, data_lancamento):
    cur = conn.cursor()
    cur.execute("INSERT INTO disco (titulo, data_lancamento) VALUES (%s, %s)", (titulo, data_lancamento))
    conn.commit()
    cur.close()

def junta_musica_no_disco(conn, id_musica, id_disco):
    cur = conn.cursor()
    cur.execute("INSERT INTO Disco_Musica (id_disco, id_musica) VALUES (%s, %s)", (id_disco, id_musica))
    conn.commit()
    cur.close()

def artista_musica(conn, id_artista, id_musica):
    cur = conn.cursor()
    cur.execute("INSERT INTO Artista_Musica (id_artista, id_musica) VALUES (%s, %s)", (id_artista, id_musica))
    conn.commit()
    cur.close()

def main():
    conn = connect()
    
    try:
        for _ in range(10):
            nome, data_nascimento = dados_artista()
            id_artista = insere_artista(conn, nome, data_nascimento)
            
            titulo, data_lancamento = dados_disco()
            id_disco = insere_disco(conn, titulo, data_lancamento)
            
            for _ in range(10):
                titulo, duracao = dados_musica()
                id_musica = insere_musica(conn, titulo, duracao)
                
                junta_musica_no_disco(conn, id_musica, id_disco)
                artista_musica(conn, id_artista, id_musica)
        conn.commit()
        print("Dados inseridos")
    except Exception as e:
        print(f"Erro ao inserir dados: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()  