# Sistema de Gerenciamento de Biblioteca Universitária

Este projeto é um sistema para gerenciar empréstimos, devoluções e reservas de materiais em uma biblioteca, utilizando Python com SQLAlchemy para a lógica de banco de dados e Streamlit para a interface de usuário.

## Pré-requisitos

Antes de começar, garanta que você tenha os seguintes softwares instalados em sua máquina:

* **Python 3.8 ou superior**: [python.org](https://www.python.org/downloads/)
    * *Importante: Durante a instalação no Windows, marque a caixa "Add Python to PATH".*
* **MySQL Server 8.0 ou superior**: [dev.mysql.com/downloads/mysql/](https://dev.mysql.com/downloads/mysql/)
* **MySQL Workbench** (Opcional, mas recomendado para gerenciar o banco de dados): [dev.mysql.com/downloads/workbench/](https://dev.mysql.com/downloads/workbench/)

## Guia de Instalação e Teste

Siga estes passos para configurar e executar o projeto em seu ambiente local.

### 1. Clonar o Repositório

Primeiro, clone este repositório para a sua máquina local usando o comando:
```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd <NOME_DA_PASTA_DO_REPOSITORIO>
```

### 2. Instalar as Bibliotecas Necessárias

Este projeto utiliza um arquivo `requirements.txt` para gerenciar todas as dependências do Python. Para instalar tudo de uma vez, execute o seguinte comando no seu terminal, dentro da pasta do projeto:

```bash
pip install -r requirements.txt
```
*Se o comando `pip` não for reconhecido, tente usar `python -m pip install -r requirements.txt`.*

### 3. Configurar o Banco de Dados MySQL

A aplicação precisa se conectar a um banco de dados MySQL para funcionar.

**a) Inicie o Servidor MySQL:**
Garanta que o seu serviço do MySQL Server esteja em execução. No Windows, você pode verificar isso em `services.msc` e iniciar o serviço "MySQL80" (ou similar) se ele estiver parado.

**b) Crie o Banco de Dados (Schema):**
Usando o MySQL Workbench ou sua ferramenta de preferência, conecte-se ao seu servidor local e crie um novo banco de dados com o nome exato:
```sql
biblioteca_universitaria_teste
```

**c) Configure a Conexão no Código:**
Abra o arquivo `app.py` em um editor de texto. No início do arquivo, ajuste as credenciais do seu banco de dados, principalmente o usuário (`MYSQL_USER`) e a senha (`MYSQL_PASSWORD`).

```python
# app.py

MYSQL_USER = 'root'
MYSQL_PASSWORD = 'SUA_SENHA_AQUI' # <-- Altere para a senha que você definiu
MYSQL_HOST = 'localhost'
MYSQL_DB = 'biblioteca_universitaria_teste'
```

### 4. Executar a Aplicação

Com tudo configurado, você pode iniciar a interface do sistema.

**a) Inicie o Streamlit:**
No terminal, dentro da pasta do projeto, execute o comando:
```bash
streamlit run app.py
```
*Se o comando `streamlit` não for reconhecido, tente `python -m streamlit run app.py`.*

**b) Crie e Popule as Tabelas (Passo Crucial):**
Ao abrir a aplicação no seu navegador pela primeira vez, o banco de dados ainda estará vazio.
* Na barra lateral esquerda, clique no botão **"Resetar e Popular Banco de Dados"**.
* Isso irá criar todas as tabelas necessárias e inserir os dados de exemplo para que você possa testar o sistema.

Após este passo, a aplicação estará totalmente funcional e pronta para ser usada.
