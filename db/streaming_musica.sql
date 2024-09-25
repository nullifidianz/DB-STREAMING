CREATE DATABASE streaming_musica;

CREATE TABLE Artista (
    id_artista SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    data_nascimento DATE
);
CREATE TABLE Disco (
    id_disco SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    data_lancamento DATE,
    id_artista INT,
    FOREIGN KEY (id_artista) REFERENCES Artista(id_artista)
);
CREATE TABLE Musica (
    id_musica SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    duracao INT
);
CREATE TABLE Usuario (
    id_usuario SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    data_registro DATE
);
CREATE TABLE Playlist (
    id_playlist SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    id_usuario INT,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
);
CREATE TABLE Artista_Musica (
    id_artista INT,
    id_musica INT,
    PRIMARY KEY (id_artista, id_musica),
    FOREIGN KEY (id_artista) REFERENCES Artista(id_artista),
    FOREIGN KEY (id_musica) REFERENCES Musica(id_musica)
);
CREATE TABLE Disco_Musica (
    id_disco INT,
    id_musica INT,
    PRIMARY KEY (id_disco, id_musica),
    FOREIGN KEY (id_disco) REFERENCES Disco(id_disco),
    FOREIGN KEY (id_musica) REFERENCES Musica(id_musica)
);
CREATE TABLE Playlist_Musica (
    id_playlist INT,
    id_musica INT,
    PRIMARY KEY (id_playlist, id_musica),
    FOREIGN KEY (id_playlist) REFERENCES Playlist(id_playlist),
    FOREIGN KEY (id_musica) REFERENCES Musica(id_musica)
);
