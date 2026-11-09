# Classe SCManager

Com o _scmanager_ instalado, a importação desta classe é feita com o comando:

```Python
from scmanager import SCManager
```

Sua instanciação pode ser feita de uma forma simples através do comando:

```Python
scm = SCManager()
```

É possível realizar a instanciação de uma forma mais personalizada modificando seus parâmetros opcionais de inicialização:

- _config_file_: `str` - O arquivo de configuração dentro da pasta `scm_config` contendo informações de acesso ao contrato. Seu valor padrão é: `"scm_config.json"`.
- _timeout_: `int` - Duração do timeout em segundos para as transações. Seu valor padrão é: `120`.
- _persist_: `int` - O número de tentativas de refazer a transação em caso de `timeout`. Seu valor padrão é: `0`.
- _show_: `bool` - Se verdadeiro, imprime na tela, após a instanciação, as informações resumidas do contrato. Seu valor padrão é: `False`.

## Métodos de chamada

A seguir a lista de métodos que fazem leitura de dados do contrato.

- _get_account_balance()_ - Retorna o saldo da carteira digital em _Ether_.
- _get_contract_data()_ - Retorna todos os dados do contrato.
- _get_last_updated_timestamp()_ - Retorna a data e hora da última atualização do contrato.
- _get_inactive_ornamental_block_uids_list()_ - Retorna a lista de blocos ornamentais inativos.
- _get_user_uids_list()_ - Retorna a lista de identificadores únicos (_uids_) dos usuários cadastrados.
- _get_ornamental_block_uids_list()_ - Retorna a lista de identificadores únicos (_uids_) dos blocos ornamentais cadastrados.
- _is_user(uid: `ChecksumAddress`)_ - Retorna verdadeiro se o _uid_ informado pertencer a um usuário cadastrado.
- _is_ornamental_block(uid: `ChecksumAddress`)_ - Retorna verdadeiro se o _uid_ informado pertencer a um bloco ornamental cadastrado.
- _get_user_data(user_uid: `ChecksumAddress`)_ - Retorna os dados do usuário com o _uid_ informado.
- _get_ornamental_block_data(ornamental_block_uid: `ChecksumAddress`)_ - Retorna os dados do bloco ornamental com o _uid_ informado.
- _is_ornamental_block_active(ornamental_block_uid: `ChecksumAddress`)_ - Retorna verdadeiro se o bloco ornamental informado através de seu _uid_ estiver ativo.

## Métodos de transação

A seguir a lista de métodos que realizam transação com o contrato inteligente.

- [_add_new_users_](#método-_add_new_users_) - Cadastra um ou mais novos usuários no contrato.
- [_add_new_ornamental_blocks_](#método-_add_new_ornamental_blocks_) - Cadastra um ou mais novos blocos no contrato.
- [_transfer_ornamental_blocks_](#método-_transfer_ornamental_blocks_) - transfere um ou mais blocos ornamentais para novos usuários.
- [_deactivate_ornamental_blocks_](#método-_deactivate_ornamental_blocks_) - Desativa um ou mais blocos ornamentais no contrato.

A seguir, os métodos de transação de forma mais detalhada

### Método _add_new_users_

Adiciona novos usuários ao contrato inteligente.

#### Declaração

Segue a declaração do método _add_new_users_:

```Python
def add_new_users(self, *,
                  user_name_list: list[str],
                  user_cnpj_list: list[str],
                  user_email_address_list: list[str],
                  estimate_cost: bool = False) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]
```    

com a _docstring_:

```Python
"""
Adds new users to the smart contract.

This method adds new users to the smart contract with the provided user data. It supports adding multiple users in a single transaction and can estimate the cost of the transactions if required.

:param user_name_list: A list of company names to be added.
:type user_name_list: list[str]
:param user_cnpj_list: A list of CNPJs (Cadastro Nacional da Pessoa Jurídica).
:type user_cnpj_list: list[str]
:param user_email_address_list: A list of email addresses.
:type user_email_address_list: list[str]
:param estimate_cost: If True, estimates and display the Ether cost for the transactions before executing them.
:type estimate_cost: bool
:return: A tuple containing two lists:
    - new_users_data_list: A list of dictionaries with the data of the newly added users.
    - transactions_list: A list of dictionaries with the details of the transactions performed.
:rtype: tuple[list[dict[str, Any]], list[dict[str, Any]]]
:raises InvalidParameterError: If any of the provided user data lists are invalid.
"""
```

#### Parâmetros

Seus parâmetros são:
- _user_name_list_: `list[str]` - Uma lista de nomes de empresas a serem adicionadas.
- _user_cnpj_list_: `list[str]` - Uma lista de CNPJs (Cadastro Nacional da Pessoa Jurídica).
- _user_email_address_list_: `list[str]` - Uma lista de endereços de _e-mail_.
- _estimate_cost_: `bool` - Se verdadeiro, estima e exibe o custo em _Ether_ das transações antes de executá-las. Seu valor padrão é: `False`.
    
#### Retorno

Retorna uma tupla contendo duas listas:
- _new_users_data_list_: `list` - Uma lista de dicionários com os dados dos novos usuários adicionados.
- _transactions_list_: `list` - Uma lista de dicionários com os detalhes das transações realizadas.

### Método  _add_new_ornamental_blocks_

Adiciona novos blocos ornamentais ao contrato inteligente.

#### Declaração

Segue a declaração do método _add_new_ornamental_blocks_:

```Python
def add_new_ornamental_blocks(self, *,
                              mining_data_list: list[dict[str, str]],
                              code_list: list[str],
                              properties_list: list[dict[str, str]],
                              hash_list: list[str],
                              owners_uid_list: list[ChecksumAddress],
                              estimate_cost: bool = False) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]
```    

com a _docstring_:

```Python
"""
Adds new ornamental blocks to the smart contract.

This method adds new ornamental blocks to the smart contract with the provided block data.
It supports adding multiple blocks in a single transaction and can estimate the cost of the transactions if required.

:param mining_data_list: A list of dictionaries containing the mining data for each block, with the following keys:
    - company (str): The company responsible for the mining.
    - mining_date (str): The date when the mining occurred.
    - mining_site (str): The site where the mining took place.
:type mining_data_list: list[dict[str, str]]
:param code_list: A list of codes associated with the ornamental blocks.
:type code_list: list[str]
:param properties_list: A list of dictionaries containing the properties of each block, with the following keys:
    - dimensions (str): The dimensions of the block.
    - material (str): The material of the block.
    - weight (str): The weight of the block.
:type properties_list: list[dict[str, str]]
:param hash_list: A list of hashes for the ornamental blocks.
:type hash_list: list[str]
:param owners_uid_list: A list of UIDs of the owners of the ornamental blocks.
:type owners_uid_list: list[ChecksumAddress]
:param estimate_cost: If True, estimates and display the Ether cost for the transactions before executing them.
:type estimate_cost: bool
:return: A tuple containing two lists:
    - new_ornamental_blocks_data_list: A list of dictionaries with the data of the newly added ornamental blocks.
    - transactions_list: A list of dictionaries with the details of the transactions performed.
:rtype: tuple[list[dict[str, Any]], list[dict[str, Any]]]
:raises InvalidParameterError: If any of the provided block data lists are invalid.
    """
```    

#### Parâmetros

Seus parâmetros são:
- _mining_data_list_: `list[dict[str, str]]` - Uma lista de dicionários contendo os dados de mineração de cada bloco, com as seguintes chaves:
    - _company_: `str` - A empresa responsável pela mineração.
    - _mining_date_: `str` - A data em que a mineração ocorreu.
    - _mining_site_: `str`: O local onde a mineração ocorreu.
- _code_list_: `list[str]` - Uma lista de códigos associados aos blocos ornamentais.
- _properties_list_: `list[dict[str, str]]` - Uma lista de dicionários contendo as propriedades de cada bloco, com as seguintes chaves:
    - _dimensions_: `str` - As dimensões do bloco.
    - _material_: `str` - O material do bloco.
    - _weight_: `str` -  O peso do bloco.        
- _hash_list_: `list[str]` - Uma lista de hashes para os blocos ornamentais.
- _owners_uid_list_: `list[ChecksumAddress]` - Uma lista de UIDs dos proprietários dos blocos ornamentais.
- _estimate_cost_: `bool` - Se verdadeiro, estima e exibe o custo em Ether das transações antes de executá-las. Seu valor padrão é: `False`.    

#### Retorno

Retorna uma tupla contendo duas listas:

- _new_ornamental_blocks_data_list_: `list` - Uma lista de dicionários com os dados dos novos blocos ornamentais adicionados.
- _transactions_list_: `list` - Uma lista de dicionários com os detalhes das transações realizadas.
    
Se ocorrer um erro de parâmetro inválido, lança uma exceção `InvalidParameterError`.

### Método _transfer_ornamental_blocks_

Transfere a propriedade de blocos ornamentais no contrato inteligente.

#### Declaração

Segue a declaração do método _transfer_ornamental_blocks_:

```Python
def transfer_ornamental_blocks(self, *,
                               ornamental_block_uid_list: list[ChecksumAddress],
                               new_owner_uid_list: list[ChecksumAddress],
                               invoice_number_list: list[str],
                               estimate_cost: bool = False) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]
```

com a _docstring_:

```Python
"""
Transfers ownership of ornamental blocks in the smart contract.

This method transfers the ownership of ornamental blocks to new owners with the provided data.
It supports transferring multiple blocks in a single transaction and can estimate the cost of the transactions if required.

:param ornamental_block_uid_list: A list of UIDs of the ornamental blocks to be transferred.
:type ornamental_block_uid_list: list[ChecksumAddress]
:param new_owner_uid_list: A list of UIDs of the new owners.
:type new_owner_uid_list: list[ChecksumAddress]
:param invoice_number_list: A list of invoice numbers associated with the transfers.
:type invoice_number_list: list[str]
:param estimate_cost: If True, estimates and display the Ether cost for the transactions before executing them.
:type estimate_cost: bool
:return: A tuple containing two lists:
    - transfered_ornamental_blocks_data_list: A list of dictionaries with the data of the transferred ornamental blocks.
    - transactions_list: A list of dictionaries with the details of the transactions performed.
:rtype: tuple[list[dict[str, Any]], list[dict[str, Any]]]
:raises InvalidParameterError: If any of the provided transfer data lists are invalid.
"""
```
    
#### Parâmetros

Seus parâmetros são:
- _ornamental_block_uid_list_: `list[ChecksumAddress]` - Uma lista de UIDs dos blocos ornamentais a serem transferidos.
- _new_owner_uid_list_: `list[ChecksumAddress]` - Uma lista de UIDs dos novos proprietários.
- _invoice_number_list_: `list[str]` - Uma lista de números de fatura associados às transferências.
- _estimate_cost_: `bool` - Se verdadeiro, estima e exibe o custo em Ether das transações antes de executá-las. Seu valor padrão é: `False`.
    
#### Retorno

Retorna uma tupla contendo duas listas:
- _transfered_ornamental_blocks_data_list_: `list` - Uma lista de dicionários com os dados dos blocos ornamentais transferidos.
- _transactions_list_: `list` - Uma lista de dicionários com os detalhes das transações realizadas.
    
Se ocorrer um erro de parâmetro inválido, lança uma exceção `InvalidParameterError`.

### Método _deactivate_ornamental_blocks_

Desativa blocos ornamentais no contrato inteligente.

#### Declaração

Segue a declaração do método _deactivate_ornamental_blocks_:

```Python
def deactivate_ornamental_blocks(self,
                                 ornamental_block_uid_list: list[ChecksumAddress], *,
                                 estimate_cost: bool = False) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]
```

com a _docstring_:

```Python
"""
Deactivates ornamental blocks in the smart contract.

This method deactivates the specified ornamental blocks in the smart contract.
It supports deactivating multiple blocks in a single transaction and can estimate the cost of the transactions if required.

:param ornamental_block_uid_list: A list of UIDs of the ornamental blocks to be deactivated.
:type ornamental_block_uid_list: list[ChecksumAddress]
:param estimate_cost: If True, estimates the cost of the transactions without executing them.
:type estimate_cost: bool
:return: A tuple containing two lists:
    - deactivated_ornamental_blocks_data_list: A list of dictionaries with the data of the deactivated ornamental blocks.
    - transactions_list: A list of dictionaries with the details of the transactions performed.
:rtype: tuple[list[dict[str, Any]], list[dict[str, Any]]]
:raises InvalidParameterError: If any of the provided block UIDs are invalid.
"""
```
    
#### Parâmetros

Seus parâmetros são:
- _ornamental_block_uid_list_: `list[ChecksumAddress]` - Uma lista de UIDs dos blocos ornamentais a serem desativados.
- _estimate_cost_: `bool` - Se verdadeiro, estima o custo das transações sem executá-las. Seu valor padrão é: `False`.

#### Retorno

Retorna uma tupla contendo duas listas:
- _deactivated_ornamental_blocks_data_list_: `list` - Uma lista de dicionários com os dados dos blocos ornamentais desativados.
- _transactions_list_: `list` - Uma lista de dicionários com os detalhes das transações realizadas.
    
Se ocorrer um erro de parâmetro inválido, lança uma exceção `InvalidParameterError`.