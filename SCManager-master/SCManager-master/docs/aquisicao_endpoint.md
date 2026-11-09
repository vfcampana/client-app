# Aquisição de um endpoint da Infura

Para se conectar à *blockchain*, é preciso utilizar um nó, ou endpoint, que serve como uma porta para a rede. Neste tópico será detalhado como acessar um endpoint da _Infura_.

1. Neste projeto é utilizado o endpoint da _Infura_, assim, acesse o site https://www.infura.io/;
2. Será preciso agora se cadastrar no site, desta forma, clique em _Sign In_, no canto superior direito da tela;
3. Na próxima tela, clique em _Sign up today_, no canto inferior direito;
4. Preencha os campos com os seus dados, marque a caixa de consentimento e depois clique em _CREATE A FREE ACCOUNT_;
5. Após isso, _verifique o e-mail_ cadastrado no passo anterior para validar o cadastro no site;
6. Após a verificação, entre novamente no site da Infura e repita o passo 2 deste tutorial;
7. Agora, entre com o e-mail e senha cadastrados e clique em _LOGIN_.

## Aquisição do endereço do endpoint
Uma vez na tela de usuário, o objetivo é obter o endereço do endpoint para a rede _Ethereum_. Para isso, é preciso criar uma _api key_ que faça essa comunicação. Assim:

1. Na tela inicial do usuário, clique no ícone no canto superior direito da tela escrito _CREATE NEW API KEY_;
2. Selecione a opção _Web3 API_ em *NETWORK* e depois escolha um nome para a aplicação na caixa de diálogo *NAME*. Após isso, clique em _CREATE_.

A tela que abre na sequência é a tela da API criada.

3. No canto superior direito, clique em _Endpoints_.

Na aba _Endpoints_ é possível gerar um endpoint para diversas redes existentes. Como neste projeto será utilizada a rede de testes da Ethereum, faça:

4. Procure a linha correspondente à rede *Ethereum*, e clique na seta do menu suspenso escrito *MAINNET* para abrir as opções;
5. Das redes que aparecem, escolha a opção _Sepolia_.

Uma vez selecionada a rede Sepolia, o _endereço de acesso ao Endpoint_ irá aparecer ao lado.

6. Copie esse endereço clicando no botão de cópia ao lado.

O endereço de acesso ao endpoint é necessário para acessar a rede _Ethereum_. Por questões de praticidade no código, esse endereço também deverá ser armazenado no sistema como uma variável de ambiente sob o nome _ETHEREUM_ENDPOINT_. Para isto, basta realizar os mesmos passos vistos no tópico [Armazenamento da chave privada no sistema](carteira_digital.md#armazenamento-da-chave-privada-no-sistema) porém modificando o nome da chave.