from datetime import date
import random
from faker import Faker
from supabase import create_client, Client

SUPABASE_URL = "<YOUR_SUPABASE_URL>"
SUPABASE_KEY = "<YOUR_SUPABASE_KEY>"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
fake = Faker('pt_BR')

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

def dados_usuario():
    nome = fake.name()
    email = fake.email()
    data_registro = fake.date()
    return nome, email, data_registro

def dados_playlist():
    titulo = fake.sentence(nb_words=3)
    return titulo

def insere_artista(nome, data_nascimento):
    data_nascimento_str = data_nascimento.isoformat()
    response = (
        supabase.table('artista')
        .insert({"nome": nome, "data_nascimento": data_nascimento_str})
        .execute()
    )
    return response.data[0]['id_artista']

def insere_musica(titulo, duracao):
    response = supabase.table('musica').insert({"titulo": titulo, "duracao": duracao}).execute()
    return response.data[0]['id_musica']

def insere_disco(titulo, data_lancamento, id_artista):
    response = (
        supabase.table('disco')
        .insert({"titulo": titulo, "data_lancamento": data_lancamento, "id_artista": id_artista})
        .execute()
    )
    return response.data[0]['id_disco']

def insere_usuario(nome, email, data_registro):
    response = (
        supabase.table('usuario')
        .insert({"nome": nome, "email": email, "data_registro": data_registro})
        .execute()
    )
    return response.data[0]['id_usuario']

def insere_playlist(titulo, id_usuario):
    response = (
        supabase.table('playlist')
        .insert({"titulo": titulo, "id_usuario": id_usuario})
        .execute()
    )
    return response.data[0]['id_playlist']

# Funções de relacionamento
def junta_musica_no_disco(id_musica, id_disco):
    supabase.table('disco_musica').insert({"id_disco": id_disco, "id_musica": id_musica}).execute()

def artista_musica(id_artista, id_musica):
    supabase.table('artista_musica').insert({"id_artista": id_artista, "id_musica": id_musica}).execute()

def playlist_musica(id_playlist, id_musica):
    supabase.table('playlist_musica').insert({"id_playlist": id_playlist, "id_musica": id_musica}).execute()

def insere_dados_musicas():
    artistas = [
        {"nome": "Queen", "data_nascimento": "1970-01-01"},
        {"nome": "Pink Floyd", "data_nascimento": "1965-01-01"},
        {"nome": "The Beatles", "data_nascimento": "1960-01-01"},
        {"nome": "John Lennon", "data_nascimento": "1940-10-09"},
    ]

    discos = [
        {"titulo": "A Night at the Opera", "data_lancamento": "1975-11-21", "artista": "Queen"},
        {"titulo": "The Dark Side of the Moon", "data_lancamento": "1973-03-01", "artista": "Pink Floyd"},
        {"titulo": "Abbey Road", "data_lancamento": "1969-09-26", "artista": "The Beatles"},
        {"titulo": "Imagine", "data_lancamento": "1971-09-09", "artista": "John Lennon"},
    ]

    musicas = [
        {"titulo": "Bohemian Rhapsody", "duracao": 354, "disco": "A Night at the Opera", "artista": "Queen"},
        {"titulo": "Dark Side of the Moon", "duracao": 423, "disco": "The Dark Side of the Moon", "artista": "Pink Floyd"},
        {"titulo": "Abbey Road", "duracao": 260, "disco": "Abbey Road", "artista": "The Beatles"},
        {"titulo": "Imagine", "duracao": 183, "disco": "Imagine", "artista": "John Lennon"},
    ]

    artista_ids = {}
    for artista in artistas:
        id_artista = insere_artista(artista['nome'], datetime.strptime(artista['data_nascimento'], '%Y-%m-%d').date())
        artista_ids[artista['nome']] = id_artista

    disco_ids = {}
    for disco in discos:
        id_artista = artista_ids[disco['artista']]
        id_disco = insere_disco(disco['titulo'], disco['data_lancamento'], id_artista)
        disco_ids[disco['titulo']] = id_disco

    for musica in musicas:
        id_musica = insere_musica(musica['titulo'], musica['duracao'])
        id_disco = disco_ids[musica['disco']]
        id_artista = artista_ids[musica['artista']]
        
        junta_musica_no_disco(id_musica, id_disco)
        artista_musica(id_artista, id_musica)

    print("Músicas e dados inseridos com sucesso.")

def main():
    try:
        for _ in range(10):
            nome_usuario, email, data_registro = dados_usuario()
            id_usuario = insere_usuario(nome_usuario, email, data_registro)

            nome_artista, data_nascimento = dados_artista()
            id_artista = insere_artista(nome_artista, data_nascimento)

            titulo_disco, data_lancamento = dados_disco()
            id_disco = insere_disco(titulo_disco, data_lancamento, id_artista)

            for _ in range(10):
                titulo_musica, duracao = dados_musica()
                id_musica = insere_musica(titulo_musica, duracao)

                junta_musica_no_disco(id_musica, id_disco)
                artista_musica(id_artista, id_musica)

            titulo_playlist = dados_playlist()
            id_playlist = insere_playlist(titulo_playlist, id_usuario)
            for _ in range(10):
                id_musica = insere_musica(titulo_musica, duracao)
                playlist_musica(id_playlist, id_musica)

        insere_dados_musicas()
        print("Dados inseridos com sucesso")
    except Exception as e:
        print(f"Erro ao inserir dados: {e}")

if __name__ == "__main__":
    main()

