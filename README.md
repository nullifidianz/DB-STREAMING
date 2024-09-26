# DB-STREAMING

# Projeto: Sistema de Streaming de Música

## Resumo

Este projeto consiste na criação de um banco de dados relacional para um sistema de streaming de música. O banco de dados foi projetado para gerenciar informações sobre **músicas**, **artistas**, **discos**, **usuários** e **playlists**. O sistema permite que usuários pesquisem músicas, criem playlists, acompanhem artistas e explorem discos. Além disso, a modelagem contempla relacionamentos entre as entidades, como a relação entre artistas e músicas, músicas e playlists, e discos e músicas.

O projeto utiliza **PostgreSQL** como banco de dados relacional e **DBeaver** para a interface de gerenciamento do banco. As queries SQL que atendem às 20 questões de álgebra relacional também estão incluídas.

## Requisitos do Sistema

1. **Música**: Cada música tem um título, uma duração (em segundos), e pode pertencer a um ou mais discos. Cada música pode ser interpretada por um ou mais artistas.
2. **Artista**: Cada artista tem um nome e uma data de nascimento.
3. **Disco**: Cada disco tem um título, uma data de lançamento e pertence a um artista específico. Um disco pode conter várias músicas.
4. **Usuário**: Cada usuário tem um nome, um e-mail (único) e uma data de registro. Os usuários podem criar e gerenciar playlists.
5. **Playlist**: Cada playlist tem um título e pertence a um único usuário. Uma playlist pode conter várias músicas, e uma música pode aparecer em várias playlists.

## Modelagem do Banco de Dados

A modelagem foi realizada usando um diagrama Entidade-Relacionamento (ER) e normalizada até a terceira forma normal (3FN). Os relacionamentos estão estruturados da seguinte forma:

- **Música** é interpretada por um ou mais **Artistas**.
- **Disco** contém várias **Músicas** e é associado a um **Artista**.
- **Usuário** cria uma ou mais **Playlists**.
- **Playlist** contém várias **Músicas**, que podem estar em várias **Playlists**.

### Diagrama Entidade-Relacionamento (ER)

O diagrama completo foi criado com as seguintes entidades e relacionamentos:

- **Música**: id_musica, titulo, duracao
- **Artista**: id_artista, nome, data_nascimento
- **Disco**: id_disco, titulo, data_lancamento
- **Usuário**: id_usuario, nome, email, data_registro
- **Playlist**: id_playlist, titulo
- **Artista_Musica**: id_artista, id_musica
- **Playlist_Musica**: id_playlist, id_musica
- **Disco_Musica**: id_disco, id_musica

## Exercícios de Álgebra Relacional

### 1. Liste o título de todas as músicas e suas durações.

```sql
SELECT titulo, duracao
FROM Musica;
```

### 2. Encontre o nome de todos os artistas que têm mais de 5 músicas em seu repertório.

```sql
SELECT a.nome
FROM Artista a
JOIN Artista_Musica am ON a.id_artista = am.id_artista
GROUP BY a.nome
HAVING COUNT(am.id_musica) > 5;

```
### 3. Encontre o nome de todos os artistas que têm mais de 5 músicas em seu repertório.

```sql
SELECT titulo
FROM Disco
WHERE data_lancamento > '2020-12-31';


```
### 4. Encontre o nome de todos os artistas que têm mais de 5 músicas em seu repertório.

```sql
SELECT m.titulo, a.nome
FROM Musica m
JOIN Artista_Musica am ON m.id_musica = am.id_musica
JOIN Artista a ON a.id_artista = am.id_artista
ORDER BY m.titulo;


```
### 5. Encontre o nome de todos os artistas que têm mais de 5 músicas em seu repertório.

```sql
SELECT p.titulo
FROM Playlist p
JOIN Playlist_Musica pm ON p.id_playlist = pm.id_playlist
JOIN Musica m ON pm.id_musica = m.id_musica
WHERE m.titulo = 'Imagine';


```
### 6. Encontre o nome de todos os artistas que têm mais de 5 músicas em seu repertório.

```sql
SELECT u.nome
FROM Usuario u
JOIN Playlist p ON u.id_usuario = p.id_usuario
JOIN Playlist_Musica pm ON p.id_playlist = pm.id_playlist
JOIN Disco_Musica dm ON pm.id_musica = dm.id_musica
JOIN Disco d ON dm.id_disco = d.id_disco
WHERE d.titulo = 'Abbey Road';


```
### 7. Encontre o nome de todos os artistas que têm mais de 5 músicas em seu repertório.

```sql
SELECT AVG(m.duracao) AS duracao_media
FROM Musica m
JOIN Artista_Musica am ON m.id_musica = am.id_musica
WHERE am.id_artista = id_artista_especifico;

```
### 8. Encontre o nome de todos os artistas que têm mais de 5 músicas em seu repertório.

```sql
SELECT a.nome
FROM Artista a
LEFT JOIN Artista_Musica am ON a.id_artista = am.id_artista
WHERE am.id_musica IS NULL;


```
### 9. Encontre o nome de todos os artistas que têm mais de 5 músicas em seu repertório.

```sql
SELECT d.titulo
FROM Disco d
JOIN Disco_Musica dm ON d.id_disco = dm.id_disco
GROUP BY d.titulo
HAVING COUNT(dm.id_musica) > 10;


```
### 10. Encontre o nome de todos os artistas que têm mais de 5 músicas em seu repertório.

```sql
SELECT DISTINCT a.nome
FROM Artista a
JOIN Disco d ON a.id_artista = d.id_artista
JOIN Disco_Musica dm ON d.id_disco = dm.id_disco
JOIN Playlist_Musica pm ON dm.id_musica = pm.id_musica
JOIN Playlist p ON pm.id_playlist = p.id_playlist
WHERE d.data_lancamento < '2010-01-01'
AND p.titulo = 'Top 50';


```
### 11. Encontre o nome de todos os artistas que têm mais de 5 músicas em seu repertório.

```sql
SELECT m.titulo
FROM Musica m
JOIN Artista_Musica am ON m.id_musica = am.id_musica
GROUP BY m.titulo
HAVING COUNT(am.id_artista) > 1;


```
### 12. Encontre o nome de todos os artistas que têm mais de 5 músicas em seu repertório.

```sql
SELECT m.titulo
FROM Musica m
JOIN Playlist_Musica pm ON m.id_musica = pm.id_musica
GROUP BY m.titulo
HAVING COUNT(pm.id_playlist) > 1;


```
### 13. Encontre o nome de todos os artistas que têm mais de 5 músicas em seu repertório.

```sql
SELECT u.nome
FROM Usuario u
JOIN Playlist p ON u.id_usuario = p.id_usuario
JOIN Playlist_Musica pm ON p.id_playlist = pm.id_playlist
JOIN Musica m ON pm.id_musica = m.id_musica
WHERE m.titulo = 'Bohemian Rhapsody';


```
### 14. Encontre o nome de todos os artistas que têm mais de 5 músicas em seu repertório.

```sql
SELECT m.titulo
FROM Musica m
JOIN Disco_Musica dm ON m.id_musica = dm.id_musica
JOIN Disco d ON dm.id_disco = d.id_disco
WHERE d.titulo = 'Dark Side of the Moon'
ORDER BY m.duracao DESC
LIMIT 1;


```
### 15. Encontre o nome de todos os artistas que têm mais de 5 músicas em seu repertório.

```sql
SELECT titulo
FROM Disco
WHERE id_artista = id_artista_especifico
AND EXTRACT(YEAR FROM data_lancamento) = ano_especifico;

```
### 16. Encontre o nome de todos os artistas que têm mais de 5 músicas em seu repertório.

```sql
SELECT DISTINCT a.nome
FROM Artista a
JOIN Artista_Musica am ON a.id_artista = am.id_artista
JOIN Musica m ON am.id_musica = m.id_musica
JOIN Playlist_Musica pm ON m.id_musica = pm.id_musica
JOIN Playlist p ON pm.id_playlist = p.id_playlist
WHERE p.id_usuario = id_usuario_especifico;


```
### 17. Encontre o nome de todos os artistas que têm mais de 5 músicas em seu repertório.

```sql
SELECT m.titulo
FROM Musica m
LEFT JOIN Playlist_Musica pm ON m.id_musica = pm.id_musica
WHERE pm.id_playlist IS NULL;


```
### 18. Encontre o nome de todos os artistas que têm mais de 5 músicas em seu repertório.

```sql
SELECT m.titulo, a.nome
FROM Musica m
JOIN Artista_Musica am ON m.id_musica = am.id_musica
JOIN Artista a ON am.id_artista = a.id_artista
JOIN Playlist_Musica pm ON m.id_musica = pm.id_musica
GROUP BY m.titulo, a.nome, pm.id_playlist
HAVING COUNT(m.id_musica) > 3;


```
### 19. Encontre o nome de todos os artistas que têm mais de 5 músicas em seu repertório.

```sql
SELECT d.titulo
FROM Disco d
JOIN Disco_Musica dm ON d.id_disco = dm.id_disco
JOIN Artista a ON d.id_artista = a.id_artista
WHERE (SELECT COUNT(*) FROM Disco WHERE id_artista = a.id_artista) >= 2;


```
### 20. Encontre o nome de todos os artistas que têm mais de 5 músicas em seu repertório.

```sql
SELECT u.nome AS usuario, p.titulo AS playlist
FROM Usuario u
JOIN Playlist p ON u.id_usuario = p.id_usuario
JOIN Playlist_Musica pm ON p.id_playlist = pm.id_playlist
GROUP BY u.nome, p.titulo
HAVING COUNT(pm.id_musica) >= 5;


```
