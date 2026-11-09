# Configuração de uma Carteira Digital da Metamask
Para configurar uma carteira digital da _Metamask_, é preciso seguir os passos:

1. Acessar o site da Metamask em: https://metamask.io/;
2. Instalar a extensão da Metamask em seu navegador ao clicar em _download_.

Uma vez adicionada a extensão, uma página irá se abrir para concordar com os termos de uso. Após isso:

3. Clique em _Criar uma nova carteira_;
4. Leia e concorde com as instruções de segurança;
5. Na próxima tela, crie uma nova senha para manipulação da carteira;
6. Na tela seguinte, clique em _Proteger minha carteira_ para gerar uma frase de recuperação secreta.

Essa frase é de uso privado, então é extremamente importante anotá-la em um local seguro e não revelá-la à ninguém.

7. Na tela seguinte, clique em _Revelar frase de recuperação secreta_ para visualizar e anotar sua senha em um local seguro;
8. Na próxima tela, será solicitado que complete as palavras que estão faltando para verificar se está tudo correto;
9. Pronto, carteira criada com sucesso. Clique em _Got it!_ -> _seguinte_ -> _concluído_ para acessar sua conta.

Na tela do usuário, é possível ver informações como:

- Endereço da conta -> Uma string hexadecimal de 40 caracteres;
- Saldo da conta -> O saldo da conta na rede **Ethereum** em _ethers;
- A rede ativa na carteira -> Inicialmente, está ativa a rede _Ethereum Mainnet_ onde se pode realizar transações utilizando valores monetários reais.

Uma dica para facilitar o acesso à carteira digital é _fixar a extensão como um atalho_ na barra de extensões do navegador.
## Mudança de rede para a rede de testes Sepolia
Como inicialmente é importante a realização de testes, é preciso alterar a rede ativa para uma rede de testes. Para isso é preciso seguir os passos:

1. Clicar em _Ethereum Mainnet_ e habilitar _Mostrar redes de teste_ para visualizar as redes de teste;
2. Neste projeto é utilizada a rede _Sepolia_, então selecione-a.

Agora, na tela do usuário, o saldo é mostrado em _SepoliaETH_ ou "ethers sepolia", que não possuem real valor monetário.
## Recuperação da chave privada
Para a manipulação de contratos inteligentes, será necessário que o usuário tenha em mãos a _chave privada_ da conta a ser utilizada. Para visualizar a chave privada da conta é preciso seguir os passos:

1. Na tela inicial da conta do usuário, _clique nos três pontos_ no canto superior direito e depois em _Detalhes da conta_;
2. No menu popup que se abriu é possível visualizar o endereço da conta e um botão para visualizar a chave privada. Clique em _Show private key_;
3. Na tela seguinte, digite a senha da conta e clique em _confirmar_;
4. Na próxima tela, é preciso manter pressionado por alguns segundos o botão _Hold to reveal Private Key_ para poder visualizar a chave privada;
5. Após isso, será revelada a chave privada, uma string em hexadecimal de 64 caracteres. **Copie** a chave e clique em _Concluído_.

## Armazenamento da chave privada no sistema
Uma vez recuperada a chave privada, é preciso armazená-la em um local seguro. Uma forma de fazer isso é salvá-la como uma variável ambiente do sistema. Para isto, segue-se os passos:

6. Aperte a tecla _Windows_, pesquise por _variáveis de ambiente_ e aperte _enter_;
7. Na janela que se abriu, clique em _Novo..._ para configurar uma nova variável de ambiente;
8. No campo _Nome da variável_ é preciso digitar o nome a qual será referenciada a chave. Neste projeto, utiliza-se o nome: _ETHEREUM_PRIVATE_KEY_;
9. No campo _Valor da variável_ é preciso primeiro escrever os caracteres _"0x"_ (zero x) e em seguida colar a _chave privada_ de 64 caracteres recuperada na conta;
10. Clique em _Ok_ e feche a janela.

Pronto, sua chave privada está armazenada de forma segura.

## Aquisição de Sepolia Ethers (faucets)

Na rede _Ethereum_, todas as transações, sejam de inserção de contratos inteligentes, sejam de chamadas de funções de transação, requerem um valor em ethers. Quanto maior e mais complexo é o contrato ou maior o custo de processamento da função a ser chamada, maior é a quantidade gasta em ether. Como o protótipo é realizado em uma rede de testes, a Sepolia, então o que se gasta é o Sepolia ether, que não tem valor monetário, mas é preciso solicitá-los de alguma forma.

Uma forma de se conseguir esses Sepolia ethers é através de _faucets_, que são sites em que é preciso se cadastrar e, diariamente, são liberados uma quantidade fixa de Sepolia ethers para a conta solicitada. O faucet que tem sido utilizado neste projeto é o https://sepoliafaucet.com/. A seguir será mostrado o procedimento para se conseguir Sepolia ethers:

1. Entre no site https://sepoliafaucet.com/ e verifique na barra superior se a rede selecionada é a _Ethereum Sepolia_;
2. Clique em _Alchemy Login_, no canto superior direito;
3. Caso não tenha uma conta na Alchemy, crie uma clicando em _Signup_ ou em _Sign in with Google_;
4. Após criada uma nova conta e realizado o login, volte a tela inicial do faucet;
5. No campo _Enter your wallet address_, cole o **Endereço da sua conta**;
6. Marque a caixa do verificador _Não sou um robô_ e, em seguida clique em _Send me ETH_.

Após isso, basta entrar na sua carteira digital e verificar se foi creditado uma quantia de Sepolia Ethers na sua conta.

Importante lembrar que esse procedimento só pode ser realizado novamente após 24h.