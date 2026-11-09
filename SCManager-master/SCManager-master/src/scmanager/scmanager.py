"""
scmanager
=========

This module provides the SCManager class, which is used to interact with a smart contract on the Ethereum blockchain.
The class includes methods for retrieving user and ornamental block data, adding new users and blocks,
transferring ownership, and deactivating blocks.

Imports
-------

- from .exceptions import InvalidParameterError
- from .sclink import SCLink
- from datetime import datetime
- from dotenv import load_dotenv
- from eth_account import Account
- from eth_account.signers.local import LocalAccount
- from eth_typing import ChecksumAddress
- import json
- from math import ceil
- from os import getenv
- from typing import Any, Callable
- from web3 import Web3, contract as web3_contract

Classes
-------

1. SCManager:
    A class used to represent a Smart Contract Manager.

    Methods
    -------
    - __init__(path_to_config_file: str = 'sc_config.json', *, timeout: int = 120, persist: int = 0,
    show: bool = False)
        Initializes the SCManager object with the necessary attributes.
    - get_account_balance() -> float
        Retrieves the balance of the account associated with this instance in Ether.
    - get_contract_data() -> dict[str, list]
        Retrieves the contract data from the smart contract.
    - get_last_updated_timestamp() -> str
        Retrieves the timestamp of the last update to the smart contract.
    - get_inactive_ornamental_block_uids_list() -> list[ChecksumAddress]
        Retrieves a list of inactive ornamental block UIDs.
    - get_user_uids_list() -> list[ChecksumAddress]
        Retrieves a list of user UIDs.
    - get_ornamental_block_uids_list() -> list[ChecksumAddress]
        Retrieves a list of ornamental block UIDs.
    - is_user(uid: ChecksumAddress) -> bool
        Checks if a given UID is a valid user UID.
    - is_ornamental_block(uid: ChecksumAddress) -> bool
        Checks if a given UID is a valid ornamental block UID.
    - get_user_data(user_uid: ChecksumAddress) -> dict[str, Any]
        Retrieves data for a specified user.
    - get_ornamental_block_data(ornamental_block_uid: ChecksumAddress) -> dict[str, Any]
        Retrieves data for a specified ornamental block.
    - is_ornamental_block_active(ornamental_block_uid: ChecksumAddress) -> bool
        Checks if a given ornamental block UID is active.
    - add_new_users(user_name_list: list[str], user_cnpj_list: list[str], user_email_address_list: list[str],
    estimate_cost: bool = False) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]
        Adds new users to the smart contract.
    - add_new_ornamental_blocks(mining_data_list: list[dict[str, str]], code_list: list[str],
    properties_list: list[dict[str, str]], hash_list: list[str], owners_uid_list: list[ChecksumAddress],
    estimate_cost: bool = False) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]
        Adds new ornamental blocks to the smart contract.
    - transfer_ornamental_blocks(ornamental_block_uid_list: list[ChecksumAddress],
    new_owner_uid_list: list[ChecksumAddress], invoice_number_list: list[str],
    estimate_cost: bool = False) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]
        Transfers ownership of ornamental blocks in the smart contract.
    - deactivate_ornamental_blocks(ornamental_block_uid_list: list[ChecksumAddress],
    estimate_cost: bool = False) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]
        Deactivates ornamental blocks in the smart contract.
    - _extract_new_user_args(user_data: dict[str, list], list_length: int) -> dict[str, Any]
        Extracts arguments for adding new users to the smart contract.
    - _extract_new_ob_args(ornamental_block_data: dict[str, list], list_length: int) -> dict[str, Any]
        Extracts arguments for adding new ornamental blocks to the smart contract.
    - _extract_transfer_ob_args(transfer_data: dict[str, list], list_length: int) -> dict[str, Any]
        Extracts arguments for transferring ownership of ornamental blocks.
    - _extract_deactivate_ob_args(ornamental_block_data: dict[str, list], list_length: int) -> dict[str, Any]
        Extracts arguments for deactivating ornamental blocks.
    - _check_type_list(list_: list, type_: type) -> bool
        Checks if all elements in a list are of a specified type.
    - _process_user_list(raw_user_list: list) -> list[dict[str, Any]]
        Processes a raw list of user data extracted from the smart contract into a structured format.
    - _process_ornamental_block_list(raw_ornamental_block_list: list) -> list[dict[str, Any]]
        Processes a raw list of ornamental block data extracted from the smart contract into a structured format.
    - _verify_list_parameters(data: list[ChecksumAddress], function_name: str) -> list
        Verifies the parameters of a list based on the specified function name.
    - _verify_dictionary_parameters(data: dict[str, list], function_name: str) -> dict[str, list[str]]
        Verifies the parameters of a dictionary based on the specified function name.
    - _make_transaction(sc_functions_list: list[web3_contract], extract_args_function: Callable[[dict[str, list], int],
    dict[str, Any]], data: dict[str, list], account: LocalAccount, sclink: SCLink, timeout: int = 120,
    persist: int = 0, estimate_cost: bool = False) -> list[dict[str, Any]]
        Executes transactions on the smart contract.

Usage
-----

To use this module, import the SCManager class and create an instance with the appropriate configuration file.
For example:

    from scmanager import SCManager

    # Create an instance of SCManager:
    scmanager = SCManager(path_to_config_file='path/to/config.json')

    # Get the balance of the account:
    balance = scmanager.get_account_balance()
    print(f"Account balance: {balance} Ether")

    # Add new users:
    new_users, transactions = scmanager.add_new_users(
        user_name_list=['Alice', 'Bob'],
        user_cnpj_list=['12345678901234', '98765432109876'],
        user_email_address_list=['alice@example.com', 'bob@example.com']
    )
    print(f"New users: {new_users}")

This module simplifies the process of interacting with the smart contract,
providing a streamlined interface for common tasks.

Dependencies
------------

- dotenv: Loads environment variables from a .env file.
- eth_account: Manages Ethereum accounts and signing transactions.
- eth_typing: Provides type hints for Ethereum-related data types.
- json: Handles JSON data.
- math: Provides mathematical functions.
- os: Provides a way of using operating system dependent functionality.
- typing: Provides type hints for function signatures.
- web3: Interacts with the Ethereum blockchain.
"""

from .exceptions import InvalidParameterError
from .sclink import SCLink
from datetime import datetime
from dotenv import load_dotenv
from eth_account import Account
from eth_account.signers.local import LocalAccount
from eth_typing import ChecksumAddress
import json
from math import ceil
from os import getenv
from typing import Any, Callable
from web3 import Web3, contract as web3_contract

load_dotenv(override=True)
ADDRESS_0 = Web3.to_checksum_address('0x' + '0' * 40)


class SCManager:
    """
    A class used to represent a Smart Contract Manager.

    This class provides methods to interact with a smart contract on the Ethereum blockchain, including retrieving user
    and ornamental block data, adding new users and blocks, transferring ownership, and deactivating blocks.

    Attributes
    ----------
    timeout : int
        The timeout duration for transactions in seconds.
    persist : int
        The number of times to retry transactions in case of failure.
    sclink : SCLink
        The SCLink object for interacting with the smart contract.
    account : LocalAccount
        The account used for signing transactions.
    web3_contract_object : web3_contract.Contract
        The smart contract instance.
    administrator_address : ChecksumAddress
        The address of the smart contract administrator.

    Methods
    -------
    __init__(path_to_config_file: str = 'sc_config.json', *, timeout: int = 120, persist: int = 0,
    show: bool = False)
        Initializes the SCManager object with the necessary attributes.
    get_account_balance() -> float
        Retrieves the balance of the account associated with this instance in Ether.
    get_contract_data() -> dict[str, list]
        Retrieves the contract data from the smart contract.
    get_last_updated_timestamp() -> str
        Retrieves the timestamp of the last update to the smart contract.
    get_inactive_ornamental_block_uids_list() -> list[ChecksumAddress]
        Retrieves a list of inactive ornamental block UIDs.
    get_user_uids_list() -> list[ChecksumAddress]
        Retrieves a list of user UIDs.
    get_ornamental_block_uids_list() -> list[ChecksumAddress]
        Retrieves a list of ornamental block UIDs.
    is_user(uid: ChecksumAddress) -> bool
        Checks if a given UID is a valid user UID.
    is_ornamental_block(uid: ChecksumAddress) -> bool
        Checks if a given UID is a valid ornamental block UID.
    get_user_data(user_uid: ChecksumAddress) -> dict[str, Any]
        Retrieves data for a specified user.
    get_ornamental_block_data(ornamental_block_uid: ChecksumAddress) -> dict[str, Any]
        Retrieves data for a specified ornamental block.
    is_ornamental_block_active(ornamental_block_uid: ChecksumAddress) -> bool
        Checks if a given ornamental block UID is active.
    add_new_users(user_name_list: list[str], user_cnpj_list: list[str], user_email_address_list: list[str],
    estimate_cost: bool = False) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]
        Adds new users to the smart contract.
    add_new_ornamental_blocks(mining_data_list: list[dict[str, str]], code_list: list[str],
    properties_list: list[dict[str, str]], hash_list: list[str], owners_uid_list: list[ChecksumAddress],
    estimate_cost: bool = False) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]
        Adds new ornamental blocks to the smart contract.
    transfer_ornamental_blocks(ornamental_block_uid_list: list[ChecksumAddress],
    new_owner_uid_list: list[ChecksumAddress], invoice_number_list: list[str],
    estimate_cost: bool = False) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]
        Transfers ownership of ornamental blocks in the smart contract.
    deactivate_ornamental_blocks(ornamental_block_uid_list: list[ChecksumAddress],
    estimate_cost: bool = False) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]
        Deactivates ornamental blocks in the smart contract.
    _extract_new_user_args(user_data: dict[str, list], list_length: int) -> dict[str, Any]
        Extracts arguments for adding new users to the smart contract.
    _extract_new_ob_args(ornamental_block_data: dict[str, list], list_length: int) -> dict[str, Any]
        Extracts arguments for adding new ornamental blocks to the smart contract.
    _extract_transfer_ob_args(transfer_data: dict[str, list], list_length: int) -> dict[str, Any]
        Extracts arguments for transferring ownership of ornamental blocks.
    _extract_deactivate_ob_args(ornamental_block_data: dict[str, list], list_length: int) -> dict[str, Any]
        Extracts arguments for deactivating ornamental blocks.
    _check_type_list(list_: list, type_: type) -> bool
        Checks if all elements in a list are of a specified type.
    _process_user_list(raw_user_list: list) -> list[dict[str, Any]]
        Processes a raw list of user data extracted from the smart contract into a structured format.
    _process_ornamental_block_list(raw_ornamental_block_list: list) -> list[dict[str, Any]]
        Processes a raw list of ornamental block data extracted from the smart contract into a structured format.
    _verify_list_parameters(data: list[ChecksumAddress], function_name: str) -> list
        Verifies the parameters of a list based on the specified function name.
    _verify_dictionary_parameters(data: dict[str, list], function_name: str) -> dict[str, list[str]]
        Verifies the parameters of a dictionary based on the specified function name.
    _make_transaction(sc_functions_list: list[web3_contract], extract_args_function: Callable[[dict[str, list], int],
    dict[str, Any]], data: dict[str, list], account: LocalAccount, sclink: SCLink, timeout: int = 120,
    persist: int = 0, estimate_cost: bool = False) -> list[dict[str, Any]]
        Executes transactions on the smart contract.
    """
    def __init__(self,
                 config_file: str = 'scm_config.json', *,
                 timeout: int = 120,
                 persist: int = 0,
                 show: bool = False):
        """
        Initializes the SCManager object with the necessary attributes.

        This method reads the smart contract configuration from a file, initializes the SCLink object, and sets up the
        smart contract instance.

        :param config_file: The configuration file inside the folder scm_config containing smart contract information
        inside the folder scm_config.
        :type config_file: str
        :param timeout: The timeout duration for transactions in seconds.
        :type timeout: int
        :param persist: The number of times to retry transactions in case of failure.
        :type persist: int
        :param show: If True, prints the SCManager object information.
        :type show: bool
        """
        if config_file[-5:] != '.json':  # pragma: no cover
            config_file = f"{config_file}.json"
        with open(f"scm_config/{config_file}", 'r', encoding='utf-8') as file:
            smart_contract_information = json.load(file)
        self.log_directory = f"scm_config/{''.join(config_file.split('/')[:-1]) + '/' if '/' in config_file else ''}"
        self.timeout = timeout
        self.persist = persist
        self.sclink = SCLink(
            endpoint=getenv(smart_contract_information['endpoint_environment_key']))
        self.account = Account.from_key(
            private_key=str(getenv(smart_contract_information['private_environment_key'])))
        self.web3_contract_object = self.sclink.get_contract(
            contract_address=smart_contract_information['contract']['address'],
            abi=json.loads(smart_contract_information['contract']['abi']))

        self.administrator_address = self.web3_contract_object.functions.ADMINISTRATOR().call()
        if show:  # pragma: no cover
            print(self)

    def __repr__(self) -> str:
        data = self.get_contract_data()
        bin_ = self.get_inactive_ornamental_block_uids_list()
        text = f"Contract {data['recovered_contracts_address_list'][-1]} connected:\n"
        text += (f"\t{len(data['users_list'])} user(s) and {len(data['ornamental_block_uids_list']) - len(bin_)} "
                 f"active ornamental block(s) found:\n")

        for user in data['users_list']:
            uid = user['metadata']['uid']
            text += (f"\t\tUser {user['metadata']['list_index']: >2} - uid {uid} "
                     f"with {len(user['ornamental_blocks_list'])} ornamental block(s):\n")

            for block_uid in user['ornamental_blocks_list']:
                index = data['ornamental_block_uids_list'].index(block_uid)
                block = data['ornamental_blocks_list'][index]
                text += f"\t\t\tBlock {block['metadata']['list_index']: >3} - uid {block_uid}\n"

        text += f"\tDump list ({len(bin_)} inactive block(s)):\n"
        for block_uid in bin_:
            index = data['ornamental_block_uids_list'].index(block_uid)
            block = data['ornamental_blocks_list'][index]
            text += f"\t\tBlock {block['metadata']['list_index']: >3} - uid {block_uid}\n"
        return text

    @SCLink.connection_checker
    def get_account_balance(self) -> float:
        """
        Retrieves the balance of the account associated with this instance in Ether.

        This method fetches the balance of the account from the blockchain.

        :return: The balance of the account in Ether.
        :rtype: float
        """
        return self.sclink.get_balance(self.account.address)

    @SCLink.connection_checker
    def get_contract_data(self) -> dict[str, list]:
        """
        Retrieves the contract data from the smart contract.

        This method calls the smart contract function `get_contract_data`
        and processes the returned data into a dictionary.

        :return: A dictionary containing the following keys:
            - recovered_contracts_address_list: A list of the previous recovered contract addresses.
            - user_uids_list: A list of user unique identifiers (UIDs).
            - users_list: A list of users information dictionaries.
            - ornamental_block_uids_list: A list of ornamental block UIDs.
            - ornamental_blocks_list: A list of ornamental block information.
        :rtype: dict[str, list]
        """
        contract_data_list = self.web3_contract_object.functions.get_contract_data().call()
        return {'recovered_contracts_address_list': contract_data_list[0],
                'user_uids_list': contract_data_list[1][1:],
                'users_list': self._process_user_list(contract_data_list[2])[1:],
                'ornamental_block_uids_list': contract_data_list[3],
                'ornamental_blocks_list': self._process_ornamental_block_list(contract_data_list[4])}

    @SCLink.connection_checker
    def get_last_updated_timestamp(self) -> str:
        """
        Retrieves the timestamp of the last update to the smart contract.

        This method calls the smart contract function `get_last_updated_timestamp`
        to get the timestamp of the last update.

        :return: The timestamp of the last update as a string.
        :rtype: str
        """
        return self.web3_contract_object.functions.get_last_updated_timestamp().call()

    @SCLink.connection_checker
    def get_inactive_ornamental_block_uids_list(self) -> list[ChecksumAddress]:
        """
        Retrieves a list of inactive ornamental block UIDs.

        This method calls the smart contract function `get_user_data` with a specific address
        to get the list of inactive ornamental block UIDs.

        :return: A list of inactive ornamental block UIDs.
        :rtype: list[ChecksumAddress]
        """
        return self.web3_contract_object.functions.get_user_data(ADDRESS_0).call()[7]

    @SCLink.connection_checker
    def get_user_uids_list(self) -> list[ChecksumAddress]:
        """
        Retrieves a list of user UIDs.

        This method calls the smart contract function `get_user_uids_list` to get the list of user UIDs.

        :return: A list of user UIDs.
        :rtype: list[ChecksumAddress]
        """
        return self.web3_contract_object.functions.get_user_uids_list().call()[1:]

    @SCLink.connection_checker
    def get_ornamental_block_uids_list(self) -> list[ChecksumAddress]:
        """
        Retrieves a list of ornamental block UIDs.

        This method calls the smart contract function `get_ornamental_block_uids_list`
        to get the list of ornamental block UIDs.

        :return: A list of ornamental block UIDs.
        :rtype: list[ChecksumAddress]
        """
        return self.web3_contract_object.functions.get_ornamental_block_uids_list().call()

    @SCLink.connection_checker
    def is_user(self,
                uid: ChecksumAddress) -> bool:
        """
        Checks if a given UID is a valid user UID.

        This method validates the provided unique identifier (UID) and then calls the
        smart contract function `is_user` to check if the UID corresponds to a registered user.

        :param uid: The user UID to check.
        :type uid: ChecksumAddress
        :return: True if the user UID is valid, False otherwise.
        :rtype: bool
        :raises InvalidParameterError: If the provided user UID is not a valid checksum address or is a null address.
        """
        if not Web3.is_checksum_address(uid):
            raise InvalidParameterError(f"{uid} is not a valid user uid")
        elif uid == ADDRESS_0:
            return False
        return self.web3_contract_object.functions.is_user(uid).call()

    @SCLink.connection_checker
    def is_ornamental_block(self,
                            uid: ChecksumAddress) -> bool:
        """
        Checks if a given UID is a valid ornamental block UID.

        This method validates the provided unique identifier (UID) and then
        calls the smart contract function `is_ornamental_block` to check if the UID corresponds
        to a registered ornamental block.

        :param uid: The ornamental block UID to check.
        :type uid: ChecksumAddress
        :return: True if the ornamental block UID is valid, False otherwise.
        :rtype: bool
        :raises InvalidParameterError: If the provided ornamental block UID is not a valid checksum address
        or is a null address.
        """
        if not Web3.is_checksum_address(uid):
            raise InvalidParameterError(f"{uid} is not a valid ornamental block uid")
        return self.web3_contract_object.functions.is_ornamental_block(uid).call()

    @SCLink.connection_checker
    def get_user_data(self,
                      user_uid: ChecksumAddress) -> dict[str, Any]:
        """
        Retrieves data for a specified user.

        This method checks if the provided user UID is valid and then calls
        the smart contract function `get_user_data` to retrieve the user's data.

        :param user_uid: The user UID to retrieve data for.
        :type user_uid: ChecksumAddress
        :return: A dictionary containing the following keys:
            - uid: The user's unique identifier (UID).
            - list_index: The index of the user in the user list.
            - registration_timestamp: The timestamp of the user's registration.
            - last_update_timestamp: The timestamp of the user's last update.
            - company_name: The company name associated with the user.
            - cnpj: The CNPJ (Cadastro Nacional da Pessoa Jurídica) of the user's company.
            - email_address: The email address associated with the user.
            - ornamental_blocks_list: A list of ornamental block UIDs associated with the user.
        :rtype: dict[str, Any]
        :raises InvalidParameterError: If the provided user UID is not from a valid user.
        """
        if not self.is_user(user_uid):
            raise InvalidParameterError(f"User uid {user_uid} not found")
        raw_data = self.web3_contract_object.functions.get_user_data(user_uid).call()
        return {'uid': raw_data[0],
                'list_index': raw_data[1],
                'registration_timestamp': raw_data[2],
                'last_update_timestamp': raw_data[3],
                'company_name': raw_data[4],
                'cnpj': raw_data[5],
                'email_address': raw_data[6],
                'ornamental_blocks_list': raw_data[7]}

    @SCLink.connection_checker
    def get_ornamental_block_data(self,
                                  ornamental_block_uid: ChecksumAddress) -> dict[str, Any]:
        """
        Retrieves data for a specified ornamental block.

        This method checks if the provided ornamental block UID is valid and then calls
        the smart contract function `get_ornamental_block_data` to retrieve the block's data.

        :param ornamental_block_uid: The ornamental block UID to retrieve data for.
        :type ornamental_block_uid: ChecksumAddress
        :return: A dictionary containing the following keys:
            - uid: The ornamental block's unique identifier (UID).
            - list_index: The index of the ornamental block in the block list.
            - registration_timestamp: The timestamp of the ornamental block's registration.
            - last_update_timestamp: The timestamp of the ornamental block's last update.
            - mining_data: A dictionary containing the mining data with the following keys:
                - company: The company responsible for the mining.
                - mining_date: The date when the mining occurred.
                - mining_site: The site where the mining took place.
            - code: The code associated with the ornamental block.
            - properties: A dictionary containing the properties of the ornamental block with the following keys:
                - dimensions: The dimensions of the ornamental block.
                - material: The material of the ornamental block.
                - weight: The weight of the ornamental block.
            - hash: The hash of the ornamental block.
            - is_active: The active status of the ornamental block.
            - last_owners: The list of last owners of the ornamental block.
            - invoice_numbers: The list of invoice numbers associated with the ornamental block.
        :rtype: dict[str, Any]
        :raises InvalidParameterError: If the provided ornamental block UID is not from a valid ornamental block.
        """
        if not self.is_ornamental_block(ornamental_block_uid):
            raise InvalidParameterError(f"Ornamental block uid {ornamental_block_uid} not found")
        raw_data = self.web3_contract_object.functions.get_ornamental_block_data(ornamental_block_uid).call()
        return {'uid': raw_data[0],
                'list_index': raw_data[1],
                'registration_timestamp': raw_data[2],
                'last_update_timestamp': raw_data[3],
                'mining_data': json.loads(raw_data[4]),
                'code': raw_data[5],
                'properties': json.loads(raw_data[6]),
                'hash': raw_data[7],
                'is_active': raw_data[8],
                'last_owners': raw_data[9],
                'invoice_numbers': raw_data[10]}

    @SCLink.connection_checker
    def is_ornamental_block_active(self,
                                   ornamental_block_uid) -> bool:
        """
        Checks if a given ornamental block is active.

        This method validates the provided ornamental block UID and then calls the
        smart contract function `is_ornamental_block_active` to check if the block is active.

        :param ornamental_block_uid: The ornamental block UID to check.
        :type ornamental_block_uid: ChecksumAddress
        :return: True if the ornamental block is active, False otherwise.
        :rtype: bool
        :raises InvalidParameterError: If the provided ornamental block UID
            is not a valid checksum address or is the zero address.
        """
        if not self.is_ornamental_block(ornamental_block_uid):
            raise InvalidParameterError(f"Ornamental block uid {ornamental_block_uid} not found")
        return self.web3_contract_object.functions.is_ornamental_block_active(ornamental_block_uid).call()

    @SCLink.connection_checker
    def add_new_users(self, *,
                      user_name_list: list[str],
                      user_cnpj_list: list[str],
                      user_email_address_list: list[str],
                      estimate_cost: bool = False) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """
        Adds new users to the smart contract.

        This method adds new users to the smart contract with the provided user data. It supports adding multiple users
        in a single transaction and can estimate the cost of the transactions if required.

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
        def get_new_users_data_list(starting_index: int):
            user_uids_list = self.get_user_uids_list()
            new_users_uids_list = user_uids_list[starting_index:]
            new_users_list = []
            for index in range(number_of_new_users):
                user_data = self.get_user_data(new_users_uids_list[index])
                new_users_list.append(user_data)
            return new_users_list

        user_data_dict = {'user_name_list': user_name_list,
                          'user_cnpj_list': user_cnpj_list,
                          'user_email_address_list': user_email_address_list}

        self._verify_dictionary_parameters(user_data_dict,
                                           'add_new_users')

        number_of_new_users = len(user_data_dict['user_name_list'])
        number_of_users_added_before = len(self.get_user_uids_list())
        new_user_functions = [self.web3_contract_object.functions.add_new_user,
                              self.web3_contract_object.functions.add_up_to_5_new_users,
                              self.web3_contract_object.functions.add_up_to_20_new_users]

        transactions_list = self._make_transaction(sc_functions_list=new_user_functions,
                                                   extract_args_function=self._extract_new_user_args,
                                                   data=user_data_dict,
                                                   account=self.account,
                                                   sclink=self.sclink,
                                                   timeout=self.timeout,
                                                   persist=self.persist,
                                                   estimate_cost=estimate_cost)
        new_users_data_list = get_new_users_data_list(number_of_users_added_before)
        self._write_output_log(directory=self.log_directory,
                               operation=f"add {len(new_users_data_list)} new users",
                               output_data=new_users_data_list,
                               transactions_data=transactions_list)
        return new_users_data_list, transactions_list

    @SCLink.connection_checker
    def add_new_ornamental_blocks(self, *,
                                  mining_data_list: list[dict[str, str]],
                                  code_list: list[str],
                                  properties_list: list[dict[str, str]],
                                  hash_list: list[str],
                                  owners_uid_list: list[ChecksumAddress],
                                  estimate_cost: bool = False) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """
        Adds new ornamental blocks to the smart contract.

        This method adds new ornamental blocks to the smart contract with the provided block data.
        It supports adding multiple blocks in a single transaction and
        can estimate the cost of the transactions if required.

        :param mining_data_list: A list of dictionaries containing the mining data for each block,
        with the following keys:
            - company (str): The company responsible for the mining.
            - mining_date (str): The date when the mining occurred.
            - mining_site (str): The site where the mining took place.
        :type mining_data_list: list[dict[str, str]]
        :param code_list: A list of codes associated with the ornamental blocks.
        :type code_list: list[str]
        :param properties_list: A list of dictionaries containing the properties of each block,
        with the following keys:
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
            - new_ornamental_blocks_data_list: A list of dictionaries with the data of the
            newly added ornamental blocks.
            - transactions_list: A list of dictionaries with the details of the transactions performed.
        :rtype: tuple[list[dict[str, Any]], list[dict[str, Any]]]
        :raises InvalidParameterError: If any of the provided block data lists are invalid.
        """

        def get_new_ornamental_blocks_data_list(starting_index: int):
            ob_uids_list = self.get_ornamental_block_uids_list()
            new_obs_uids_list = ob_uids_list[starting_index:]
            new_obs_list = []
            for index in range(len(new_obs_uids_list)):
                ob_data = self.get_ornamental_block_data(new_obs_uids_list[index])
                new_obs_list.append(ob_data)
            return new_obs_list

        ornamental_block_data_dict = {'mining_data_list': mining_data_list,
                                      'code_list': code_list,
                                      'properties_list': properties_list,
                                      'hash_list': hash_list,
                                      'owners_uid_list': owners_uid_list}

        self._verify_dictionary_parameters(ornamental_block_data_dict,
                                           'add_new_ornamental_blocks')

        number_of_obs_before = len(self.get_ornamental_block_uids_list())
        new_ob_functions = [self.web3_contract_object.functions.add_new_ornamental_block,
                            self.web3_contract_object.functions.add_up_to_5_new_ornamental_blocks,
                            self.web3_contract_object.functions.add_up_to_20_new_ornamental_blocks]

        transactions_list = self._make_transaction(sc_functions_list=new_ob_functions,
                                                   extract_args_function=self._extract_new_ob_args,
                                                   data=ornamental_block_data_dict,
                                                   account=self.account,
                                                   sclink=self.sclink,
                                                   timeout=self.timeout,
                                                   persist=self.persist,
                                                   estimate_cost=estimate_cost)
        new_ornamental_blocks_data_list = get_new_ornamental_blocks_data_list(number_of_obs_before)
        self._write_output_log(directory=self.log_directory,
                               operation=f"add {len(new_ornamental_blocks_data_list)} new ornamental blocks",
                               output_data=new_ornamental_blocks_data_list,
                               transactions_data=transactions_list)
        return new_ornamental_blocks_data_list, transactions_list

    @SCLink.connection_checker
    def transfer_ornamental_blocks(self, *,
                                   ornamental_block_uid_list: list[ChecksumAddress],
                                   new_owner_uid_list: list[ChecksumAddress],
                                   invoice_number_list: list[str],
                                   estimate_cost: bool = False) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """
        Transfers ownership of ornamental blocks in the smart contract.

        This method transfers the ownership of ornamental blocks to new owners with the provided data.
        It supports transferring multiple blocks in a single transaction and
        can estimate the cost of the transactions if required.

        :param ornamental_block_uid_list: A list of UIDs of the ornamental blocks to be transferred.
        :type ornamental_block_uid_list: list[ChecksumAddress]
        :param new_owner_uid_list: A list of UIDs of the new owners.
        :type new_owner_uid_list: list[ChecksumAddress]
        :param invoice_number_list: A list of invoice numbers associated with the transfers.
        :type invoice_number_list: list[str]
        :param estimate_cost: If True, estimates and display the Ether cost for the transactions before executing them.
        :type estimate_cost: bool
        :return: A tuple containing two lists:
            - transfered_ornamental_blocks_data_list: A list of dictionaries with the
            data of the transferred ornamental blocks.
            - transactions_list: A list of dictionaries with the details of the transactions performed.
        :rtype: tuple[list[dict[str, Any]], list[dict[str, Any]]]
        :raises InvalidParameterError: If any of the provided transfer data lists are invalid.
        """

        def get_transfered_ornamental_blocks_data_list():
            tobs_data_list = []
            for ob_uid in transfer_uids:
                ob_data = self.get_ornamental_block_data(ob_uid)
                tobs_data_list.append(ob_data)
            return tobs_data_list

        transfer_data_dict = {'ornamental_block_uid_list': ornamental_block_uid_list,
                              'new_owner_uid_list': new_owner_uid_list,
                              'invoice_number_list': invoice_number_list}

        self._verify_dictionary_parameters(transfer_data_dict,
                                           'transfer_ornamental_blocks')
        transfer_uids = transfer_data_dict['ornamental_block_uid_list'].copy()

        transfer_ob_functions = [self.web3_contract_object.functions.transfer_ornamental_block,
                                 self.web3_contract_object.functions.transfer_up_to_5_ornamental_blocks,
                                 self.web3_contract_object.functions.transfer_up_to_20_ornamental_blocks]

        transactions_list = self._make_transaction(sc_functions_list=transfer_ob_functions,
                                                   extract_args_function=self._extract_transfer_ob_args,
                                                   data=transfer_data_dict,
                                                   account=self.account,
                                                   sclink=self.sclink,
                                                   timeout=self.timeout,
                                                   persist=self.persist,
                                                   estimate_cost=estimate_cost)
        transfered_ornamental_blocks_data_list = get_transfered_ornamental_blocks_data_list()
        self._write_output_log(directory=self.log_directory,
                               operation=f"transfer {len(transfered_ornamental_blocks_data_list)} ornamental blocks",
                               output_data=transfered_ornamental_blocks_data_list,
                               transactions_data=transactions_list)
        return transfered_ornamental_blocks_data_list, transactions_list

    @SCLink.connection_checker
    def deactivate_ornamental_blocks(self,
                                     ornamental_block_uid_list: list[ChecksumAddress], *,
                                     estimate_cost: bool = False) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """
        Deactivates ornamental blocks in the smart contract.

        This method deactivates the specified ornamental blocks in the smart contract.
        It supports deactivating multiple blocks in a single transaction and
        can estimate the cost of the transactions if required.

        :param ornamental_block_uid_list: A list of UIDs of the ornamental blocks to be deactivated.
        :type ornamental_block_uid_list: list[ChecksumAddress]
        :param estimate_cost: If True, estimates the cost of the transactions without executing them.
        :type estimate_cost: bool
        :return: A tuple containing two lists:
            - deactivated_ornamental_blocks_data_list: A list of dictionaries with the data of the
            deactivated ornamental blocks.
            - transactions_list: A list of dictionaries with the details of the transactions performed.
        :rtype: tuple[list[dict[str, Any]], list[dict[str, Any]]]
        :raises InvalidParameterError: If any of the provided block UIDs are invalid.
        """

        def get_deactivated_ornamental_blocks_data_list():
            dobs_list = []
            inactive_ob_uids_list = self.get_inactive_ornamental_block_uids_list()[number_of_inactve_ob_before:]
            for index in range(number_of_new_inactive_obs):
                ob_data = self.get_ornamental_block_data(Web3.to_checksum_address(inactive_ob_uids_list[index]))
                dobs_list.append(ob_data)
            return dobs_list

        valid_uid_list = self._verify_list_parameters(ornamental_block_uid_list,
                                                      'deactivate_ornamental_blocks')

        number_of_new_inactive_obs = len(valid_uid_list)
        number_of_inactve_ob_before = len(self.get_inactive_ornamental_block_uids_list())
        deactivate_ob_functions = [self.web3_contract_object.functions.deactivate_ornamental_block,
                                   self.web3_contract_object.functions.deactivate_up_to_5_ornamental_blocks,
                                   self.web3_contract_object.functions.deactivate_up_to_20_ornamental_blocks]

        transactions_list = self._make_transaction(sc_functions_list=deactivate_ob_functions,
                                                   extract_args_function=self._extract_deactivate_ob_args,
                                                   data={'ornamental_block_uid_list': valid_uid_list},
                                                   account=self.account,
                                                   sclink=self.sclink,
                                                   timeout=self.timeout,
                                                   persist=self.persist,
                                                   estimate_cost=estimate_cost)
        deactivated_ornamental_blocks_data_list = get_deactivated_ornamental_blocks_data_list()
        self._write_output_log(directory=self.log_directory,
                               operation=f"deactivate {len(deactivated_ornamental_blocks_data_list)} ornamental blocks",
                               output_data=deactivated_ornamental_blocks_data_list,
                               transactions_data=transactions_list)
        return deactivated_ornamental_blocks_data_list, transactions_list

    @staticmethod
    def _write_output_log(directory: str,
                          operation: str,
                          output_data: list,
                          transactions_data: list) -> None:
        """
        Writes a json log file with information about the operation executed, the transactions made and the output data.

        :param directory: The directory where the log file will be saved.
        :type directory: str
        :param operation: The description of the operation performed on the smart contract.
        :type operation: str
        :param output_data: The data returned in the function output.
        :type output_data: list[dict[str, Any]]
        :param transactions_data: The data on transactions performed with the smart contract.
        :type transactions_data: list[dict[str, Any]]
        """
        log_info = {'operation': operation,
                    'timestamp': output_data[-1]['last_update_timestamp'],
                    'output': output_data,
                    'transactions': transactions_data}
        log_file_name = f"log_{log_info['transactions'][-1]['contract_address']}.json"
        with open(f"{directory}logs/{log_file_name}", 'r', encoding='utf-8') as f:
            log_file = json.load(f)
        log_file.append(log_info)
        with open(f"{directory}logs/{log_file_name}", 'w', encoding='utf-8') as f:
            json.dump(log_file, f, ensure_ascii=False, indent=4)

    def _verify_list_parameters(self, data: list[ChecksumAddress],
                                function_name: str) -> list:
        """
        Verifies the parameters of a list based on the specified function name.

        This method checks the validity of the provided list of data according to the requirements of the
        specified function.
        It ensures that the list contains valid checksum addresses and that the
        ornamental blocks meet the criteria for the given function.

        :param data: The list of data to verify.
        :type data: list[ChecksumAddress]
        :param function_name: The name of the function for which the parameters are being verified.
        :type function_name: str
        :return: A list of valid data after verification.
        :rtype: list
        :raises InvalidParameterError: If the list is empty or contains invalid data.
        :raises TypeError: If the data is not a list of ChecksumAddress.
        :raises NameError: If the function_name is invalid.
        """
        match function_name:
            case 'deactivate_ornamental_blocks':
                if not data:
                    raise InvalidParameterError('Ornamental block uid list is empty')
                if not isinstance(data, list):
                    raise TypeError(f"Wrong data type! Expected: list[ChecksumAddress]")
                valid_data = data.copy()
                for ob_uid in data:
                    remove = False
                    if not Web3.is_checksum_address(ob_uid):
                        print(f"Ornamental block {ob_uid} is invalid")
                        remove = True
                    elif not self.is_ornamental_block(ob_uid):
                        print(f"Ornamental block {ob_uid} not found")
                        remove = True
                    elif not self.is_ornamental_block_active(ob_uid):
                        print(f"Ornamental block {ob_uid} is already inactive")
                        remove = True
                    if remove:
                        print('Item removed from list')
                        valid_data.remove(ob_uid)

                    if not valid_data:
                        raise InvalidParameterError('Ornamental block uid list is empty')
                return valid_data
            case _:
                raise NameError('Invalid function_name')

    def _verify_dictionary_parameters(self,
                                      data: dict[str, list],
                                      function_name: str) -> dict[str, list[str]]:
        """
        Verifies the parameters of a dictionary based on the specified function name.

        This method checks the validity of the provided dictionary of data according to
        the requirements of the specified function.
        It ensures that the dictionary contains valid lists and that the data meets the
        criteria for the given function.

        :param data: The dictionary of data to verify, extracted from the smart contract.
        :type data: dict[str, list]
        :param function_name: The name of the function for which the parameters are being verified.
        :type function_name: str
        :return: A dictionary of valid data after verification.
        :rtype: dict[str, list[str]]
        :raises InvalidParameterError: If the dictionary contains invalid data.
        :raises TypeError: If the data is not a dictionary of lists.
        :raises KeyError: If the dictionary contains incorrect keys.
        :raises NameError: If the function_name is invalid.
        """
        def check_parameters_validity(correct_keys_: list):
            if (not isinstance(data, dict)  # data is not a dictionary
                    or not self._check_type_list(list(lists), list)):  # elements inside lists are not strings
                raise TypeError(
                    f"Wrong data type! Expected: dict[str, list] "
                    f"for the keys: {str(correct_keys_)}, respectively")

            if parameter_keys != correct_keys:  # wrong keys
                raise KeyError(f"Wrong keys in dictionary parameter! Expected: {correct_keys}")

            if set([len(i) for i in lists]) == {0}:  # lists length empty
                raise InvalidParameterError(f"The lists in parameters should not be empty")

            if len(set([len(i) for i in lists])) != 1:  # lists length not equal
                raise InvalidParameterError(f"The lists in parameters should have the same length")

        def check_str_type_values(correct_keys_: list):
            if not all([self._check_type_list(list_, str) for list_ in lists]):
                raise TypeError(
                    f"Wrong data type! Expected: dict[str, list[str] "
                    f"for the keys: {str(correct_keys_)}, respectively")

        def check_nested_dictionary(data_: dict, key_: str, correct_nested_keys: list):
            for nested_index, nested_data in enumerate(data_[key_]):
                remove_ = False
                if not isinstance(nested_data, dict):
                    print(f"Wrong data type for key: {key_}. Expected: \'dict[str, str]\'")
                    remove_ = True
                else:
                    testing_keys = list(nested_data.keys())
                    testing_keys.sort()
                    if testing_keys != correct_nested_keys:
                        print(
                            f"Wrong keys for parameter \'{key_}\' at ornamental block with code: "
                            f"{data_['code_list'][nested_index]}. Expected: {correct_nested_keys}")
                        remove_ = True
                    else:
                        for i, ck in enumerate(correct_nested_keys):
                            if not isinstance(nested_data[ck], str):
                                print(
                                    f"Wrong format value for parameter \'{key_}\', key: \'{ck}\', at "
                                    f"ornamental block with code: {data_['code_list'][nested_index]}. "
                                    f"Expected: \'str\'")
                                remove_ = True
                if remove_:
                    print('Item removed from list')
                    for k in data_.keys():
                        data_[k].pop(nested_index)

        correct_keys = []
        lists = []
        parameter_keys = []
        if isinstance(data, dict):
            lists = data.values()
            parameter_keys = list(data.keys())
            parameter_keys.sort()
        match function_name:
            case 'add_new_users':
                correct_keys = ['user_cnpj_list', 'user_email_address_list', 'user_name_list']
                check_parameters_validity(correct_keys)
                check_str_type_values(correct_keys)

            case 'add_new_ornamental_blocks':
                correct_keys = ['code_list', 'hash_list', 'mining_data_list', 'owners_uid_list', 'properties_list']
                check_parameters_validity(correct_keys)
                check_nested_dictionary(data_=data,
                                        key_='mining_data_list',
                                        correct_nested_keys=['company', 'mining_date', 'mining_site'])
                check_nested_dictionary(data_=data,
                                        key_='properties_list',
                                        correct_nested_keys=['dimensions', 'material', 'weight'])
                data['mining_data_list'] = [json.dumps(value_data) for value_data in data['mining_data_list']]
                data['properties_list'] = [json.dumps(value_data) for value_data in data['properties_list']]
                check_str_type_values(correct_keys)

                for index, owner_uid in enumerate(data['owners_uid_list']):
                    remove = False
                    if (owner_uid == ADDRESS_0
                            or not Web3.is_checksum_address(owner_uid)):
                        print(f"Owner uid {owner_uid} is invalid")
                        remove = True
                    elif not self.is_user(owner_uid):
                        print(f"Owner uid {owner_uid} not found")
                        remove = True

                    if remove:
                        print('Item removed from list')
                        for key in data.keys():
                            data[key].pop(index)

                if not data['owners_uid_list']:
                    raise InvalidParameterError(f"All new ornamental blocks were removed from operation")

            case 'transfer_ornamental_blocks':
                correct_keys = ['invoice_number_list', 'new_owner_uid_list', 'ornamental_block_uid_list']
                check_parameters_validity(correct_keys)
                check_str_type_values(correct_keys)

                for index, ob_uid in enumerate(data['ornamental_block_uid_list']):
                    remove = False
                    if not Web3.is_checksum_address(ob_uid):
                        print(f"Ornamental block uid {ob_uid} is invalid")
                        remove = True
                    elif not Web3.is_checksum_address(data['new_owner_uid_list'][index]):
                        print(f"New owner uid {data['new_owner_uid_list'][index]} is invalid")
                        remove = True
                    elif not self.is_user(data['new_owner_uid_list'][index]):
                        print(f"New owner uid {data['new_owner_uid_list'][index]} not found")
                        remove = True
                    elif not self.is_ornamental_block(ob_uid):
                        print(f"Ornamental block {ob_uid} not found")
                        remove = True
                    elif ob_uid in self.get_inactive_ornamental_block_uids_list():
                        print(f"Ornamental block {ob_uid} is inactive")
                        remove = True

                    if remove:
                        print('Item removed from list')
                        for key in data.keys():
                            data[key].pop(index)

                if not data['invoice_number_list']:
                    raise InvalidParameterError(f"All transfers were removed from operation")
            case _:
                raise NameError('Invalid function_name')

        return data

    @staticmethod
    def _process_user_list(raw_user_list: list) -> list[dict[str, Any]]:
        """
        Processes a raw list of user data extracted from the smart contract into a structured format.

        This method iterates through the provided raw user list and converts each user's data into a dictionary
        with metadata and other user information.

        :param raw_user_list: The raw list of user data to process.
        :type raw_user_list: list
        :return: A list of dictionaries, each containing the processed user data with the following keys:
            - metadata: A dictionary containing the user's metadata with the following keys:
                - uid: The user's unique identifier (UID).
                - list_index: The index of the user in the user list.
                - registration_timestamp: The timestamp of the user's registration.
                - last_update_timestamp: The timestamp of the user's last update.
            - name: The name of the user.
            - cnpj: The CNPJ (Cadastro Nacional da Pessoa Jurídica) of the user's company.
            - email_address: The email address associated with the user.
            - ornamental_blocks_list: A list of ornamental block UIDs associated with the user.
        :rtype: list[dict[str, Any]]
        """
        user_list = []
        for user in raw_user_list:
            user_metadata = {'uid': user[0][0],
                             'list_index': user[0][1],
                             'registration_timestamp': user[0][2],
                             'last_update_timestamp': user[0][3]}
            user_dictionary = {'metadata': user_metadata,
                               'name': user[1],
                               'cnpj': user[2],
                               'email_address': user[3],
                               'ornamental_blocks_list': user[4]}
            user_list.append(user_dictionary)
        return user_list

    @staticmethod
    def _process_ornamental_block_list(raw_ornamental_block_list) -> list[dict[str, Any]]:
        """
        Processes a raw list of ornamental block data extracted from the smart contract into a structured format.

        This method iterates through the provided raw ornamental block list, which is obtained from the smart contract,
        and converts each block's data into a dictionary with metadata and other block information.

        :param raw_ornamental_block_list: The raw list of ornamental block data extracted from the smart contract.
        :type raw_ornamental_block_list: list
        :return: A list of dictionaries, each containing the processed ornamental block data with the following keys:
            - metadata: A dictionary containing the block's metadata with the following keys:
                - uid: The block's unique identifier (UID).
                - list_index: The index of the block in the block list.
                - registration_timestamp: The timestamp of the block's registration.
                - last_update_timestamp: The timestamp of the block's last update.
            - mining_data: A dictionary containing the mining data with the following keys:
                - company: The company responsible for the mining.
                - mining_date: The date when the mining occurred.
                - mining_site: The site where the mining took place.
            - code: The code associated with the ornamental block.
            - properties: A dictionary containing the properties of the block with the following keys:
                - dimensions: The dimensions of the block.
                - material: The material of the block.
                - weight: The weight of the block.
            - hash: The hash of the ornamental block.
            - is_active: The active status of the ornamental block.
            - last_owners: The list of last owners of the ornamental block.
            - invoice_numbers: The list of invoice numbers associated with the ornamental block.
        :rtype: list[dict[str, Any]]
        """
        ornamental_block_list = []
        for ornamental_block in raw_ornamental_block_list:
            ornamental_block_metadata = {'uid': ornamental_block[0][0],
                                         'list_index': ornamental_block[0][1],
                                         'registration_timestamp': ornamental_block[0][2],
                                         'last_update_timestamp': ornamental_block[0][3]}
            ornamental_block_dictionary = {'metadata': ornamental_block_metadata,
                                           'mining_data': json.loads(ornamental_block[1]),
                                           'code': ornamental_block[2],
                                           'properties': json.loads(ornamental_block[3]),
                                           'hash': ornamental_block[4],
                                           'is_active': ornamental_block[5],
                                           'last_owners': ornamental_block[6],
                                           'invoice_numbers': ornamental_block[7]}
            ornamental_block_list.append(ornamental_block_dictionary)
        return ornamental_block_list

    @staticmethod
    def _extract_new_user_args(user_data: dict[str, list], list_length: int) -> dict[str, Any]:
        """
        Extracts arguments for adding new users to the smart contract.

        This method processes the provided user data and prepares the arguments needed for the smart contract
        functions to add new users. It generates user UIDs based on the user data and formats the data
        according to the required structure.

        :param user_data: A dictionary containing lists of user data with the following keys:
            - user_name_list: A list of company names.
            - user_cnpj_list: A list of CNPJ numbers.
            - user_email_address_list: A list of email addresses.
        :type user_data: dict[str, list]
        :param list_length: The number of users to process.
        :type list_length: int
        :return: A dictionary containing the formatted user data with the following keys:
            - user_uid: The UID of the user (if list_length is 1) or a list of UIDs.
            - user_name: The name of the user (if list_length is 1) or a list of names.
            - user_cnpj: The CNPJ of the user (if list_length is 1) or a list of CNPJs.
            - user_email_address: The email address of the user (if list_length is 1) or a list of email addresses.
            - timestamp: The current timestamp.
        :rtype: dict[str, Any]
        """
        sufix = '' if list_length == 1 else '_list'
        user_uid_list = [ADDRESS_0] * list_length
        user_name_list, user_cnpj_list, user_email_address_list = \
            [''] * list_length, [''] * list_length, [''] * list_length
        for i in range(len(user_data.get('user_name_list'))):
            user_name_list[i] = user_data.get('user_name_list').pop(0)
            user_cnpj_list[i] = user_data.get('user_cnpj_list').pop(0)
            user_email_address_list[i] = user_data.get('user_email_address_list').pop(0)
            user_uid_list[i] = Account.from_key(private_key=Web3.keccak(text=(user_name_list[i] +
                                                                              user_cnpj_list[i] +
                                                                              user_email_address_list[i]))).address
        return {f"user_uid{sufix}": user_uid_list.pop(0) if list_length == 1 else user_uid_list,
                f"user_name{sufix}": user_name_list.pop(0) if list_length == 1 else user_name_list,
                f"user_cnpj{sufix}": user_cnpj_list.pop(0) if list_length == 1 else user_cnpj_list,
                f"user_email_address{sufix}": user_email_address_list.pop(0) if list_length == 1
                else user_email_address_list,
                'timestamp': datetime.now().strftime("%Y/%m/%d, %H:%M:%S.%f")}

    @staticmethod
    def _extract_new_ob_args(ornamental_block_data: dict[str, list], list_length: int) -> dict[str, Any]:
        """
        Extracts arguments for adding new ornamental blocks to the smart contract.

        This method processes the provided ornamental block data and prepares the arguments needed for the
        smart contract functions to add new ornamental blocks. It generates ornamental block UIDs based on the
        block data and formats the data according to the required structure.

        :param ornamental_block_data: A dictionary containing lists of ornamental block data with the following keys:
            - mining_data_list: A list of mining data dictionaries, each containing:
                - company: The company responsible for the mining.
                - mining_date: The date when the mining occurred.
                - mining_site: The site where the mining took place.
            - code_list: A list of codes associated with the ornamental blocks.
            - properties_list: A list of properties dictionaries, each containing:
                - dimensions: The dimensions of the ornamental block.
                - material: The material of the ornamental block.
                - weight: The weight of the ornamental block.
            - hash_list: A list of hashes for the ornamental blocks.
            - owners_uid_list: A list of UIDs of the owners of the ornamental blocks.
        :type ornamental_block_data: dict[str, list]
        :param list_length: The number of ornamental blocks to process.
        :type list_length: int
        :return: A dictionary containing the formatted ornamental block data with the following keys:
            - ornamental_block_uid: The UID of the ornamental block (if list_length is 1) or a list of UIDs.
            - mining_data: The mining data of the ornamental block (if list_length is 1) or a list of mining data.
            - code: The code of the ornamental block (if list_length is 1) or a list of codes.
            - properties: The properties of the ornamental block (if list_length is 1) or a list of properties.
            - hash: The hash of the ornamental block (if list_length is 1) or a list of hashes.
            - owners_uid: The UID of the owner of the ornamental block (if list_length is 1) or a list of owner UIDs.
            - timestamp: The current timestamp.
        :rtype: dict[str, Any]
        """
        sufix = '' if list_length == 1 else '_list'
        ornamental_block_uid_list = [ADDRESS_0] * list_length
        ornamental_block_mining_data_list = [''] * list_length
        ornamental_block_code_list = [''] * list_length
        ornamental_block_properties_list = [''] * list_length
        ornamental_block_hash_list = [''] * list_length
        ornamental_block_owners_uid_list = [ADDRESS_0] * list_length
        for i in range(len(ornamental_block_data.get('code_list'))):
            ornamental_block_mining_data_list[i] = ornamental_block_data.get('mining_data_list').pop(0)
            ornamental_block_code_list[i] = ornamental_block_data.get('code_list').pop(0)
            ornamental_block_properties_list[i] = ornamental_block_data.get('properties_list').pop(0)
            ornamental_block_hash_list[i] = ornamental_block_data.get('hash_list').pop(0)
            ornamental_block_owners_uid_list[i] = ornamental_block_data.get('owners_uid_list').pop(0)
            ornamental_block_uid_list[i] = Account.from_key(private_key=Web3.keccak(
                text=(ornamental_block_mining_data_list[i] +
                      ornamental_block_code_list[i] +
                      ornamental_block_properties_list[i] +
                      ornamental_block_hash_list[i]))).address
        return {f"ornamental_block_uid{sufix}": ornamental_block_uid_list.pop(0) if list_length == 1
                else ornamental_block_uid_list,
                f"mining_data{sufix}": ornamental_block_mining_data_list.pop(0) if list_length == 1
                else ornamental_block_mining_data_list,
                f"code{sufix}": ornamental_block_code_list.pop(0) if list_length == 1 else ornamental_block_code_list,
                f"properties{sufix}": ornamental_block_properties_list.pop(
                    0) if list_length == 1 else ornamental_block_properties_list,
                f"hash{sufix}": ornamental_block_hash_list.pop(0) if list_length == 1 else ornamental_block_hash_list,
                f"owners_uid{sufix}": ornamental_block_owners_uid_list.pop(
                    0) if list_length == 1 else ornamental_block_owners_uid_list,
                'timestamp': datetime.now().strftime("%Y/%m/%d, %H:%M:%S.%f")}

    @staticmethod
    def _extract_transfer_ob_args(transfer_data: dict[str, list], list_length: int) -> dict[str, Any]:
        """
        Extracts arguments for transferring ownership of ornamental blocks.

        This method processes the provided transfer data and prepares the arguments needed for the smart contract
        functions to transfer ownership of ornamental blocks. It formats the data according to the required structure.

        :param transfer_data: A dictionary containing lists of transfer data with the following keys:
            - ornamental_block_uid_list: A list of UIDs of the ornamental blocks to be transferred.
            - new_owner_uid_list: A list of UIDs of the new owners.
            - invoice_number_list: A list of invoice numbers associated with the transfers.
        :type transfer_data: dict[str, list]
        :param list_length: The number of transfers to process.
        :type list_length: int
        :return: A dictionary containing the formatted transfer data with the following keys:
            - ornamental_block_uid: The UID of the ornamental block (if list_length is 1) or a list of UIDs.
            - new_owner_uid: The UID of the new owner (if list_length is 1) or a list of UIDs.
            - invoice_number: The invoice number (if list_length is 1) or a list of invoice numbers.
            - timestamp: The current timestamp.
        :rtype: dict[str, Any]
        """
        sufix = '' if list_length == 1 else '_list'
        ornamental_block_uid_list = [ADDRESS_0] * list_length
        new_owner_uid_list = [ADDRESS_0] * list_length
        invoice_number_list = [''] * list_length
        for i in range(len(transfer_data['ornamental_block_uid_list'])):
            ornamental_block_uid_list[i] = transfer_data['ornamental_block_uid_list'][i]
            new_owner_uid_list[i] = transfer_data['new_owner_uid_list'][i]
            invoice_number_list[i] = transfer_data['invoice_number_list'][i]

        return {f"ornamental_block_uid{sufix}": ornamental_block_uid_list.pop(0)
                if list_length == 1 else ornamental_block_uid_list,
                f"new_owner_uid{sufix}": new_owner_uid_list.pop(0)
                if list_length == 1 else new_owner_uid_list,
                f"invoice_number{sufix}": invoice_number_list.pop(0)
                if list_length == 1 else invoice_number_list,
                'timestamp': datetime.now().strftime("%Y/%m/%d, %H:%M:%S.%f")}

    @staticmethod
    def _extract_deactivate_ob_args(ornamental_block_data: dict[str, list], list_length: int) -> dict[str, Any]:
        """
        Extracts arguments for deactivating ornamental blocks.

        This method processes the provided ornamental block data and prepares the arguments needed for the
        smart contract functions to deactivate ornamental blocks.
        It formats the data according to the required structure.

        :param ornamental_block_data: A dictionary containing lists of ornamental block data with the following key:
            - ornamental_block_uid_list: A list of UIDs of the ornamental blocks to be deactivated.
        :type ornamental_block_data: dict[str, list]
        :param list_length: The number of ornamental blocks to process.
        :type list_length: int
        :return: A dictionary containing the formatted ornamental block data with the following key:
            - ornamental_block_uid: The UID of the ornamental block (if list_length is 1) or a list of UIDs.
            - timestamp: The current timestamp.
        :rtype: dict[str, Any]
        """
        sufix = '' if list_length == 1 else '_list'
        ornamental_block_uid_list = [ADDRESS_0] * list_length
        for i in range(len(ornamental_block_data['ornamental_block_uid_list'])):
            ornamental_block_uid_list[i] = ornamental_block_data['ornamental_block_uid_list'][i]
        return {f"ornamental_block_uid{sufix}": ornamental_block_uid_list.pop(0)
                if list_length == 1 else ornamental_block_uid_list,
                'timestamp': datetime.now().strftime("%Y/%m/%d, %H:%M:%S.%f")}

    @staticmethod
    def _check_type_list(list_: list,
                         type_: type) -> bool:
        """
        Checks if all elements in a list are of a specified type.

        This function iterates through the provided list and verifies if each element is an instance of the given type.

        :param list_: The list to check.
        :type list_: list
        :param type_: The expected type of the elements in the list.
        :type type_: type
        :return: True if all elements are of the specified type, False otherwise.
        :rtype: bool
        """
        return all([isinstance(elem, type_) for elem in list_])

    @staticmethod
    def _make_transaction(sc_functions_list: list[web3_contract],
                          extract_args_function: Callable[[dict[str, list], int], dict[str, Any]],
                          data: dict[str, list],
                          account: LocalAccount,
                          sclink: SCLink,
                          timeout: int = 120,
                          persist: int = 0,
                          estimate_cost: bool = False) -> list[dict[str, Any]]:
        """
        Executes transactions on the smart contract.

        This method processes the provided data and executes the necessary transactions on the smart contract.
        It divides the operations into multiple transactions if needed and handles the transaction execution.

        :param sc_functions_list: A list of smart contract functions to be called.
        :type sc_functions_list: list[web3_contract]
        :param extract_args_function: A function to extract the arguments for the smart contract functions.
        :type extract_args_function: Callable[[dict[str, list], int], dict[str, Any]]
        :param data: The dictionary of data to be used in the transactions, extracted from the smart contract.
        :type data: dict[str, list]
        :param account: The account to be used for signing the transactions.
        :type account: LocalAccount
        :param sclink: The SCLink object for interacting with the smart contract.
        :type sclink: SCLink
        :param timeout: The timeout duration for transactions in seconds.
        :type timeout: int
        :param persist: The number of times to retry transactions in case of failure.
        :type persist: int
        :param estimate_cost: If True, estimates and displays the Ether cost for the transaction before executing it.
        :type estimate_cost: bool
        :return: A list of dictionaries containing the details of the executed transactions.
        :rtype: list[dict[str, Any]]
        """
        data_keys = list(data.keys())
        operations_left = len(data.get(data_keys[0]))
        transactions_data = []
        transactions_count = ceil(operations_left / 20)
        print(
            f"The operation will be executed in {transactions_count} "
            f"transaction{'s' if transactions_count > 1 else ''}:")

        for _ in range(transactions_count):
            subset_list = [1, 5, 20]
            subset = {}
            index = 0 if operations_left == 1 else (1 if operations_left <= 5 else 2)
            for key in data_keys:
                subset[key] = data[key][:subset_list[index]]
                data[key] = data[key][subset_list[index]:]
            args = extract_args_function(subset, subset_list[index])
            receipt = sclink.build_and_send_transaction(contract_function=sc_functions_list[index](**args),
                                                        account=account,
                                                        timeout=timeout,
                                                        persist=persist,
                                                        estimate_cost=estimate_cost)
            transactions_data.append(receipt)
            operations_left -= subset_list[index]

        return transactions_data
