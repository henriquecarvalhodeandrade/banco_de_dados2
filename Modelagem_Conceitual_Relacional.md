### A) Diagrama Entidade Relacionamento e B) Diagrama Modelo Relacional
Disponível na pasta "img"

### C) Justificativa das Escolhas de Cardinalidade e Integridade

As escolhas de cardinalidade nos relacionamentos e as restrições de integridade nas tabelas garantem a consistência e a correta aplicação das regras de negócio do sistema de biblioteca.

#### 1. Escolhas de Cardinalidade (Relacionamentos)

As cardinalidades foram definidas com base na lógica do mundo real e no design orientado a objetos das classes:

* **1:N (Um para Muitos):**
    * **Material (1) -> Exemplar (N):** Um material abstrato (um título único, como "Python para Iniciantes") pode ter muitas cópias físicas (`Exemplar`). É uma relação de "um para muitas" cópias.
    * **Usuario (1) -> Emprestimo/Reserva (N):** Um utilizador pode realizar vários registos de empréstimos e várias reservas ao longo do tempo.
    * **Exemplar (1) -> Emprestimo/Reserva (N):** Um exemplar específico (cópia física) pode estar associado a muitos registos de empréstimo (historicamente) e a várias reservas.

* **N:M (Muitos para Muitos):**
    * **Material (N) <-> Autor (M):** Um material pode ter múltiplos autores, e um autor pode ter escrito múltiplos materiais. Este relacionamento é resolvido pela tabela associativa **`material_autor`**.

* **1:1 (Herança - *Joined Table Inheritance*):**
    * **Usuario (1) <-> Subtipos (Aluno, Professor, Funcionario) (1):** O modelo usa herança (tabelas unidas), onde cada subtipo tem uma relação **1:1** com a superclasse. O `id` do subtipo é, simultaneamente, Chave Primária (PK) e Chave Estrangeira (FK) para a tabela da superclasse, garantindo a especialização dos atributos. O mesmo princípio aplica-se à hierarquia de **Material**.

#### 2. Escolhas de Integridade (Restrições de Colunas)

As restrições de integridade são cruciais para a validade dos dados:

* **Integridade de Entidade (Chave Primária - PK):**
    * Todas as tabelas possuem uma coluna `id` definida como `primary_key=True`, garantindo que cada registo seja único e não nulo.

* **Integridade Referencial (Chave Estrangeira - FK):**
    * As Chaves Estrangeiras (FKs), como `emprestimos.usuario_id`, garantem que os registos nos relacionamentos apenas apontem para entidades que realmente existem nas tabelas referenciadas (`usuarios.id`), mantendo a consistência dos dados.

* **Integridade de Domínio (Restrições Lógicas):**
    * **`matricula` Única:** A coluna `matricula` em `usuarios` é definida como `unique=True` para garantir que a identificação dos utilizadores seja exclusiva.
    * **`data_devolucao` Anulável (Nullable):** Permite que um registo de empréstimo exista na base de dados (`emprestimos`) enquanto o material está "em andamento" (não devolvido). A data é preenchida apenas no momento da devolução.
    * **`multa` Padrão (Default):** O atributo `multa` em `emprestimos` possui um valor `default=0`, garantindo que um novo empréstimo comece sem penalidades.