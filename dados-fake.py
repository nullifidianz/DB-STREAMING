from datetime import date
import random
from faker import Faker
from supabase import create_client, Client


SUPABASE_URL = "https://<YOUR_SUPABASE_URL>.supabase.co"
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

def insere_artista(nome, data_nascimento):
    
    data_nascimento_str = data_nascimento.isoformat()
    response = supabase.table('artista').insert({"nome": nome, "data_nascimento": data_nascimento_str}).execute()
    if response.error:
        print(f"Erro ao inserir artista: {response.error}")
    return response.data[0]['id']

def insere_musica(titulo, duracao):
    response = supabase.table('musica').insert({"titulo": titulo, "duracao": duracao}).execute()
    if response.error:
        print(f"Erro ao inserir musica: {response.error}")
    return response.data[0]['id']

def insere_disco(titulo, data_lancamento):
    
    data_lancamento_str = data_lancamento.isoformat()
    response = supabase.table('disco').insert({"titulo": titulo, "data_lancamento": data_lancamento_str}).execute()
    if response.error:
        print(f"Erro ao inserir disco: {response.error}")
    return response.data[0]['id']

def junta_musica_no_disco(id_musica, id_disco):
    response = supabase.table('Disco_Musica').insert({"id_disco": id_disco, "id_musica": id_musica}).execute()
    if response.error:
        print(f"Erro ao vincular música ao disco: {response.error}")

def artista_musica(id_artista, id_musica):
    response = supabase.table('Artista_Musica').insert({"id_artista": id_artista, "id_musica": id_musica}).execute()
    if response.error:
        print(f"Erro ao vincular artista à música: {response.error}")

def main():
    try:
        for _ in range(10):
            nome, data_nascimento = dados_artista()
            id_artista = insere_artista(nome, data_nascimento)

            titulo, data_lancamento = dados_disco()
            id_disco = insere_disco(titulo, data_lancamento)

            for _ in range(10):
                titulo, duracao = dados_musica()
                id_musica = insere_musica(titulo, duracao)

                junta_musica_no_disco(id_musica, id_disco)
                artista_musica(id_artista, id_musica)

        print("Dados inseridos com sucesso")
    except Exception as e:
        print(f"Erro ao inserir dados: {e}")

if __name__ == "__main__":
    main()
