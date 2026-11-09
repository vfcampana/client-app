# Módulo example

O módulo _example_ possui quatro métodos:

- [_generate_dummy_users_](https://dev.azure.com/Mogai/CNPQ_Blockchain/_wiki/wikis/CNPQ_Blockchain.wiki?wikiVersion=GBwikiMaster&_a=edit&pagePath=/Blockchain/Pacote%20scmanager/M%C3%B3dulo%20_example_&pageId=187&anchor=m%C3%A9todo-generate_dummy_users) - Gera usuários falsos com dados aleatórios para testes.
- [_generate_dummy_blocks_](https://dev.azure.com/Mogai/CNPQ_Blockchain/_wiki/wikis/CNPQ_Blockchain.wiki?wikiVersion=GBwikiMaster&_a=edit&pagePath=/Blockchain/Pacote%20scmanager/M%C3%B3dulo%20_example_&pageId=187&anchor=m%C3%A9todo-generate_dummy_blocks) - Gera blocos ornamentais falsos com características aleatórias associadas à uma lista de usuários.
- [_generate_dummy_transfers_](https://dev.azure.com/Mogai/CNPQ_Blockchain/_wiki/wikis/CNPQ_Blockchain.wiki/187/M%C3%B3dulo-_example_?_a=edit&anchor=m%C3%A9todo-generate_dummy_transfers) - Gera informações falsas de transferências com notas aleatórias.
- [_run_](https://dev.azure.com/Mogai/CNPQ_Blockchain/_wiki/wikis/CNPQ_Blockchain.wiki/187/M%C3%B3dulo-_example_?_a=edit&anchor=m%C3%A9todo-run) - Executa uma série de operações demonstrando a uso da classe _SCManager_.

Com o _scmanager_ instalado, a importação deste módulo é feita com o comando:

```Python
from scmanager.examples import example
```

## Método _generate_dummy_users_

Gera usuários falsos com nomes, CNPJs e endereços de _e-mail_ aleatórios em um dicionário no formato necessário para utilizar o método `add_new_users` da classe _SCManager_.

### Declaração

Segue a declaração do método _generate_dummy_users_:

```Python
def generate_dummy_users(number_of_users: int = 1) -> dict[str, list]
```

com a _docstring_:

```Python  
"""  
Generates dummy users with random names, CNPJs, and email addresses.  
  
This function generates a specified number of dummy users, each with a random name, CNPJ, and email address. The user data is returned in a dictionary format.  
  
:param number_of_users: The number of dummy users to generate. Defaults to 1.
:type number_of_users: int:
return: A dictionary containing three lists:  
    - user_name_list: A list of generated user names.
    - user_cnpj_list: A list of generated CNPJs.
    - user_email_address_list: A list of generated email addresses.
:rtype: dict[str, list]
"""
```

### Parâmetros

Seu parâmetro é:

- _number_of_users_: `int` - O número de usuários a serem gerados. Seu valor padrão é: `1`.

### Retorno

Um dicionário contendo as seguintes chaves:
- _user_name_list_: `list[str]` - Lista de nomes aleatórios de usuários.
- _user_cnpj_list_: `list[str]` - Lista de CNPJs aleatórios de usuários.
- _user_email_address_list_: `list[str]` - Lista de endereços de _e-mail_ aleatórios de usuários.

## Método _generate_dummy_blocks_

Gera blocos ornamentais falsos com características aleatórias associadas à uma lista de usuários em um dicionário no formato necessário para utilizar o método `add_new_ornamental_blocks` da classe _SCManager_.

### Declaração

Segue a declaração do método _generate_dummy_blocks_:

```Python
def generate_dummy_blocks(owner_uids_list: list[str]) -> dict[str, list]
```

com a _docstring_:

```Python  
"""
Generates dummy blocks with random mining data, properties, and unique identifiers.  
  
This function generates a block of data for each owner UID provided in the list. Each block contains  
random mining data, properties, a code, and a hash. The data is returned in a dictionary format.  
  
:param owner_uids_list: A list of owner UIDs for which the blocks will be generated.
:type owner_uids_list: list
:return: A dictionary containing five lists:  
    - mining_data_list: A list of dictionaries with random mining data.
    - code_list: A list of generated codes.
    - properties_list: A list of dictionaries with random properties.
    - hash_list: A list of generated hashes.
    - owners_uid_list: The list of provided owner UIDs.
:rtype: dict[str, list]
"""
```

### Parâmetros

Seu parâmetro é:

- _owner_uids_list_: `list[str]` - A lista de identificadores únicos dos usuários que serão os proprietários dos blocos.

### Retorno

Um dicionário contendo as seguintes chaves:
- _mining_data_list_: `list[str]` - Lista de dicionários com dados aleatórios sobre a mineração dos blocos ornamentais.
- _code_list_: `list[str]` - Lista de códigos aleatórios para os blocos ornamentais.
- _properties_list_: `list[str]` - Lista de dicionários com dados aleatórios sobre as propriedades dos blocos ornamentais.
- _hash_list_: `list[str]` - Lista de _hashs_ aleatórios para os blocos ornamentais.
- _owners_uid_list_: `list[str]` - Lista de identificadores únicos dos usuários proprietários dos blocos fornecida.

## Método _generate_dummy_transfers_

Gera informações falsas de transferências com notas aleatórias em um dicionário no formato necessário para utilizar o método `transfer_ornamental_blocks` da classe _SCManager_.

### Declaração

Segue a declaração do método _generate_dummy_transfers_:

```Python
def generate_dummy_transfers(block_uids_list: list[str], new_owner_uids_list: list[str])
```

com a _docstring_:

```Python  
"""  
Generates dummy transfer data with random invoice numbers for ornamental blocks.  
  
This function generates transfer data for each block UID provided in the list. Each transfer includes the block UID,  
the new owner UID, and a randomly generated invoice number. The data is returned in a dictionary format.  
  
:param block_uids_list: A list of ornamental block UIDs for which the transfers will be generated.
:type block_uids_list: list[str]
:param new_owner_uids_list: A list of new owner UIDs for the corresponding blocks.
:type new_owner_uids_list: list[str]
:return: A dictionary containing three lists:  
    - ornamental_block_uid_list: The list of provided block UIDs.
    - new_owner_uid_list: The list of provided new owner UIDs.
    - invoice_number_list: A list of randomly generated invoice numbers.
:rtype: dict[str, list]
"""
```

### Parâmetros

Seus parâmetros são:

- _block_uids_list_: `list[str]` - A lista de identificadores únicos dos blocos ornamentais que serão transferidos para novos proprietários.
- _new_owner_uids_list_: `list[str]` - A lista de identificadores únicos dos respectivos novos usuários proprietários desses blocos ornamentais.

### Retorno

Um dicionário contendo as seguintes chaves:
- _ornamental_block_uid_list_: `list[str]` - Lista fornecida de identificadores únicos dos blocos ornamentais a serem transferidos.
- _new_owner_uid_list_: `list[str]` - Lista fornecida de identificadores únicos dos novos usuários proprietários dos blocos ornamentais.
- _invoice_number_list_: `list[str]` - Lista de notas aleatórias para a transferência.

## Método run

Executa uma série de operações demonstrando a uso da classe _SCManager_.

### Declaração

Segue a declaração do método _run_:

```Python
def run(step_by_step: bool = True) -> None
```

com a _docstring_:

```Python  
"""  
Executes a series of operations to demonstrate the usage of the SCManager.  
  
This function performs the following operations:  
1. Creates a config file.  
2. Deploys a smart contract.  
3. Instantiates an SCManager object.  
4. Extracts all data from the smart contract.  
5. Registers three users with random data.  
6. Retrieves the list of user UIDs.  
7. Adds four ornamental blocks to the first user.  
8. Retrieves the list of ornamental block UIDs.  
9. Extracts data from the first user.  
10. Transfers two ornamental blocks to the second and third users.  
11. Extracts data from the second and third users.  
12. Deactivates one ornamental block from the first user.  
13. Extracts data from the deactivated ornamental block.  
14. Retrieves the list of inactive ornamental block UIDs.  
15. Extracts all data from the smart contract.  
  
The detailed description of each operation is printed to the console.  
  
:param step_by_step: Set to True to run the example step by step.
:type step_by_step: bool
:return: None
"""
```

### Parâmetros

Seu parâmetro é:

- _step_by_step_: `bool` - Se verdadeiro, a demonstração exige que o usuário pressione a tecla `ENTER` no intervalod e cada operação. Seu valor padrão é: True.

### Retorno

Não há retorno. Apenas uma sequência de impressões no console demonstrando um exemplo da execução das seguintes operações:

1. Criação de um arquivo de configuração;
2. Implantação do contrato inteligente na rede;
3. Instanciação de um objeto da classe _SCManager_;
4. Extração dos dados do contrato;
5. Cadastro de três usuários aleatórios;
6. Leitura da lista de identificadores únicos dos usuários cadastrados;
7. Adição de quatro blocos ornamentais para o primeiro usuário cadastrado;
8. Leitura da lista de identificadores únicos dos blocos ornamentais registrados;
9. Extração dos dados do primeiro usuário cadastrado;
10. Transferência de propriedade de dois blocos ornamentais do primeiro usuário cadastrado para o segundo e terceiro usuários;
11. Extração dos dados do segundo e terceiro usuários cadastrados;
12. Desativação de um bloco ornamental do primeiro usuário cadastrado;
13. Extração dos dados do bloco ornamental desativado;
14. Leitura da lista de identificadores únicos dos blocos ornamentais desativados;
15. Extração de todos os dados do contrato inteligente.

### Exemplo

Um exemplo de execução do método _run_ pode ser visto a seguir:

```Cmd
************************* Importing scmanager package **************************

>>> from scmanager.admin_tools import create_config_file
    from scmanager import SCManager

************ Creating a config file and deploying a smart contract *************

>>> create_config_file(file_name='examples/cfg_example_937.json')

Config file successfully created at: scm_config/examples/cfg_example_937.json
Building transaction contract_deploy...
	Estimated transaction cost: 0.104103 Eth.
		Press ENTER to send the transaction:
>? 
	Sending transaction nº 3851...
	Transaction contract_deploy sent successfully in 6.512 s! Cost: 0.103261 Eth.

Press ENTER to continue...

********************** Instantiating an SCManager object ***********************

>>> scm = SCManager(config_file='examples/cfg_example_937.json', persist=1, show=True)

Contract 0xb8996fC314bf3A7D89E3220ecc435E56549154Ca connected:
	0 user(s) and 0 active ornamental block(s) found:
	Dump list (0 inactive block(s)):

Press ENTER to continue...

***************** Extracting all data from the smart contract ******************

>>> scm.get_contract_data()

{'ornamental_block_uids_list': [],
 'ornamental_blocks_list': [],
 'recovered_contracts_address_list': ['0xb8996fC314bf3A7D89E3220ecc435E56549154Ca'],
 'user_uids_list': [],
 'users_list': []}

Press ENTER to continue...

***************************** Registering 3 users ******************************

>>> scm.add_new_users(user_name_list=['qlqvxnnsxm', 'xopnzcpkseo', 'gfvqcoldbsw'],
  		      user_cnpj_list=['31.345.604/0001-01', '79.105.754/0001-66', '99.142.754/0001-43'],
		      user_email_address_list=['contato@qlqvx.com', 'contato@xopnz.com', 'contato@gfvqc.com'])

The operation will be executed in 1 transaction:
Building transaction add_up_to_5_new_users...
	Sending transaction nº 3852...
	Transaction add_up_to_5_new_users sent successfully in 26.634 s! Cost: 0.010875 Eth.

([{'cnpj': '31.345.604/0001-01',
   'company_name': 'qlqvxnnsxm',
   'email_address': 'contato@qlqvx.com',
   'last_update_timestamp': '2025/03/13, 15:01:30.579235',
   'list_index': 1,
   'ornamental_blocks_list': [],
   'registration_timestamp': '2025/03/13, 15:01:30.579235',
   'uid': '0xaAF4b51A022adDE0dEb86CC7980Bc9859917e4A9'},
  {'cnpj': '79.105.754/0001-66',
   'company_name': 'xopnzcpkseo',
   'email_address': 'contato@xopnz.com',
   'last_update_timestamp': '2025/03/13, 15:01:30.579235',
   'list_index': 2,
   'ornamental_blocks_list': [],
   'registration_timestamp': '2025/03/13, 15:01:30.579235',
   'uid': '0x0d69aD522fc08D650D0FF6172fC9EEcc0EBC30CD'},
  {'cnpj': '99.142.754/0001-43',
   'company_name': 'gfvqcoldbsw',
   'email_address': 'contato@gfvqc.com',
   'last_update_timestamp': '2025/03/13, 15:01:30.579235',
   'list_index': 3,
   'ornamental_blocks_list': [],
   'registration_timestamp': '2025/03/13, 15:01:30.579235',
   'uid': '0xcC3f20EaDA81AFdfA4D77d44d171306820DceF00'}],
 [{'block_hash': '0x58fd0c3e2a62446709d01aba031e5fd89fdfdb1b3f65f2a74c95379da20d55fc',
   'block_number': 7895317,
   'contract_address': '0xb8996fC314bf3A7D89E3220ecc435E56549154Ca',
   'cost_eth': 0.010874979068864692,
   'cost_gwei': 10874979.06886469,
   'duration': 26.634,
   'effective_gas_price': 17963147098,
   'from': '0xcEB8dDd79E5C794c4CA8058B0f7fF8876533F168',
   'function': 'add_up_to_5_new_users',
   'gas_used': 605405,
   'hash': '0x94c8c262d538412d94dca97449d6bf31777d1325e53afed03481b920cdaeead7',
   'index': 51,
   'link': 'https://sepolia.etherscan.io/tx/0x94c8c262d538412d94dca97449d6bf31777d1325e53afed03481b920cdaeead7'}])

Press ENTER to continue...

************************** Getting the users uid list **************************

>>> scm.get_user_uids_list()

['0xaAF4b51A022adDE0dEb86CC7980Bc9859917e4A9',
 '0x0d69aD522fc08D650D0FF6172fC9EEcc0EBC30CD',
 '0xcC3f20EaDA81AFdfA4D77d44d171306820DceF00']

Press ENTER to continue...

***************** Adding 4 ornamental blocks to the first user *****************

>>> scm.add_new_ornamental_blocks(mining_data_list=[{"company": "sfvalcpwhfed", "mining_site": "wlgigydmggda", "mining_date": "myjmrimklz"},
						    {"company": "rhjvyqmpjpr", "mining_site": "opijeqvzcms", "mining_date": "famnzvgdqr"},
						    {"company": "wwpcjwuhvubzsb", "mining_site": "uokzwawajbljyg", "mining_date": "sapdaoiivz"},
						    {"company": "rmqczeqyupmlv", "mining_site": "idqbfseefvyhn", "mining_date": "eqykioyfew"}],
				  code_list=["lplwakoptm", "fglrefxeii", "nsviqliaue", "tkmadvrhga"],
				  properties_list=[{"material": "cshfpdhruwqq", "dimensions": "2.75, 1.47, 2.64", "weight": "3326"},
						   {"material": "ymxhmkfroej", "dimensions": "2.31, 1.2, 2.06", "weight": "6155"},
						   {"material": "msgblhyrpynfts", "dimensions": "1.04, 1.92, 1.36", "weight": "4360"},
						   {"material": "bcbhpwfjrgipi", "dimensions": "2.94, 2.07, 2.26", "weight": "2952"}],
				  hash_list=["Yrh64Wyg5rtbXFYxsZHXclOAG006CfL4VJIQ5NCH42", "APGoKcGpxpz4YiuQmokab2Ts25tNyuBrZwOFH2MxMQ", "uLyJ2UTJpci18V1XiL8SIpbStn1EHWjwmRkc7XemEz", "pH6O6Qm2xcEqEINNF6m1GU512CT5EduGl9TWrHUp2B"],
				  owners_uid_list=["0xaAF4b51A022adDE0dEb86CC7980Bc9859917e4A9", "0xaAF4b51A022adDE0dEb86CC7980Bc9859917e4A9", "0xaAF4b51A022adDE0dEb86CC7980Bc9859917e4A9", "0xaAF4b51A022adDE0dEb86CC7980Bc9859917e4A9"])

The operation will be executed in 1 transaction:
Building transaction add_up_to_5_new_ornamental_blocks...
	Sending transaction nº 3853...
	Transaction add_up_to_5_new_ornamental_blocks sent successfully in 24.612 s! Cost: 0.035033 Eth.

([{'code': 'lplwakoptm',
   'hash': 'Yrh64Wyg5rtbXFYxsZHXclOAG006CfL4VJIQ5NCH42',
   'invoice_numbers': [],
   'is_active': True,
   'last_owners': ['0xaAF4b51A022adDE0dEb86CC7980Bc9859917e4A9'],
   'last_update_timestamp': '2025/03/13, 15:02:08.126275',
   'list_index': 0,
   'mining_data': {'company': 'sfvalcpwhfed',
                   'mining_date': 'myjmrimklz',
                   'mining_site': 'wlgigydmggda'},
   'properties': {'dimensions': '2.75, 1.47, 2.64',
                  'material': 'cshfpdhruwqq',
                  'weight': '3326'},
   'registration_timestamp': '2025/03/13, 15:02:08.126275',
   'uid': '0x4b23d3e9f26576d6431027225Ad8711942067F83'},
  {'code': 'fglrefxeii',
   'hash': 'APGoKcGpxpz4YiuQmokab2Ts25tNyuBrZwOFH2MxMQ',
   'invoice_numbers': [],
   'is_active': True,
   'last_owners': ['0xaAF4b51A022adDE0dEb86CC7980Bc9859917e4A9'],
   'last_update_timestamp': '2025/03/13, 15:02:08.126275',
   'list_index': 1,
   'mining_data': {'company': 'rhjvyqmpjpr',
                   'mining_date': 'famnzvgdqr',
                   'mining_site': 'opijeqvzcms'},
   'properties': {'dimensions': '2.31, 1.2, 2.06',
                  'material': 'ymxhmkfroej',
                  'weight': '6155'},
   'registration_timestamp': '2025/03/13, 15:02:08.126275',
   'uid': '0xf998cc90532015Ec2Ce47718547782587380e6E8'},
  {'code': 'nsviqliaue',
   'hash': 'uLyJ2UTJpci18V1XiL8SIpbStn1EHWjwmRkc7XemEz',
   'invoice_numbers': [],
   'is_active': True,
   'last_owners': ['0xaAF4b51A022adDE0dEb86CC7980Bc9859917e4A9'],
   'last_update_timestamp': '2025/03/13, 15:02:08.126275',
   'list_index': 2,
   'mining_data': {'company': 'wwpcjwuhvubzsb',
                   'mining_date': 'sapdaoiivz',
                   'mining_site': 'uokzwawajbljyg'},
   'properties': {'dimensions': '1.04, 1.92, 1.36',
                  'material': 'msgblhyrpynfts',
                  'weight': '4360'},
   'registration_timestamp': '2025/03/13, 15:02:08.126275',
   'uid': '0xc3D95B9f3fC2cAee393Dde48a759D021C87F3B67'},
  {'code': 'tkmadvrhga',
   'hash': 'pH6O6Qm2xcEqEINNF6m1GU512CT5EduGl9TWrHUp2B',
   'invoice_numbers': [],
   'is_active': True,
   'last_owners': ['0xaAF4b51A022adDE0dEb86CC7980Bc9859917e4A9'],
   'last_update_timestamp': '2025/03/13, 15:02:08.126275',
   'list_index': 3,
   'mining_data': {'company': 'rmqczeqyupmlv',
                   'mining_date': 'eqykioyfew',
                   'mining_site': 'idqbfseefvyhn'},
   'properties': {'dimensions': '2.94, 2.07, 2.26',
                  'material': 'bcbhpwfjrgipi',
                  'weight': '2952'},
   'registration_timestamp': '2025/03/13, 15:02:08.126275',
   'uid': '0xf295b3b4B947221a17A49541178192908dd30932'}],
 [{'block_hash': '0x8d31b301efe07ee1c16f0ebea125bbd3ab0cbb158eb3e4fd9f88b569bcf28807',
   'block_number': 7895320,
   'contract_address': '0xb8996fC314bf3A7D89E3220ecc435E56549154Ca',
   'cost_eth': 0.0350327739332017,
   'cost_gwei': 35032773.9332017,
   'duration': 24.612,
   'effective_gas_price': 17541383438,
   'from': '0xcEB8dDd79E5C794c4CA8058B0f7fF8876533F168',
   'function': 'add_up_to_5_new_ornamental_blocks',
   'gas_used': 1997150,
   'hash': '0x929febc9f498bce95b7c70747679f9db3a4b2b3c1ebb7541a06fffea719c39e8',
   'index': 116,
   'link': 'https://sepolia.etherscan.io/tx/0x929febc9f498bce95b7c70747679f9db3a4b2b3c1ebb7541a06fffea719c39e8'}])

Press ENTER to continue...

******************** Getting the ornamental blocks uid list ********************

>>> scm.get_ornamental_block_uids_list()

['0x4b23d3e9f26576d6431027225Ad8711942067F83',
 '0xf998cc90532015Ec2Ce47718547782587380e6E8',
 '0xc3D95B9f3fC2cAee393Dde48a759D021C87F3B67',
 '0xf295b3b4B947221a17A49541178192908dd30932']

Press ENTER to continue...

********************* Extracting data from the first user **********************

>>> scm.get_user_data('0xaAF4b51A022adDE0dEb86CC7980Bc9859917e4A9')

{'cnpj': '31.345.604/0001-01',
 'company_name': 'qlqvxnnsxm',
 'email_address': 'contato@qlqvx.com',
 'last_update_timestamp': '2025/03/13, 15:02:08.126275',
 'list_index': 1,
 'ornamental_blocks_list': ['0x4b23d3e9f26576d6431027225Ad8711942067F83',
                            '0xf998cc90532015Ec2Ce47718547782587380e6E8',
                            '0xc3D95B9f3fC2cAee393Dde48a759D021C87F3B67',
                            '0xf295b3b4B947221a17A49541178192908dd30932'],
 'registration_timestamp': '2025/03/13, 15:01:30.579235',
 'uid': '0xaAF4b51A022adDE0dEb86CC7980Bc9859917e4A9'}

Press ENTER to continue...

********* Transfering 1 ornamental block to the second and third users *********

>>> scm.transfer_ornamental_blocks(ornamental_block_uid_list=["0xf998cc90532015Ec2Ce47718547782587380e6E8", "0xc3D95B9f3fC2cAee393Dde48a759D021C87F3B67"], 
				   new_owner_uid_list=["0x0d69aD522fc08D650D0FF6172fC9EEcc0EBC30CD", "0xcC3f20EaDA81AFdfA4D77d44d171306820DceF00"], 
				   invoice_number_list=["5463674580", "3627222684"])

The operation will be executed in 1 transaction:
Building transaction transfer_up_to_5_ornamental_blocks...
	Sending transaction nº 3854...
	Transaction transfer_up_to_5_ornamental_blocks sent successfully in 10.665 s! Cost: 0.006116 Eth.

([{'code': 'fglrefxeii',
   'hash': 'APGoKcGpxpz4YiuQmokab2Ts25tNyuBrZwOFH2MxMQ',
   'invoice_numbers': ['5463674580'],
   'is_active': True,
   'last_owners': ['0xaAF4b51A022adDE0dEb86CC7980Bc9859917e4A9',
                   '0x0d69aD522fc08D650D0FF6172fC9EEcc0EBC30CD'],
   'last_update_timestamp': '2025/03/13, 15:02:47.204032',
   'list_index': 1,
   'mining_data': {'company': 'rhjvyqmpjpr',
                   'mining_date': 'famnzvgdqr',
                   'mining_site': 'opijeqvzcms'},
   'properties': {'dimensions': '2.31, 1.2, 2.06',
                  'material': 'ymxhmkfroej',
                  'weight': '6155'},
   'registration_timestamp': '2025/03/13, 15:02:08.126275',
   'uid': '0xf998cc90532015Ec2Ce47718547782587380e6E8'},
  {'code': 'nsviqliaue',
   'hash': 'uLyJ2UTJpci18V1XiL8SIpbStn1EHWjwmRkc7XemEz',
   'invoice_numbers': ['3627222684'],
   'is_active': True,
   'last_owners': ['0xaAF4b51A022adDE0dEb86CC7980Bc9859917e4A9',
                   '0xcC3f20EaDA81AFdfA4D77d44d171306820DceF00'],
   'last_update_timestamp': '2025/03/13, 15:02:47.204032',
   'list_index': 2,
   'mining_data': {'company': 'wwpcjwuhvubzsb',
                   'mining_date': 'sapdaoiivz',
                   'mining_site': 'uokzwawajbljyg'},
   'properties': {'dimensions': '1.04, 1.92, 1.36',
                  'material': 'msgblhyrpynfts',
                  'weight': '4360'},
   'registration_timestamp': '2025/03/13, 15:02:08.126275',
   'uid': '0xc3D95B9f3fC2cAee393Dde48a759D021C87F3B67'}],
 [{'block_hash': '0x65a05e0774d3c768ca0381762a95d9bcbb25c676e0c59a7ce6f3649f4091acec',
   'block_number': 7895321,
   'contract_address': '0xb8996fC314bf3A7D89E3220ecc435E56549154Ca',
   'cost_eth': 0.006116126182204425,
   'cost_gwei': 6116126.182204424,
   'duration': 10.665,
   'effective_gas_price': 17520499886,
   'from': '0xcEB8dDd79E5C794c4CA8058B0f7fF8876533F168',
   'function': 'transfer_up_to_5_ornamental_blocks',
   'gas_used': 349084,
   'hash': '0x00672f924cbb94bd9393c56de1aa6f856aba06983e181ffa5a5b4fc9adaae643',
   'index': 212,
   'link': 'https://sepolia.etherscan.io/tx/0x00672f924cbb94bd9393c56de1aa6f856aba06983e181ffa5a5b4fc9adaae643'}])

Press ENTER to continue...

********************* Extracting data from the second user *********************

>>> scm.get_user_data('0x0d69aD522fc08D650D0FF6172fC9EEcc0EBC30CD')

{'cnpj': '79.105.754/0001-66',
 'company_name': 'xopnzcpkseo',
 'email_address': 'contato@xopnz.com',
 'last_update_timestamp': '2025/03/13, 15:02:47.204032',
 'list_index': 2,
 'ornamental_blocks_list': ['0xf998cc90532015Ec2Ce47718547782587380e6E8'],
 'registration_timestamp': '2025/03/13, 15:01:30.579235',
 'uid': '0x0d69aD522fc08D650D0FF6172fC9EEcc0EBC30CD'}

Press ENTER to continue...

********************* Extracting data from the third user **********************

>>> scm.get_user_data('0xcC3f20EaDA81AFdfA4D77d44d171306820DceF00')

{'cnpj': '99.142.754/0001-43',
 'company_name': 'gfvqcoldbsw',
 'email_address': 'contato@gfvqc.com',
 'last_update_timestamp': '2025/03/13, 15:02:47.204032',
 'list_index': 3,
 'ornamental_blocks_list': ['0xc3D95B9f3fC2cAee393Dde48a759D021C87F3B67'],
 'registration_timestamp': '2025/03/13, 15:01:30.579235',
 'uid': '0xcC3f20EaDA81AFdfA4D77d44d171306820DceF00'}

Press ENTER to continue...

************* Deactivating 1 ornamental block from the first user **************

>>> scm.deactivate_ornamental_blocks(['0xf295b3b4B947221a17A49541178192908dd30932'])

The operation will be executed in 1 transaction:
Building transaction deactivate_ornamental_block...
	Sending transaction nº 3855...
	Transaction deactivate_ornamental_block sent successfully in 156.447 s! Cost: 0.002988 Eth.

([{'code': 'tkmadvrhga',
   'hash': 'pH6O6Qm2xcEqEINNF6m1GU512CT5EduGl9TWrHUp2B',
   'invoice_numbers': [''],
   'is_active': False,
   'last_owners': ['0xaAF4b51A022adDE0dEb86CC7980Bc9859917e4A9',
                   '0x0000000000000000000000000000000000000000'],
   'last_update_timestamp': '2025/03/13, 15:03:44.124185',
   'list_index': 3,
   'mining_data': {'company': 'rmqczeqyupmlv',
                   'mining_date': 'eqykioyfew',
                   'mining_site': 'idqbfseefvyhn'},
   'properties': {'dimensions': '2.94, 2.07, 2.26',
                  'material': 'bcbhpwfjrgipi',
                  'weight': '2952'},
   'registration_timestamp': '2025/03/13, 15:02:08.126275',
   'uid': '0xf295b3b4B947221a17A49541178192908dd30932'}],
 [{'block_hash': '0x77e23dca9400ded15fb544140bb85d3c07f80b8a5eb51cbca07c3ac7939b3a27',
   'block_number': 7895336,
   'contract_address': '0xb8996fC314bf3A7D89E3220ecc435E56549154Ca',
   'cost_eth': 0.0029882715702859533,
   'cost_gwei': 2988271.570285953,
   'duration': 156.447,
   'effective_gas_price': 17995240067,
   'from': '0xcEB8dDd79E5C794c4CA8058B0f7fF8876533F168',
   'function': 'deactivate_ornamental_block',
   'gas_used': 166059,
   'hash': '0xcb022524caa29f3a0235d0f849cb0db7e16713c38e75ed6032a55bdbd8e5f863',
   'index': 110,
   'link': 'https://sepolia.etherscan.io/tx/0xcb022524caa29f3a0235d0f849cb0db7e16713c38e75ed6032a55bdbd8e5f863'}])

Press ENTER to continue...

********************* Extracting data from the first user **********************

>>> scm.get_user_data('0xaAF4b51A022adDE0dEb86CC7980Bc9859917e4A9')

{'cnpj': '31.345.604/0001-01',
 'company_name': 'qlqvxnnsxm',
 'email_address': 'contato@qlqvx.com',
 'last_update_timestamp': '2025/03/13, 15:03:44.124185',
 'list_index': 1,
 'ornamental_blocks_list': ['0x4b23d3e9f26576d6431027225Ad8711942067F83'],
 'registration_timestamp': '2025/03/13, 15:01:30.579235',
 'uid': '0xaAF4b51A022adDE0dEb86CC7980Bc9859917e4A9'}

Press ENTER to continue...

************ Extracting data from the deactivated ornamental block *************

>>> scm.get_ornamental_block_data('0xf295b3b4B947221a17A49541178192908dd30932')

{'code': 'tkmadvrhga',
 'hash': 'pH6O6Qm2xcEqEINNF6m1GU512CT5EduGl9TWrHUp2B',
 'invoice_numbers': [''],
 'is_active': False,
 'last_owners': ['0xaAF4b51A022adDE0dEb86CC7980Bc9859917e4A9',
                 '0x0000000000000000000000000000000000000000'],
 'last_update_timestamp': '2025/03/13, 15:03:44.124185',
 'list_index': 3,
 'mining_data': {'company': 'rmqczeqyupmlv',
                 'mining_date': 'eqykioyfew',
                 'mining_site': 'idqbfseefvyhn'},
 'properties': {'dimensions': '2.94, 2.07, 2.26',
                'material': 'bcbhpwfjrgipi',
                'weight': '2952'},
 'registration_timestamp': '2025/03/13, 15:02:08.126275',
 'uid': '0xf295b3b4B947221a17A49541178192908dd30932'}

Press ENTER to continue...

*************** Getting the inactive ornamental block uids list ****************

>>> scm.get_inactive_ornamental_block_uids_list()

['0xf295b3b4B947221a17A49541178192908dd30932']

Press ENTER to continue...

***************** Extracting all data from the smart contract ******************

>>> scm.get_contract_data()

{'ornamental_block_uids_list': ['0x4b23d3e9f26576d6431027225Ad8711942067F83',
                                '0xf998cc90532015Ec2Ce47718547782587380e6E8',
                                '0xc3D95B9f3fC2cAee393Dde48a759D021C87F3B67',
                                '0xf295b3b4B947221a17A49541178192908dd30932'],
 'ornamental_blocks_list': [{'code': 'lplwakoptm',
                             'hash': 'Yrh64Wyg5rtbXFYxsZHXclOAG006CfL4VJIQ5NCH42',
                             'invoice_numbers': [],
                             'is_active': True,
                             'last_owners': ['0xaAF4b51A022adDE0dEb86CC7980Bc9859917e4A9'],
                             'metadata': {'last_update_timestamp': '2025/03/13, '
                                                                   '15:02:08.126275',
                                          'list_index': 0,
                                          'registration_timestamp': '2025/03/13, '
                                                                    '15:02:08.126275',
                                          'uid': '0x4b23d3e9f26576d6431027225Ad8711942067F83'},
                             'mining_data': {'company': 'sfvalcpwhfed',
                                             'mining_date': 'myjmrimklz',
                                             'mining_site': 'wlgigydmggda'},
                             'properties': {'dimensions': '2.75, 1.47, 2.64',
                                            'material': 'cshfpdhruwqq',
                                            'weight': '3326'}},
                            {'code': 'fglrefxeii',
                             'hash': 'APGoKcGpxpz4YiuQmokab2Ts25tNyuBrZwOFH2MxMQ',
                             'invoice_numbers': ['5463674580'],
                             'is_active': True,
                             'last_owners': ['0xaAF4b51A022adDE0dEb86CC7980Bc9859917e4A9',
                                             '0x0d69aD522fc08D650D0FF6172fC9EEcc0EBC30CD'],
                             'metadata': {'last_update_timestamp': '2025/03/13, '
                                                                   '15:02:47.204032',
                                          'list_index': 1,
                                          'registration_timestamp': '2025/03/13, '
                                                                    '15:02:08.126275',
                                          'uid': '0xf998cc90532015Ec2Ce47718547782587380e6E8'},
                             'mining_data': {'company': 'rhjvyqmpjpr',
                                             'mining_date': 'famnzvgdqr',
                                             'mining_site': 'opijeqvzcms'},
                             'properties': {'dimensions': '2.31, 1.2, 2.06',
                                            'material': 'ymxhmkfroej',
                                            'weight': '6155'}},
                            {'code': 'nsviqliaue',
                             'hash': 'uLyJ2UTJpci18V1XiL8SIpbStn1EHWjwmRkc7XemEz',
                             'invoice_numbers': ['3627222684'],
                             'is_active': True,
                             'last_owners': ['0xaAF4b51A022adDE0dEb86CC7980Bc9859917e4A9',
                                             '0xcC3f20EaDA81AFdfA4D77d44d171306820DceF00'],
                             'metadata': {'last_update_timestamp': '2025/03/13, '
                                                                   '15:02:47.204032',
                                          'list_index': 2,
                                          'registration_timestamp': '2025/03/13, '
                                                                    '15:02:08.126275',
                                          'uid': '0xc3D95B9f3fC2cAee393Dde48a759D021C87F3B67'},
                             'mining_data': {'company': 'wwpcjwuhvubzsb',
                                             'mining_date': 'sapdaoiivz',
                                             'mining_site': 'uokzwawajbljyg'},
                             'properties': {'dimensions': '1.04, 1.92, 1.36',
                                            'material': 'msgblhyrpynfts',
                                            'weight': '4360'}},
                            {'code': 'tkmadvrhga',
                             'hash': 'pH6O6Qm2xcEqEINNF6m1GU512CT5EduGl9TWrHUp2B',
                             'invoice_numbers': [''],
                             'is_active': False,
                             'last_owners': ['0xaAF4b51A022adDE0dEb86CC7980Bc9859917e4A9',
                                             '0x0000000000000000000000000000000000000000'],
                             'metadata': {'last_update_timestamp': '2025/03/13, '
                                                                   '15:03:44.124185',
                                          'list_index': 3,
                                          'registration_timestamp': '2025/03/13, '
                                                                    '15:02:08.126275',
                                          'uid': '0xf295b3b4B947221a17A49541178192908dd30932'},
                             'mining_data': {'company': 'rmqczeqyupmlv',
                                             'mining_date': 'eqykioyfew',
                                             'mining_site': 'idqbfseefvyhn'},
                             'properties': {'dimensions': '2.94, 2.07, 2.26',
                                            'material': 'bcbhpwfjrgipi',
                                            'weight': '2952'}}],
 'recovered_contracts_address_list': ['0xb8996fC314bf3A7D89E3220ecc435E56549154Ca'],
 'user_uids_list': ['0xaAF4b51A022adDE0dEb86CC7980Bc9859917e4A9',
                    '0x0d69aD522fc08D650D0FF6172fC9EEcc0EBC30CD',
                    '0xcC3f20EaDA81AFdfA4D77d44d171306820DceF00'],
 'users_list': [{'cnpj': '31.345.604/0001-01',
                 'email_address': 'contato@qlqvx.com',
                 'metadata': {'last_update_timestamp': '2025/03/13, '
                                                       '15:03:44.124185',
                              'list_index': 1,
                              'registration_timestamp': '2025/03/13, '
                                                        '15:01:30.579235',
                              'uid': '0xaAF4b51A022adDE0dEb86CC7980Bc9859917e4A9'},
                 'name': 'qlqvxnnsxm',
                 'ornamental_blocks_list': ['0x4b23d3e9f26576d6431027225Ad8711942067F83']},
                {'cnpj': '79.105.754/0001-66',
                 'email_address': 'contato@xopnz.com',
                 'metadata': {'last_update_timestamp': '2025/03/13, '
                                                       '15:02:47.204032',
                              'list_index': 2,
                              'registration_timestamp': '2025/03/13, '
                                                        '15:01:30.579235',
                              'uid': '0x0d69aD522fc08D650D0FF6172fC9EEcc0EBC30CD'},
                 'name': 'xopnzcpkseo',
                 'ornamental_blocks_list': ['0xf998cc90532015Ec2Ce47718547782587380e6E8']},
                {'cnpj': '99.142.754/0001-43',
                 'email_address': 'contato@gfvqc.com',
                 'metadata': {'last_update_timestamp': '2025/03/13, '
                                                       '15:02:47.204032',
                              'list_index': 3,
                              'registration_timestamp': '2025/03/13, '
                                                        '15:01:30.579235',
                              'uid': '0xcC3f20EaDA81AFdfA4D77d44d171306820DceF00'},
                 'name': 'gfvqcoldbsw',
                 'ornamental_blocks_list': ['0xc3D95B9f3fC2cAee393Dde48a759D021C87F3B67']}]}

End of the example.
```