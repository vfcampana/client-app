# Pacote SCManager

Este pacote em python fornece a classe _scmanager_, que é usada para interagir com um contrato inteligente na rede _blockchain Ethereum_.
Essa classe contém métodos para adicionar informações de novos usuários e blocos ornamentais, recuperar informações gerais, transferir blocos entre usuários e desativar blocos.

## Pré-requisitos

Para a utilização da _scmanager_, alguns pré-requisitos são necessários de se executar. São eles:

1. [Configuração de uma _Carteira Digital_](#configuração-de-uma-carteira-digital);
2. [Conexão com um nó da Blockchain](#conexão-com-um-nó-da-_blockchain_);
3. [Instalação do pacote _scmanager_](#instalação-do-pacote-_scmanager_).

Os procedimentos para esses pré-requisitos serão detalhados a seguir.

### Configuração de uma Carteira Digital

Neste projeto, será utilizada uma carteira digital da _Metamask_. Para configurar uma, é preciso seguir os passos do tutorial disponível nesse link:
[Configuração de uma Carteira Digital da Metamask](docs/carteira_digital.md)

### Conexão com um nó da _blockchain_

Para se conectar à *blockchain*, é preciso utilizar um nó, ou endpoint, que serve como uma porta para a rede. Para adquirir esse endpoint, siga os passos descritos no seguinte tutorial:
[Aquisição de um endpoint da Infura](docs/aquisicao_endpoint.md)

### Instalação do pacote _scmanager_

Para a instalação do pacote _scmanager_, é preciso ter acesso ao repositório no **Azure DevOps** ou ao repositório no **GitHub**. Para adquirir o acesso, solicite ao responsável técnico do projeto.
Abra um novo projeto com ambiente virtual ativado. No terminal, navegue até a pasta do projeto e insira a seguinte linha de comando:

- Com acesso ao repositório no **Azure DevOps**:

```Cmd
pip install git+https://dev.azure.com/Mogai/CNPQ_Blockchain/_git/blockchain_module
```

- Com acesso ao repositório no **GitHub**:

```Cmd
pip install git+https://github.com/Blockchain-Tests/SCManager.git
```

### Organização das variáveis de ambiente

Como mencionado anteriormente sobre [armazenamento da chave privada no sistema](docs/carteira_digital.md#armazenamento-da-chave-privada-no-sistema), tanto a chave privada da carteira digital quanto o [endpoint](docs/aquisicao_endpoint.md#aquisição-do-endereço-do-endpoint) devem estar acessíveis pelo pacote _scmanager_. Para isso, é necessário de duas uma:

- ou que as chaves _ETHEREUM_PRIVATE_KEY_ e _ETHEREUM_ENDPOINT_ estejam registradas nas variáveis de ambiente;
- ou que um arquivo `.env` contendo essas chaves esteja no diretório raiz do projeto. Neste caso:
	- crie um arquivo de texto e o renomeie como `.env`;
	- dentro do arquivo insira o texto abaixo (substituindo os escritos entre <>), salve e feche o arquivo.

```
ETHEREUM_PRIVATE_KEY='0x<sua_chave_privada>'
ETHEREUM_ENDPOINT='<seu_endpoint>'
``` 

## Conhecendo o pacote _scmanager_

O primeiro passo na utilização do _scmanager_ é a realização do _deploy_ de um contrato inteligente na rede Ethereum. Para isso, é preciso criar um arquivo de configuração contendo os parâmetros necessários para o acesso à rede.

### _Deploy_ do contrato inteligente na rede Ethereum

Importação do módulo admin_tools e execução do método `create_config_file()`:

```Python
from scmanager import admin_tools as adm
adm.create_config_file()
```

Este comando irá criar um arquivo de configuração padrão `scm_config.json` na pasta `scm_config` e realizar o _deploy_ do contrato inteligente na rede. 
Para mais informações sobre o módulo `admin_tools`, [clique aqui](docs/modulo_admin_tools.md).
Durante sua execução, a seguinte mensagem aparecerá no console:

```Cmd
Config file successfully created at: scm_config/scm_config.json
Building transaction contract_deploy...
    Estimated transaction cost: X Eth.
	Press ENTER to send the transaction: 
```

Como toda transação realizada na _blockchain_ possui um custo em _Ether_, essa mensagem solicita a aprovação da transação baseada na estimativa de custo do _deploy_.
Tecle `ENTER` para continuar com a transação ou qualquer tecla e `ENTER` para cancelar.

> Nota: O cancelamento de uma transação gerará o erro `KeyboardInterrupt: Transaction interrupted by user`.

Aprovando o custo da transação, esta será realizada e as configurações do contrato serão gravadas no arquivo de configuração (neste caso, localizado em `scm_config/scm_config.json`) e retornadas no console. 

### Instanciação do objeto _scm_ da classe _SCManager_

A classe _SCManager_ é a interface com a rede _blockchain_, representando o contrato inteligente.
Sua importação e instanciação é feita através do comando:

```Python
from scmanager import SCManager
scm = SCManager()
```

Essa forma de instanciar, utilizando o padrão dos parâmetros, a classe busca o contrato gravado no arquivo de configuração localizado em `scm_config/scm_config.json`.  
  
Mais informações sobre a classe _SCManager_ podem ser encontradas [aqui](docs/classe_SCManager).  
  
## Testes  
  
Para testes da classe _SCManager_, foi desenvolvido [módulo example](docs/modulo_example) com métodos de geração de parâmetros aleatórios para as funções de transação existentes.  
  
Um exemplo de utilização pode ser executado através do método _run_ do módulo _example_ como mostrado [neste link](docs/modulo_example#exemplo)
