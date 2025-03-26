
# Título do Projeto

Este projeto visa permitir a rastreabilidade de um bloco de rocha ornamental, desde o momento de sua lavra
até seu processamento e comercialização. Com esse objetivo, visa-se a construção de um sistema (no formato de aplicação web).

O sistema conta com 2 "agentes", clientes - nossos usuários, que são empresas no ramo de blocos ornamentais, e a administração - Mogai, que controla os aspectos do usuário (se está inativo, cria as contas, entre outros).

As principais funções do sistema são: permitir que um usuário autenticar-se no sistema, manipular seus blocos 
(adicionar, inativar, editar), ver blocos anunciados e negociar com os anunciantes.

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
