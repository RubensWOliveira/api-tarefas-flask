# Flask Task Manager API

![Python](https://img.shields.io/badge/python-3.11-blue)
![Flask](https://img.shields.io/badge/flask-backend-green)
![JWT](https://img.shields.io/badge/authentication-JWT-orange)
![Swagger](https://img.shields.io/badge/docs-swagger-lightblue)

API RESTful desenvolvida com Flask para gerenciamento de tarefas com autenticação JWT, controle multiusuário e documentação Swagger.

---

## Tecnologias utilizadas

* Python
* Flask
* Flask SQLAlchemy
* Flask JWT Extended
* Flask Bcrypt
* SQLite
* Swagger (Flasgger)
* Postman (testes de API)

---

## Funcionalidades

### Autenticação

* Cadastro de usuário
* Login com geração de token JWT
* Senhas criptografadas com bcrypt

### Tarefas

* Criar tarefa
* Listar tarefas do usuário logado
* Buscar tarefa por ID
* Marcar tarefa como concluída
* Atualizar tarefa
* Deletar tarefa

### Segurança

* Autenticação via JWT
* Proteção de rotas privadas
* Cada usuário acessa apenas suas próprias tarefas

---

## Estrutura do projeto

```
api-tarefas-flask/
│
├── app.py
├── database.py
├── requirements.txt
│
├── models/
│   ├── user.py
│   └── task.py
│
├── routes/
│   ├── auth_routes.py
│   └── task_routes.py
│
└── README.md
```

---

## Instalação

Clone o repositório:

```
git clone https://github.com/seu-usuario/api-tarefas-flask.git
```

Entre na pasta:

```
cd api-tarefas-flask
```

Crie ambiente virtual:

```
python -m venv venv
```

Ative o ambiente virtual:

Windows:

```
venv\Scripts\activate
```

Instale dependências:

```
pip install -r requirements.txt
```

Execute o projeto:

```
python app.py
```

Servidor iniciará em:

```
http://localhost:5000
```

---

## Documentação Swagger

Acesse:

```
http://localhost:5000/apidocs
```

Permite testar endpoints diretamente pelo navegador.

---

## Endpoints principais

### Autenticação

POST /register

```
{
  "username": "usuario",
  "password": "123456"
}
```

POST /login

```
{
  "username": "usuario",
  "password": "123456"
}
```

Retorna:

```
access_token
```

---

### Tarefas (requer token JWT)

Criar tarefa

POST /tasks

```
{
  "title": "Nova tarefa",
  "description": "Descrição da tarefa"
}
```

Listar tarefas

GET /tasks

Buscar tarefa por ID

GET /tasks/{id}

Marcar como concluída

PATCH /tasks/{id}/complete

Atualizar tarefa

PUT /tasks/{id}

Deletar tarefa

DELETE /tasks/{id}

---

## Exemplo de uso com Postman

1. Registrar usuário
2. Fazer login
3. Copiar access_token
4. Usar Bearer Token nas rotas protegidas

---

## Autor

Rubens Oliveira

Projeto desenvolvido como parte da transição de carreira para desenvolvimento backend com Python.
