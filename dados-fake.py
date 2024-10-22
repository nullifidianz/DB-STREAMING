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

        print("Dados inseridos com sucesso")
    except Exception as e:
        print(f"Erro ao inserir dados: {e}")

if __name__ == "__main__":
    main()
