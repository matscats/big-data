CREATE TABLE music (
  id SERIAL PRIMARY KEY,
  usuario VARCHAR(255),
  nome VARCHAR(255),
  artista VARCHAR(255),
  duracao INT,
  genero VARCHAR(255)
);