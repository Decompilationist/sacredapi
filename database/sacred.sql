-- Criação da tabela de livros
CREATE TABLE livros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    testamento ENUM('Velho', 'Novo') NOT NULL
);

ALTER TABLE livros ADD UNIQUE INDEX idx_nome (nome);


-- Criação da tabela de capítulos
CREATE TABLE capitulos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    livro_id INT NOT NULL,
    numero INT NOT NULL,
    FOREIGN KEY (livro_id) REFERENCES livros(id)
);

-- Criação da tabela de versículos
CREATE TABLE versiculos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    livro_id INT NOT NULL,
    capitulo_id INT NOT NULL,
    numero INT NOT NULL,
    texto TEXT NOT NULL,
    FOREIGN KEY (livro_id) REFERENCES livros(id),
    FOREIGN KEY (capitulo_id) REFERENCES capitulos(id)
);

-- Criação da tabela de posts
CREATE TABLE posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    livro_id INT NOT NULL,
    capitulo_id INT NOT NULL,
    versiculo_id INT NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    conteudo TEXT NOT NULL,
    UNIQUE INDEX idx_titulo (titulo), -- Restrição de índice único no título
    FOREIGN KEY (livro_id) REFERENCES livros(id),
    FOREIGN KEY (capitulo_id) REFERENCES capitulos(id),
    FOREIGN KEY (versiculo_id) REFERENCES versiculos(id)
);
