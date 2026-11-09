# Módulo admin_tools

O módulo _admin_tools_ possui dois métodos:

- [_create_config_file_](#método-_create_config_file_) - Cria um arquivo de configuração na pasta `scm_config` contendo informações de acesso à rede _blockchain_ e ao contrato inteligente.
- [_deploy_smart_contract_](#método-_deploy_smart_contract_) - Realiza o _deploy_ (implantação) do contrato na rede.

Com o scmanager instalado, a importação deste módulo é feita com o comando:

```Python
from scmanager import admin_tools
```

## Método _create_config_file_

Cria um arquivo de configuração na pasta `scm_config` contendo informações de acesso à rede _blockchain_ e ao contrato inteligente.

### Declaração

Segue a declaração do método _create_config_file_:

```Python
def create_config_file(endpoint_environment_key: str = 'ETHEREUM_ENDPOINT',  
                       private_environment_key: str = 'ETHEREUM_PRIVATE_KEY',  
                       file_name: str = 'scm_config.json',  
                       deploy: bool = True) -> None
```

com a _docstring_:

```Python  
"""  
Creates a configuration file for the smart contract deployment environment.  
  
This method generates a JSON configuration file with the provided endpoint link and private environment key.  
  
:param endpoint_environment_key: The environment key for the endpoint link of the blockchain network.
:type endpoint_environment_key: str
:param private_environment_key: The key for the environment variable containing the account private key.
:type private_environment_key: str:param file_name: The name of the configuration file to be created.
:type file_name: str:param deploy: If True, calls the deploy_smart_contract() method with it's default values.
:type deploy: bool
:return: If deploy is True, returns dictionary containing the updated configuration data, including the contract's 
deployment information, else returns None  
:rtype: dict[str, Any] | None
"""
```

### Parâmetros

Seus parâmetros são:

- _endpoint_environment_key_: `str` - A chave da variável de ambiente que contém o endereço do [endpoint](docs/aquisicao_endpoint.md#aquisição-do-endereço-do-endpoint) para a rede _blockchain_. Seu valor padrão é: `"ETHEREUM_ENDPOINT"`.
- _private_environment_key_: `str` - A chave da variável de ambiente que contém a [chave privada](carteira_digital.md#recuperação-da-chave-privada) da conta na carteira digital. Seu valor padrão é: `"ETHEREUM_PRIVATE_KEY"`.
- _file_name_: `str` - O nome do arquivo de configuração a ser criado (na pasta scm_config). Seu valor padrão é: `"scm_config.json"`.
- _deploy_: `bool` - Se verdadeiro, após a criação do arquivo de configuração, o método `deploy_smart_contract()` é chamado com seus parâmetros padrão. Seu valor padrão é: `True`.

### Retorno

Caso o parâmetro `deploy` for verdadeiro, retorna um dicionário contendo os dados de configuração atualizados com as informações de _deploy_ do contrato, caso negativo, não retorna nada.

## Método _deploy_smart_contract_

Faz o _deploy_ de um contrato inteligente na rede _blockchain_.

### Declaração

Segue a declaração do método _deploy_smart_contract_:

```Python
def deploy_smart_contract(contract_address_to_recover: str = '0x' + '0' * 40,
                          config_file: str = 'scm_config.json',
                          timeout: int = 120,
                          persist: int = 0) -> dict[str, Any] | None
```    

com a _docstring_:

```Python
"""
Deploys a smart contract to the blockchain.
    
This method reads the configuration file, extracts and compiles the smart contract code, and deploys the contract to the blockchain. 
It also updates the configuration file with the contract's deployment information.
   
:param contract_address_to_recover: The recovery address for the old smart contract.
:type contract_address_to_recover: str
:param config_file: The path to the configuration file to read and update.
:type config_file: str
:param timeout: The timeout duration for the transaction in seconds.
:type timeout: int
:param persist: The persistence flag for the transaction.
:type persist: int
:return: A dictionary containing the updated configuration data, including the contract's deployment information.
:rtype: dict[str, Any] | None
"""
```

### Parâmetros

Seus parâmetros são:
- _contract_address_to_recover_: `str` - O endereço de recuperação do contrato inteligente antigo, se houver. Seu valor padrão é: `'0x' + '0' * 40`.
- _config_file_: `str` - O caminho para o [arquivo de configuração](#método-_create_config_file_) a ser lido e atualizado. Seu valor padrão é: `"scm_config.json"`.
- _timeout_: `int` - A duração do tempo limite para a transação em segundos. Seu valor padrão é: `120`.
- _persist_: `int` - A flag de persistência para a transação. Seu valor padrão é: `0`.
    

### Retorno

Retorna um dicionário contendo os dados de configuração atualizados com as informações de _deploy_ do contrato. Caso contrário, retorna `None`.