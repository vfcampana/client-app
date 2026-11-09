from pytest import raises, fixture
from web3.contract import Contract
from web3.datastructures import AttributeDict
from ..scmanager.sclink import SCLink
from eth_account import Account
from eth_account.datastructures import SignedTransaction
from os import getenv
from .utils import utils
import web3
import json
from pathlib import Path


Path("/scm_config/tests").mkdir(parents=True, exist_ok=True)
CONFIG_FILE_NAME = 'basic_contract_test_config.json'
CLASS_NAME = 'TestSCLnk'

with open(f"scm_config/tests/{CONFIG_FILE_NAME}", 'r', encoding='utf-8') as file:
    config_data = json.load(file)
w3 = web3.Web3(web3.Web3.HTTPProvider(endpoint_uri=getenv(config_data['endpoint_environment_key'])))
config_data['transaction_count'] = w3.eth.get_transaction_count(config_data['deployer'])
config_data['last_balance'] = w3.eth.get_balance(config_data['deployer'])
sclink = SCLink(endpoint=getenv(config_data['endpoint_environment_key']))
account_test = Account.from_key(private_key=str(getenv(config_data['private_environment_key'])))
shared_data = {}

utils.calc_cost(None, previous=True, test='all')


@fixture(autouse=True, scope='session')
def setup_teardown():

    yield sclink, config_data, account_test

    contract = sclink.get_contract(contract_address=config_data['contract']['address'],
                                   abi=config_data['contract']['abi'])
    if contract.functions.get_status().call():  # pragma: no cover
        config_data['last_balance'] = sclink.get_balance(config_data['deployer'])
        config_data['transaction_count'] = sclink.get_transaction_count(config_data['deployer'])
        contract_function = contract.functions.set_status(False)
        gas_price = sclink.get_gas_price()
        nonce = sclink.get_transaction_count(account_test.address)
        unsigned_tx = contract_function.build_transaction(
            transaction={'from': account_test.address,
                         'nonce': nonce,
                         'gasPrice': round(gas_price * 10 ** 18),
                         'gas': 1000000000})
        gas = sclink.estimate_gas(unsigned_tx)
        unsigned_tx.update({'gas': gas})
        signed_tx = sclink.sign_transaction(transaction=unsigned_tx,
                                            account_private_key=account_test.key)
        sclink.send_transaction(transaction=signed_tx.rawTransaction,
                                timeout=300)

    new_last_balance = sclink.get_balance(config_data['deployer'])
    new_transaction_count = sclink.get_transaction_count(config_data['deployer'])

    config_data['last_balance'] = new_last_balance
    config_data['transaction_count'] = new_transaction_count
    with open(f"scm_config/tests/{CONFIG_FILE_NAME}", 'w', encoding='utf-8') as file:
        json.dump(config_data, file, ensure_ascii=False, indent=4)

    # utils.calc_cost(None)


class TestSCLnk:
    account_test = None
    sclink = None

    @utils.print_class_test_name(__file__)
    def test_01_of_11_init(self):
        assert sclink.endpoint == getenv(config_data['endpoint_environment_key'])
        assert isinstance(sclink.web3, web3.Web3)

    def test_02_of_11_is_connected(self):
        assert sclink.is_connected()

    def test_03_of_11_get_contract(self):
        contract = sclink.get_contract(contract_address=config_data['contract']['address'],
                                       abi=config_data['contract']['abi'])
        assert isinstance(contract, Contract)
        assert contract.address == config_data['contract']['address']
        assert contract.abi == json.loads(config_data['contract']['abi'])
        assert not contract.functions.get_status().call()

    def test_04_of_11_get_transaction_count(self):
        tx_count = w3.eth.get_transaction_count(config_data['deployer'])
        assert sclink.get_transaction_count(config_data['deployer']) == tx_count
        config_data['transaction_count'] = tx_count

    def test_05_of_11_get_balance(self):
        account_balance = w3.eth.get_balance(account_test.address) * 10 ** (-18)
        assert sclink.get_balance(config_data['deployer']) == account_balance
        config_data['last_balance'] = account_balance

    def test_06_of_11_get_gas_price(self):
        assert isinstance(sclink.get_gas_price(), float)

    def test_07_of_11_sign_transaction(self):
        contract = sclink.get_contract(contract_address=config_data['contract']['address'],
                                       abi=config_data['contract']['abi'])
        config_data['last_balance'] = sclink.get_balance(config_data['deployer'])
        config_data['transaction_count'] = sclink.get_transaction_count(config_data['deployer'])
        contract_function = contract.functions.set_status(True)
        cost = sclink.estimate_transaction_cost(contract_function=contract_function,
                                                account_address=account_test.address)

        assert 0 < cost < 0.02

        gas_price = sclink.get_gas_price()
        nonce = sclink.get_transaction_count(account_test.address)
        unsigned_tx = contract_function.build_transaction(
            transaction={'from': account_test.address,
                         'nonce': nonce,
                         'gasPrice': round(gas_price * 10 ** 18),
                         'gas': 1000000000})
        gas = sclink.estimate_gas(unsigned_tx)
        unsigned_tx.update({'gas': gas})
        signed_tx = sclink.sign_transaction(transaction=unsigned_tx,
                                            account_private_key=account_test.key)

        assert isinstance(signed_tx, SignedTransaction)

        shared_data['contract'] = contract
        shared_data['signed_tx'] = signed_tx

    def test_08_of_11_send_transaction(self):
        tx_receipt = sclink.send_transaction(transaction=shared_data['signed_tx'].rawTransaction,
                                             timeout=300)

        assert isinstance(tx_receipt, AttributeDict)

        shared_data['tx_receipt'] = tx_receipt

    @SCLink.connection_checker
    def foo(self):
        return True

    def test_09_of_11_connection_checker(self):
        self.sclink = sclink
        try:
            assert self.foo()
        except ConnectionError:  # pragma: no cover
            assert False

    @utils.enclosure_prints(file=__file__, class_name=CLASS_NAME)
    def test_10_of_11_build_and_send_transaction_interrupted(self):
        contract_function = shared_data['contract'].functions.set_status(False)
        with raises(KeyboardInterrupt):
            tx_data = utils.ignore_requests(function=sclink.build_and_send_transaction,
                                            kwargs={'contract_function': contract_function,
                                                    'account': account_test,
                                                    'timeout': 300,
                                                    'estimate_cost': True},
                                            ignore=True,
                                            key='1')

    @utils.enclosure_prints(file=__file__, class_name=CLASS_NAME)
    def test_11_of_11_build_and_send_transaction(self):
        contract_function = shared_data['contract'].functions.set_status(False)
        tx_data = utils.ignore_requests(function=sclink.build_and_send_transaction,
                                        kwargs={'contract_function': contract_function,
                                                'account': account_test,
                                                'timeout': 300,
                                                'persist': 3,
                                                'estimate_cost': True},
                                        ignore=True)
        testing_keys = ['block_hash', 'block_number', 'contract_address', 'cost_eth', 'cost_gwei',
                        'duration', 'effective_gas_price', 'from', 'function', 'gas_used', 'hash',
                        'index', 'link']
        tx_keys = list(tx_data.keys())
        tx_keys.sort()
        assert tx_keys == testing_keys
        assert tx_data['contract_address'] == shared_data['contract'].address
        assert tx_data['from'] == account_test.address
