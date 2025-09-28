-- 1. Pesquisa por filtros múltiplos (título e ano)
-- Encontra um livro com título e ano de publicação específicos.
SELECT T1.*, T2.*
FROM materiais AS T1
JOIN livros AS T2 ON T1.id = T2.id
WHERE T1.titulo = 'Machine Learning com Python' AND T1.ano_publicacao = 2023
LIMIT 1;

-- 2. Pesquisa de materiais por autor
-- Usa JOINs para encontrar todos os materiais associados a um autor específico.
SELECT materiais.*
FROM materiais
JOIN material_autor ON materiais.id = material_autor.material_id
JOIN autores ON autores.id = material_autor.autor_id
WHERE autores.nome = 'Autor A';

-- 3. Relatório agregado (contagem total)
-- Conta o número total de empréstimos na tabela.
SELECT COUNT(id)
FROM emprestimos;

-- 4. Queries com LIKE
-- Encontra todos os materiais cujo título contém a palavra 'Dados'.
SELECT *
FROM materiais
WHERE titulo LIKE '%Dados%';