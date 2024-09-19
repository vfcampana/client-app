# Introduction 

Este projeto visa permitir a rastreabilidade de um bloco de rocha ornamental, desde o momento de sua lavra
até seu processamento e comercialização. Com esse objetivo, visa-se a construção de um sistema 
(no formato de aplicação web) que permita os clientes tirarem fotos de seus blocos e, através da visão computacional, 
identificá-los e guardar as informações relevantes no blockchain, garantindo permanência e transparência.

O sistema conta com 2 "agentes", clientes - nossos usuários, que são empresas no ramo de blocos ornamentais, 
e a administração - Mogai, que controla os aspectos do usuário (se está inativo, cria as contas, entre outros).

As principais funções do sistema são: permitir que um usuário autenticar-se no sistema, manipular seus blocos 
(adicionar, inativar, editar), ver blocos anunciados e negociar com os anunciantes.

As tecnologias escolhidas para o sistema foram: React.js (front), Flask (back), PostgreSQL (banco de dados). 
Estão sujeitas a alterações conforme necessidade do projeto. 

# Getting Started
1. Para continuar o desenvolvimento do sistema, instale Python em sua máquina (ou ambiente de sua preferência).
2. Com o Python devidamente instalado e configurado, abra o local do projeto (na IDE ou outro programa de sua preferência).
3. Crie um ambiente virtual para desenvolvimento. Use o seguinte comando no terminal dentro da pasta do projeto: ``py -m venv nome_da_pasta_venv``
4. Após a criação do ambiente virtual, ative-o utilizando o script apropriado para seu terminal. E.g: no powershell escreva: ``./nome_da_pasta_venv/Scripts/Activate.ps1``
5. Com o ambiente ativado, execute o seguinte comando para instalar as dependências do projeto: ``pip install -r ./requirements.txt``
6. O projeto está pronto para ser rodado :)

# Contribute
O código atual contempla apenas as operações CRUD do usuário e suas rotas. Os modelos para as classes identificadas
em uma análise anterior também estão implementadas, porém não são utilizadas ainda. Nenhuma tela foi desenvolvida ainda.
Os próximos passos são criar a interação de usuário e bloco, comunicar com o módulo de visão computacional e módulo
de blockchain.

Caso algo no repositório não esteja seguindo as boas práticas (clean code), reporte para podermos melhorar.