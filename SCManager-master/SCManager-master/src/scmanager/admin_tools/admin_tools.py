"""
admin_tools
===========

This module provides a set of administrative tools for managing smart contracts on the blockchain.
It includes functions for extracting, deploying, and configuring smart contracts, making it easier to interact with and
manage these contracts.

Imports
-------

- from ..sclink import SCLink
- from dotenv import load_dotenv
- from eth_account import Account
- from os import getenv
- from solcx import compile_source, install_solc
- from solcx.exceptions import SolcError, SolcNotInstalled
- from typing import Any
- from web3 import contract as web3_contract
- import json

Functions
---------

1. extract_code(sclink: SCLink) -> tuple[web3_contract, dict[str, Any]]:
    Extracts a contract and returns it formatted for the blockchain with deployment information.

2. create_config_file(endpoint_env_key: str, private_environment_key: str, file_name: str) -> None:
    Creates a configuration file for the smart contract deployment environment.

3. deploy_sc(contract_address_to_recover: str = '0x' + '0' * 40,
             path_to_config_file: str = 'sc_config.json',
             timeout: int = 120,
             persist: int = 0) -> dict[str, Any] | None:
    Deploys a smart contract to the blockchain.

Usage
-----

To use this module, import it and call the desired functions with the appropriate parameters. For example:

    from admin_tools import extract_code, create_config_file, deploy_sc

    # Create a configuration file
    create_config_file(endpoint_env_key='your_endpoint_environment_key',
                       private_environment_key='your_private_environment_key',
                       file_name='config')

    # Extract and deploy a smart contract
    sclink = SCLink(endpoint='https://example.com')
    contract, contract_info = extract_code(sclink=sclink)
    deployment_info = deploy_sc(path_to_config_file='config')

This module simplifies the process of managing smart contracts, providing a streamlined interface for common tasks.

Environment
-----------

The module uses environment variables loaded from a .env file to manage sensitive information such as private keys.
Ensure that the .env file is properly configured and loaded using `load_dotenv(override=True)`.

Dependencies
------------

- sclink: Provides the SCLink class for blockchain interactions.
- dotenv: Loads environment variables from a .env file.
- eth_account: Manages Ethereum accounts and signing transactions.
- os: Provides functions to interact with the operating system.
- solcx: Compiles Solidity source code and manages Solidity compiler versions.
- typing: Provides type hints for function signatures.
- web3: Interacts with the Ethereum blockchain.
- json: Handles JSON data.

"""
from solcx.exceptions import SolcError, SolcNotInstalled
from solcx import compile_source, install_solc
from web3 import contract as web3_contract
from eth_account import Account
from dotenv import load_dotenv
from datetime import datetime
from ..sclink import SCLink
from pathlib import Path
from typing import Any
from os import getenv
import json
load_dotenv(override=True)


def _extract_code(sclink: SCLink) -> tuple[web3_contract, dict[str, Any]]:
    """
    Extracts a solidity contract and returns it formatted for the blockchain with deployment information.

    This method reads the contract code from a solidity file, compiles it, and prepares it for deployment on the
    blockchain.

    :param sclink: An instance of the SCLink class that provides a connection to the blockchain.
    :type sclink: SCLink
    :return: A tuple containing:
        - contract: The extracted and formatted contract ready for deployment.
        - contract_info: A dictionary containing the contract's deployment information, including:
            - address: The address of the contract (initially empty).
            - version: The version of the contract.
            - description: A description of the contract.
            - code: The Solidity code of the contract.
            - abi: The ABI (Application Binary Interface) of the contract.
            - bin: The bytecode of the contract.
    :rtype: tuple[web3_contract, dict[str, Any]]
    """
    this_path = str(Path(__file__))
    with open(this_path[:this_path.index('admin_tools.py')] + 'smart_contract.sol', "r", encoding="utf-8") as file:
        text = file.readlines()
    text.pop(0)
    contract_info = {'address': '',
                     'version': text.pop(0).split(': ')[1].replace('\n', ''),
                     'description': text.pop(0).split(': ')[1].replace('\n', '')}
    text.pop(0)
    contract_info['code'] = ''.join(_ for _ in text if _ != '\n')
    sol_version = contract_info['code'].split(' ^')[1].split(';')[0]
    try:
        compiled_sol = compile_source(source=contract_info['code'],
                                      output_values=['abi', 'bin'],
                                      solc_version=sol_version)
    except (SolcError, SolcNotInstalled):  # pragma: no cover
        install_solc(sol_version)
        compiled_sol = compile_source(source=contract_info['code'],
                                      output_values=['abi', 'bin'],
                                      solc_version=sol_version)
    _, solidity_info = compiled_sol.popitem()
    contract = sclink.web3.eth.contract(abi=solidity_info['abi'],
                                        bytecode=solidity_info['bin'])
    contract_info.update({'abi': json.dumps(solidity_info['abi']),
                          'bin': solidity_info['bin']})
    return contract, contract_info


def deploy_smart_contract(contract_address_to_recover: str = '0x' + '0' * 40,
                          config_file: str = 'scm_config.json',
                          timeout: int = 120,
                          persist: int = 0) -> dict[str, Any] | None:
    """
    Deploys a smart contract to the blockchain.

    This method reads the configuration file, extracts and compiles the smart contract code, and deploys the contract
    to the blockchain. It also updates the configuration file with the contract's deployment information.

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
    if config_file[-5:] != '.json':  # pragma: no cover
        config_file = f"{config_file}.json"
    with open(f"scm_config/{config_file}", 'r', encoding='utf-8') as file:
        config_data = json.load(file)
    sclink = SCLink(
        endpoint=getenv(config_data['endpoint_environment_key']))
    contract, contract_info = _extract_code(sclink=sclink)
    account = Account.from_key(private_key=str(getenv(config_data['private_environment_key'])))
    timestamp = datetime.now().strftime("%Y/%m/%d, %H:%M:%S.%f")
    transaction_data = sclink.build_and_send_transaction(
        contract_function=contract.constructor(contract_address_to_recover),
        account=account,
        timeout=timeout,
        persist=persist,
        estimate_cost=True)
    if not transaction_data:  # pragma: no cover
        return None
    contract_info['address'] = transaction_data['contract_address']
    config_data.update({'contract': contract_info,
                        'deployer': account.address})
    with open(f"scm_config/{config_file}", 'w', encoding='utf-8') as file:
        json.dump(config_data, file, ensure_ascii=False, indent=4)
    log_directory = f"scm_config/{''.join(config_file.split('/')[:-1]) + '/' if '/' in config_file else ''}"
    Path(f"{log_directory}logs").mkdir(parents=True, exist_ok=True)
    log_info = {'operation': 'contract creation',
                'timestamp': timestamp,
                'output': [contract_info],
                'transactions': [transaction_data]}
    log_file_name = f"log_{contract_info['address']}.json"

    with open(f"{log_directory}logs/{log_file_name}", 'w', encoding='utf-8') as f:
        json.dump([log_info], f, ensure_ascii=False, indent=4)
    return config_data


def create_config_file(endpoint_environment_key: str = 'ETHEREUM_ENDPOINT',
                       private_environment_key: str = 'ETHEREUM_PRIVATE_KEY',
                       file_name: str = 'scm_config.json',
                       deploy: bool = True) -> dict[str, Any] | None:
    """
    Creates a configuration file for the smart contract deployment environment.

    This method generates a JSON configuration file with the provided endpoint link and private environment key.

    :param endpoint_environment_key: The environment key for the endpoint link of the blockchain network.
    :type endpoint_environment_key: str
    :param private_environment_key: The key for the environment variable containing the account private key.
    :type private_environment_key: str
    :param file_name: The name of the configuration file to be created.
    :type file_name: str
    :param deploy: If True, calls the deploy_smart_contract() method with it's default values.
    :type deploy: bool
    :return: If deploy is True, returns dictionary containing the updated configuration data, including the contract's
    deployment information, else returns None
    :rtype: dict[str, Any] | None
    """
    config_data = {'contract': {},
                   'deployer': '',
                   'endpoint_environment_key': endpoint_environment_key,
                   'private_environment_key': private_environment_key}
    Path("scm_config").mkdir(parents=True, exist_ok=True)
    if file_name[-5:] != '.json':  # pragma: no cover
        file_name = f"{file_name}.json"
    with open(f"scm_config/{file_name}", 'w', encoding='utf-8') as config_file:
        json.dump(config_data, config_file, ensure_ascii=False, indent=4)
    print(f"Config file successfully created at: scm_config/{file_name}")
    if deploy:  # pragma: no cover
        return deploy_smart_contract(config_file=file_name)
