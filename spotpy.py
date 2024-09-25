import random
import psycopg2
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Configuração do Spotify
SPOTIFY_CLIENT_ID = 'seu-client-id-aqui'
SPOTIFY_CLIENT_SECRET = 'seu-client-secret-aqui'

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID,
                                                                client_secret=SPOTIFY_CLIENT_SECRET))

# Função para conectar ao banco de dados PostgreSQL
def connect_db():
    return psycopg2.connect(
        host="localhost",
        database="streaming_musica",
        user="seu-usuario",
        password="sua-senha"
    )

# Função para buscar um artista do Spotify
def get_spotify_artist():
    results = spotify.search(q='genre:pop', type='artist', limit=1)
    artist = results['artists']['items'][0]
    name = artist['name']
    followers = artist['followers']['total']  # Podemos usar os seguidores como proxy para popularidade
    return name, followers

# Função para inserir dados na tabela Artista
def insert_artist(conn, name):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO Artista (nome, data_nascimento)
            VALUES (%s, %s)
            RETURNING id_artista;
        """, (name, None))  # Não temos a data de nascimento do Spotify
        return cur.fetchone()[0]

# Função para buscar álbuns do Spotify
def get_spotify_album(artist_id):
    albums = spotify.artist_albums(artist_id, album_type='album', limit=1)
    album = albums['items'][0]
    title = album['name']
    release_date = album['release_date']
    return title, release_date

# Função para inserir dados na tabela Disco
def insert_album(conn, title, release_date, artist_id):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO Disco (titulo, data_lancamento, id_artista)
            VALUES (%s, %s, %s)
            RETURNING id_disco;
        """, (title, release_date, artist_id))
        return cur.fetchone()[0]

# Função para buscar músicas de um álbum do Spotify
def get_spotify_tracks(album_id):
    tracks = spotify.album_tracks(album_id, limit=5)
    return [(track['name'], track['duration_ms'] // 1000) for track in tracks['items']]

# Função para inserir dados na tabela Musica
def insert_song(conn, title, duration):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO Musica (titulo, duracao)
            VALUES (%s, %s)
            RETURNING id_musica;
        """, (title, duration))
        return cur.fetchone()[0]

# Função para associar músicas a um disco
def insert_song_to_album(conn, album_id, song_id):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO Disco_Musica (id_disco, id_musica)
            VALUES (%s, %s);
        """, (album_id, song_id))

# Função para associar artista a uma música
def insert_artist_to_song(conn, artist_id, song_id):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO Artista_Musica (id_artista, id_musica)
            VALUES (%s, %s);
        """, (artist_id, song_id))

def main():
    conn = connect_db()
    
    try:
        # Buscar e inserir artistas e seus álbuns e músicas do Spotify
        for _ in range(5):  # Buscar 5 artistas
            # Obter e inserir artista
            artist_name, artist_followers = get_spotify_artist()
            artist_id = insert_artist(conn, artist_name)
            
            # Obter e inserir álbum
            album_title, release_date = get_spotify_album(artist_id)
            album_id = insert_album(conn, album_title, release_date, artist_id)
            
            # Obter e inserir músicas do álbum
            tracks = get_spotify_tracks(album_id)
            for track_name, duration in tracks:
                song_id = insert_song(conn, track_name, duration)
                
                # Associar música ao álbum
                insert_song_to_album(conn, album_id, song_id)
                
                # Associar artista à música
                insert_artist_to_song(conn, artist_id, song_id)
        
        conn.commit()  # Salva todas as inserções no banco
        print("Dados inseridos com sucesso!")
    
    except Exception as e:
        conn.rollback()  # Desfaz as alterações em caso de erro
        print(f"Erro ao inserir dados: {e}")
    
    finally:
        conn.close()

if __name__ == "__main__":
    main()
