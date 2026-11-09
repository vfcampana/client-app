"""
sclink
======

This module provides the SCLink class, which is used to represent a connection to the Ethereum blockchain. The class
includes methods for interacting with the blockchain, such as retrieving contract information, estimating transaction
costs, and sending transactions.

Imports
-------

- from eth_account.signers.local import LocalAccount
- from eth_account.datastructures import SignedTransaction
- from eth_typing import ChecksumAddress, HexStr
- from functools import wraps
- from hexbytes import HexBytes
- import logging
- import time
- from typing import Any, Union
- from web3 import Web3, contract as web3_contract
- from web3.exceptions import TimeExhausted
- from web3.types import ABI

Classes
-------

1. SCLink:
    A class used to represent a Blockchain connection.

    Methods
    -------
    - __init__(endpoint: str)
        Constructs all the necessary attributes for the Blockchain object.
    - build_and_send_transaction(function: web3_contract, account: LocalAccount, timeout: int = 120, persist: int = 0,
    estimate_cost: bool = False) -> dict[str, Any] | None
        Sends a transaction to the blockchain.
    - connect(endpoint: str, timeout: int = 20) -> Web3
        Connects to the blockchain node and initializes the Web3 instance.
    - connection_checker(func: function) -> function
        A decorator that checks the blockchain connection before executing a function.
    - is_connected() -> bool
        Checks if the connection to the blockchain node is active.
    - get_contract(address: ChecksumAddress, abi: ABI) -> web3_contract.Contract
        Retrieves a smart contract instance.
    - get_balance(account_address: ChecksumAddress) -> float
        Retrieves the balance of an account in Ether.
    - get_transaction_count(account_address: ChecksumAddress) -> int
        Retrieves the number of transactions sent from an account.
    - get_gas_price() -> float
        Retrieves the current gas price in Ether.
    - estimate_gas(transaction: Any) -> int
        Estimates the gas required for a transaction.
    - estimate_cost_eth(function: web3_contract, account_address: ChecksumAddress) -> float
        Estimates the cost of a transaction in Ether.
    - sign_transaction(transaction: dict[str, Any], private_key: Any) -> SignedTransaction
        Signs a transaction with a private key.
    - send_transaction(transaction: Union[HexStr, bytes], timeout: int = 120) -> TxReceipt
        Sends a signed transaction to the blockchain.

Usage
-----

To use this module, import the SCLink class and create an instance with the appropriate endpoint. For example:

    from sclink import SCLink

    # Create an instance of SCLink:
    sclink = SCLink(endpoint='https://example.com')

    # Check if connected:
    if sclink.is_connected():
        print("Connected to the blockchain")

    # Get the balance of an account:
    balance = sclink.get_balance(account_address='0xYourAccountAddress')
    print(f"Account balance: {balance} Ether")

This module simplifies the process of interacting with the Ethereum blockchain, providing a streamlined interface for
common tasks.

Dependencies
------------

- eth_account: Manages Ethereum accounts and signing transactions.
- eth_typing: Provides type hints for Ethereum-related data types.
- functools: Provides higher-order functions and operations on callable objects.
- hexbytes: Handles hexadecimal byte data.
- logging: Provides a flexible framework for emitting log messages from Python programs.
- time: Provides various time-related functions.
- typing: Provides type hints for function signatures.
- web3: Interacts with the Ethereum blockchain.

"""

from eth_account.signers.local import LocalAccount
from eth_account.datastructures import SignedTransaction
from eth_typing import ChecksumAddress, HexStr
from functools import wraps
from hexbytes import HexBytes
import logging
import time
from typing import Any, Union
from web3 import Web3, contract as web3_contract
from web3.exceptions import TimeExhausted
from web3.types import ABI


class SCLink:
    """
    A class used to represent a Blockchain connection.

    This class provides methods to interact with the Ethereum blockchain, including connecting to a node, retrieving
    contract information, estimating transaction costs, and sending transactions.

    Attributes
    ----------
    endpoint : str
        The endpoint URL of the blockchain node.
    web3 : Web3
        The Web3 instance for interacting with the Ethereum blockchain.

    Methods
    -------
    __init__(endpoint: str)
        Constructs all the necessary attributes for the Blockchain object.
    connect(endpoint: str, timeout: int = 20) -> Web3
        Connects to the blockchain node and initializes the Web3 instance.
    connection_checker(func: function) -> function
        A decorator that checks the blockchain connection before executing a function.
    is_connected() -> bool
        Checks if the connection to the blockchain node is active.
    get_contract(address: ChecksumAddress, abi: ABI) -> web3_contract.Contract
        Retrieves a smart contract instance.
    get_balance(account_address: ChecksumAddress) -> int
        Retrieves the balance of an account.
    get_transaction_count(account_address: ChecksumAddress) -> int
        Retrieves the number of transactions sent from an account.
    get_gas_price() -> int
        Retrieves the current gas price.
    estimate_gas(transaction: Any) -> int
        Estimates the gas required for a transaction.
    estimate_cost_eth(function: web3_contract, account_address: ChecksumAddress) -> float
        Estimates the cost of a transaction in Ether.
    sign_transaction(transaction: dict[str, Any], private_key: Any) -> SignedTransaction
        Signs a transaction with a private key.
    send_transaction(transaction: Union[HexStr, bytes], timeout: int = 120) -> TxReceipt
        Sends a signed transaction to the blockchain.
    build_and_send_transaction(function: web3_contract, account: LocalAccount, timeout: int = 120, persist: int = 0,
    estimate_cost: bool = False) -> dict[str, Any] | None
        Sends a transaction to the blockchain.
    """

    def __init__(self,
                 endpoint: str):
        """
        Constructs all the necessary attributes for the SCLink object.

        :param endpoint: The endpoint URL of the blockchain node.
        :type endpoint: str
        :return: The SCLink instance.
        :rtype: SCLink
        """
        self.endpoint = endpoint
        self.web3 = self.connect(endpoint)

    def is_connected(self) -> bool:
        """
        Checks if the connection to the blockchain node is active.

        :return: True if connected, False otherwise.
        :rtype: bool
        """
        return self.web3.is_connected()

    def get_contract(self,
                     contract_address: ChecksumAddress,
                     abi: ABI) -> web3_contract.Contract:
        """
        Retrieves a smart contract instance.

        :param contract_address: The address of the smart contract.
        :type contract_address: ChecksumAddress
        :param abi: The ABI (Application Binary Interface) of the smart contract.
        :type abi: ABI
        :return: The smart contract instance.
        :rtype: web3_contract.Contract
        """
        return self.web3.eth.contract(address=contract_address,
                                      abi=abi)

    def get_balance(self,
                    account_address: ChecksumAddress) -> float:
        """
        Retrieves the balance of an account in Ether.

        :param account_address: The address of the account.
        :type account_address: ChecksumAddress
        :return: The balance of the account in Ether.
        :rtype: int
        """
        return self.web3.eth.get_balance(account_address) * 10 ** (-18)

    def get_transaction_count(self,
                              account_address: ChecksumAddress) -> int:
        """
        Retrieves the number of transactions sent from an account.

        :param account_address: The address of the account.
        :type account_address: ChecksumAddress
        :return: The number of transactions sent from the account.
        :rtype: int
        """
        return self.web3.eth.get_transaction_count(account_address)

    def get_gas_price(self) -> float:
        """
        Retrieves the current gas price in Ether.

        :return: The current gas price in Ether.
        :rtype: int
        """
        return self.web3.eth.gas_price * 10 ** (-18)

    def estimate_gas(self,
                     transaction: Any) -> int:
        """
        Estimates the gas required for a transaction.

        :param transaction: The transaction for which to estimate gas.
        :type transaction: Any
        :return: The estimated gas required for the transaction.
        :rtype: int
        """
        return self.web3.eth.estimate_gas(transaction)

    def estimate_transaction_cost(self,
                                  contract_function: web3_contract,
                                  account_address: ChecksumAddress) -> float:
        """
        Estimates the cost of a transaction in Ether.

        This method calculates the estimated gas cost in Ether for executing a given smart contract function.

        :param contract_function: The smart contract function to estimate the cost for.
        :type contract_function: web3_contract
        :param account_address: The address of the account initiating the transaction.
        :type account_address: ChecksumAddress
        :return: The estimated cost of the transaction in Ether.
        :rtype: float
        """
        gas_price = self.get_gas_price()
        nonce = self.get_transaction_count(account_address)
        tx = contract_function.build_transaction(
            transaction={'from': account_address,
                         'nonce': nonce,
                         'gasPrice': round(gas_price * 10 ** 18),
                         'gas': 1000000000})
        gas = self.estimate_gas(tx)
        return gas * gas_price

    def sign_transaction(self,
                         transaction: dict[str, Any],
                         account_private_key: Any) -> SignedTransaction:
        """
        Signs a transaction with a private key.

        This method signs a given transaction using the provided private key.

        :param transaction: The transaction to be signed.
        :type transaction: dict[str, Any]
        :param account_private_key: The account private key to sign the transaction with.
        :type account_private_key: Any
        :return: The signed transaction.
        :rtype: SignedTransaction
        """
        return self.web3.eth.account.sign_transaction(transaction_dict=transaction,
                                                      private_key=account_private_key)

    def send_transaction(self,
                         transaction: Union[HexStr, bytes],
                         timeout: int = 120) -> HexBytes:
        """
        Sends a signed transaction to the blockchain.

        This method sends a raw signed transaction to the blockchain network and returns the transaction receipt.

        :param transaction: The signed transaction to be sent.
        :type transaction: Union[HexStr, bytes]
        :param timeout: The maximum time to wait for the transaction receipt, in seconds.
        :type timeout: int
        :return: The transaction receipt.
        :rtype: TxReceipt
        """
        transaction_hash = self.web3.eth.send_raw_transaction(transaction=transaction)
        return self.web3.eth.wait_for_transaction_receipt(transaction_hash=transaction_hash,
                                                          timeout=timeout)

    def build_and_send_transaction(self,
                                   contract_function: web3_contract,
                                   account: LocalAccount,
                                   timeout: int = 120,
                                   persist: int = 0,
                                   estimate_cost: bool = False) -> dict[str, Any] | None:
        """
        Sends a transaction to the blockchain.

        This method builds, signs, and sends a transaction to the blockchain.
        It also estimates the transaction cost if requested.

        :param contract_function: The function to call on the contract.
        :type contract_function: web3_contract
        :param account: The account from which the transaction will be sent.
        :type account: LocalAccount
        :param timeout: The timeout duration for the transaction in seconds.
        :type timeout: int
        :param persist: The number of times to retry the transaction in case of failure.
        :type persist: int
        :param estimate_cost: If True, estimates and displays the Ether cost for the transaction before executing it.
        :type estimate_cost: bool
        :return: A dictionary containing the receipt of the transaction.
        :rtype: dict[str, Any] | None
        """

        def build_transaction():
            params_ = {}
            try:
                params_['function_identifier'] = contract_function.function_identifier
                params_['contract_address'] = contract_function.address
            except AttributeError:  # pragma: no cover
                params_['function_identifier'] = 'contract_deploy'
                params_['contract_address'] = ''
            print(f"Building transaction {params_['function_identifier']}...")
            params_['gas_price'] = round(self.get_gas_price() * 10 ** 18)
            params_['nonce'] = self.get_transaction_count(account.address)
            params_['unsigned_tx'] = contract_function.build_transaction(
                transaction={'from': account.address,
                             'nonce': params_['nonce'],
                             'gasPrice': params_['gas_price'],
                             'gas': 1000000000})
            params_['gas'] = self.estimate_gas(params_['unsigned_tx'])
            return params_

        def verify_transaction_cost(params_):
            cost = params_['gas'] * params_['gas_price'] * 10 ** -18
            print(f"\tEstimated transaction cost: {cost:.6f} Eth.")
            if input('\t\tPress ENTER to send the transaction: '):  # pragma: no cover
                raise KeyboardInterrupt('Transaction interrupted by user')

        def send_transaction(params_):
            start_timer = time.time()
            params_['unsigned_tx'].update({'gas': params_['gas']})
            signed_tx = self.sign_transaction(
                transaction=params_['unsigned_tx'],
                account_private_key=account.key)
            print(f"\tSending transaction nº {params_['nonce']}...")
            receipt_ = self.send_transaction(
                transaction=signed_tx.rawTransaction,
                timeout=timeout)
            elapsed_time_ = round(time.time() - start_timer, 3)
            return receipt_, elapsed_time_

        def get_transaction_data(receipt_, params_, elapsed_time_):
            if receipt_['contractAddress']:  # pragma: no cover
                params_['contract_address'] = receipt_['contractAddress']
            transaction_data = {'contract_address': params_['contract_address'],
                                'from': receipt_['from'],
                                'function': params_['function_identifier'],
                                'cost_gwei': receipt_['effectiveGasPrice'] * receipt_['gasUsed'] * 10 ** (-9),
                                'cost_eth': receipt_['effectiveGasPrice'] * receipt_['gasUsed'] * 10 ** (-18),
                                'duration': elapsed_time_,
                                'index': receipt_['transactionIndex'],
                                'gas_used': receipt_['gasUsed'],
                                'effective_gas_price': receipt_['effectiveGasPrice'],
                                'hash': receipt_['transactionHash'].hex(),
                                'block_hash': receipt_['blockHash'].hex(),
                                'block_number': receipt_['blockNumber'],
                                'link': f"https://sepolia.etherscan.io/tx/{receipt_['transactionHash'].hex()}"}
            print(f"\tTransaction {params_['function_identifier']} sent successfully in {elapsed_time_:.3f} s! "
                  f"Cost: {transaction_data['cost_eth']:.6f} Eth.")
            return transaction_data

        receipt = {}
        params = {}
        elapsed_time = 0.0
        if persist != 0:
            timeout = 300
        for i in range(persist + 1):
            if i == persist:  # pragma: no cover
                params = build_transaction()
                if estimate_cost:
                    verify_transaction_cost(params)
                receipt, elapsed_time = send_transaction(params)
                break
            try:
                params = build_transaction()
                if estimate_cost:
                    verify_transaction_cost(params)
                receipt, elapsed_time = send_transaction(params)
                break
            except TimeExhausted:  # pragma: no cover
                print(f"\t\tTransaction timed out! Resending... (Attempt {i + 2} of {persist + 1})")

        return get_transaction_data(receipt, params, elapsed_time)

    @staticmethod
    def connect(endpoint: str,
                timeout: int = 20) -> Web3:
        """
        Connects to the blockchain node and initializes the Web3 instance.

        This method establishes a connection to the blockchain node using the provided endpoint URL.

        :param endpoint: The endpoint URL of the blockchain node.
        :type endpoint: str
        :param timeout: The timeout duration for the connection in seconds.
        :type timeout: int
        :return: The Web3 instance for interacting with the blockchain.
        :rtype: Web3
        :raises ConnectionError: If the connection to the blockchain node fails.
        """
        web3_link = Web3(Web3.HTTPProvider(
            endpoint_uri=endpoint,
            request_kwargs={'timeout': timeout}))
        if not web3_link.is_connected():  # pragma: no cover
            raise ConnectionError('Connection failed: Check your internet connection.')
        return web3_link

    @staticmethod
    def connection_checker(func):
        """
        A decorator that checks the blockchain connection before executing a function.

        This decorator ensures that the blockchain connection is active before calling the decorated function.

        :param func: The function to be decorated.
        :type func: function
        :return: The decorated function.
        :rtype: function
        """

        @wraps(func)
        def wrapper(self,
                    *args,
                    **kwargs):
            if not self.sclink.is_connected():  # pragma: no cover
                logging.warning('Connection lost. Trying to reconnect...')
                self.sclink.connect(endpoint=self.sclink.endpoint,
                                    timeout=self.timeout)
            return func(self, *args, **kwargs)

        return wrapper
