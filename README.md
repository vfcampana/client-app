
# 🏗️ BlockAPI - Sistema de Gestão de Blocos de Pedra

Sistema completo para gestão de blocos de pedra com backend Flask, frontend React e integração com Supabase para armazenamento de imagens.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Tecnologias](#tecnologias)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Execução](#execução)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [API Endpoints](#api-endpoints)
- [Funcionalidades](#funcionalidades)
- [Troubleshooting](#troubleshooting)

## 🎯 Visão Geral

O BlockAPI é uma plataforma para gestão de blocos de pedra que permite:
- ✅ Cadastro e gestão de blocos com múltiplas imagens
- ✅ Sistema de autenticação e autorização
- ✅ Upload de imagens via galeria ou câmera
- ✅ Criação e gestão de lotes
- ✅ Sistema de favoritos
- ✅ Chat entre usuários
- ✅ Interface responsiva (mobile/desktop)

## 🛠️ Tecnologias

### Backend
- **Flask** - Framework web Python
- **PostgreSQL** - Banco de dados principal
- **Supabase** - Storage para imagens
- **JWT** - Autenticação
- **Flask-CORS** - Controle de acesso

### Frontend
- **React + TypeScript** - Interface do usuário
- **Material-UI** - Componentes visuais
- **React Query** - Gerenciamento de estado
- **Axios** - Cliente HTTP

## 📋 Pré-requisitos

- **Python 3.8+**
- **Node.js 16+** e **npm**
- **PostgreSQL** (ou acesso ao banco remoto)
- **Git**

## 🚀 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/vfcampana/client-app.git
cd client-app
```

### 2. Configuração do Backend

#### Criar ambiente virtual Python
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### Instalar dependências Python
```bash
pip install -r requirements.txt
```

### 3. Configuração do Frontend
Tem que instalar o NODE pelo google

```bash
cd front-app
npm install
```

## ⚙️ Configuração

### 1. Variáveis de Ambiente

Crie ou configure o arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=postgresql://usuario:senha@host:porta/database?sslmode=require

SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua_chave_publica_supabase

Pedir chaves de conexão para Enzo Hubner. É possivel que no momento em que voce rodar o projeto os banco de dados estejam desligados, então peça que seja conferido!
```

### 2. Configuração do Frontend

Crie o arquivo `front-app/.env`:

```env
REACT_APP_BACKEND_URL=http://localhost:5000
```

## 🏃‍♂️ Execução

### 1. Iniciar Backend

```bash
# Na raiz do projeto, com ambiente virtual ativado
cd blockapi
python app.py
```

O backend estará disponível em: `http://localhost:5000`

### 2. Iniciar Frontend

```bash
# Em outro terminal
cd front-app
npm start
```

O frontend estará disponível em: `http://localhost:3000`

## 📁 Estrutura do Projeto

```
client-app/
├── blockapi/                 # Backend Flask
│   ├── api/                  # Endpoints da API
│   │   ├── resources/        # Recursos REST
│   │   └── views.py          # Views principais
│   ├── models/               # Modelos do banco
│   ├── scripts/              # Scripts utilitários
│   ├── sql/                  # Scripts SQL
│   └── app.py               # Aplicação principal
│
├── front-app/               # Frontend React
│   ├── src/
│   │   ├── components/      # Componentes reutilizáveis
│   │   ├── pages/          # Páginas da aplicação
│   │   ├── services/       # Serviços de API
│   │   ├── types/          # Tipos TypeScript
│   │   └── styles/         # Estilos e temas
│   └── public/             # Arquivos públicos
│
├── tests/                  # Testes
├── requirements.txt        # Dependências Python
├── .env                    # Variáveis de ambiente
└── README.md              # Este arquivo
```

## ✨ Funcionalidades

### 📷 Upload de Imagens
- **Galeria**: Seleção múltipla de imagens
- **Câmera**: Captura direta (mobile/desktop)
- **Preview**: Carrossel de visualização
- **Storage**: Armazenamento no Supabase

### 🗂️ Gestão de Blocos
- Cadastro completo com informações técnicas
- Sistema de status (privado/anunciado)
- Múltiplas imagens por bloco
- Filtros e busca

### 📦 Sistema de Lotes
- Agrupamento de blocos
- Gestão centralizada
- Preços por lote

### 🔐 Autenticação
- JWT tokens
- Controle de acesso
- Sessões persistentes

## 🐛 Troubleshooting

### Backend não inicia
```bash
# Verificar se o ambiente virtual está ativo
which python  # deve apontar para venv

# Reinstalar dependências
pip install -r requirements.txt

# Verificar variáveis de ambiente
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('DATABASE_URL'))"
```

### Frontend não carrega
```bash
# Limpar cache e reinstalar
rm -rf node_modules package-lock.json
npm install

# Verificar porta
lsof -i :3000  # verificar se porta está ocupada
```

### Erro de CORS
Verifique se o `flask-cors` está instalado e configurado no `app.py`:
```python
from flask_cors import CORS
CORS(app)
```

### Imagens não aparecem
1. Verificar configuração do Supabase
2. Verificar políticas de acesso no Supabase
3. Verificar console do navegador para erros

### Erro de autenticação
```bash
# Verificar JWT_SECRET_KEY no .env
# Limpar localStorage do navegador
localStorage.clear()
```

## 📝 Notas de Desenvolvimento

- O projeto usa PostgreSQL como banco principal
- Imagens são armazenadas no Supabase Storage
- Frontend e backend rodam em portas separadas
- CORS está habilitado para desenvolvimento
- JWT tokens têm expiração configurável

---

🚀 **Projeto desenvolvido com Flask + React + TypeScript + Supabase**

As tecnologias escolhidas para o sistema foram: React.js (front), Flask (back), PostgreSQL (banco de dados). 
Estão sujeitas a alterações conforme necessidade do projeto. 

## Documentação da API

#### Cadastra Usuário   

```http
  POST /cadastro
```

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `email` | `string` | **Obrigatório**. |
| `senha` | `string` | **Obrigatório**. |


#### Faz Login

```http
  POST /login
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `email`      | `string` | **Obrigatório**.|
| `senha`      | `string` | **Obrigatório**.|

#### Atualiza Usuário

```http
  PUT /usuario
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `nome`      | `string` | **Opcional**.|
| `telefone`      | `string` | **Opcional**.|
| `CEP`      | `string` | **Opcional**.|

#### Busca Usuário

```http
  GET /usuario/<int:id>
```

#### Apaga Conta

```http
  DELETE /usuario
```
Obs: Apaga a conta do usuário ao enviar com o Bearer Token

#### Cadastra Bloco

```http
  POST /bloco
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `título`      | `string` | **Obrigatório**.|
| `classificação`      | `string` | **Obrigatório**.|
| `coloração`      | `string` | **Obrigatório**.|
| `material`      | `string` | **Obrigatório**.|
| `medida_bruta`      | `string` | **Obrigatório**.|
| `volume_bruto`      | `string` | **Obrigatório**.|
| `pedreira`      | `string` | **Obrigatório**.|
| `observacoes`      | `string` | **Obrigatório**.|
| `cep`      | `string` | **Obrigatório**.|
| `valor`      | `float` | **Obrigatório**.|
| `status`      | `int` | **Obrigatório**.|


#### Busca Bloco

```http
  GET /bloco/<int:id>
```

#### Lista Bloco(do Usuario)

```http
  GET /bloco
```
Obs: Aqui são puxados os blocos do usuário a partir do ID dele que veio do token JWT

#### Apaga Bloco

```http
  DELETE /bloco/<int:id>
```

#### Cadastra Lote

```http
  POST /lote
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `nome`      | `string` | **Obrigatório**.|
| `preco`      | `float` | **Obrigatório**.|
| `observacoes`      | `string` | **Obrigatório**.|
| `status`      | `int` | **Obrigatório**.|
| `blocos`      | `<list:int>` | **Obrigatório**.|

#### Atualiza Lote

```http
  PUT /lote/<int:id>
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `nome`      | `string` | **Opcional**.|
| `preco`      | `float` | **Opcional**.|
| `observacoes`      | `string` | **Opcional**.|
| `status`      | `int` | **Opcional**.|
| `blocos`      | `<list:int>` | **Opcional**.|

#### Busca Lote

```http
  GET /lote/<int:id>
```
#### Lista Lote

```http
  GET /lote
```
Obs: Aqui são puxados os lotes do usuário a partir do ID dele que veio do token JWT

#### Apaga Lote

```http
  DELETE /lote/<int:id>
```

#### Cadastro Anuncio

```http
  POST /anuncio
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `id_lote`      | `int` | **Opcional**.|
| `id_bloco`      | `int` | **Opcional**.|

#### Atualizar Anuncio

```http
  PUT /anuncio/<int:id>
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `id_lote`      | `int` | **Opcional**.|
| `id_bloco`      | `int` | **Opcional**.|

#### Busca Anuncio

```http
  GET /anuncio/<int:id>
```
#### Lista Anuncios

```http
  GET /anuncio
```

#### Apaga Anuncio

```http
  DELETE /anuncio/<int:id>
```

#### Lista Anuncios do Usuário

```http
  GET /meusAnuncios
```
Obs: Aqui são puxados os anuncios do usuário a partir do ID dele que veio do token JWT

# Colaboradores

Agradecemos às seguintes pessoas que contribuíram para este projeto:

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/enzohubner" title="" style="text-decoration: none; color: #FFFFFF;">
        <img src="https://avatars.githubusercontent.com/u/94123023?s=400&u=823c0ea99dbd99d62ea0d6e0fe768a8e6af35ed0&v=4" width="100px;" alt="Foto do Enzo Hubner no GitHub"/><br>
        <sub>
          <b>Enzo Hubner</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/viniciusxv27" title="" style="text-decoration: none; color: #FFFFFF;">
        <img src="https://avatars.githubusercontent.com/u/83793571?v=4" width="100px;" alt="Foto do Vinicius no GitHub"/><br>
        <sub>
          <b>Vinícius Costa</b>
        </sub>
      </a>
    </td>
  </tr>
</table>
