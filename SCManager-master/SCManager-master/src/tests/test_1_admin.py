from pytest import raises, fixture
from ..scmanager.admin_tools import admin_tools as adm
from ..scmanager.sclink import SCLink
from .utils import utils
from web3._utils.datatypes import PropertyCheckingFactory as Contract
from web3 import Web3
from dotenv import load_dotenv
from eth_account import Account
import json
from os import listdir, remove, getenv

ENDPOINT_ENV_KEY = 'ETHEREUM_ENDPOINT'
PRIVATE_ENVIRONMENT_KEY = 'ETHEREUM_PRIVATE_KEY_TEST'
SOLIDITY_FILE = 'smart_contract.sol'
CONFIG_FILE_NAME = 'testing_config.json'

IGNORE_REQUESTS = True
CLASS_NAME = 'TestAdmin'
load_dotenv(override=True)


@fixture(autouse=True, scope='session')
def setup_teardown():

    yield

    # utils.calc_cost(None)


class TestAdmin:
    @utils.print_class_test_name(__file__)
    def test_01_of_03_create_config_file(self):
        if CONFIG_FILE_NAME in listdir('scm_config/tests'):  # pragma: no cover
            remove(f"scm_config/tests/{CONFIG_FILE_NAME}")
        adm.create_config_file(endpoint_environment_key=ENDPOINT_ENV_KEY,
                               private_environment_key=PRIVATE_ENVIRONMENT_KEY,
                               file_name=f"tests/{CONFIG_FILE_NAME}",
                               deploy=False)

        assert CONFIG_FILE_NAME in listdir('scm_config/tests')

        with open(f"scm_config/tests/{CONFIG_FILE_NAME}", 'r', encoding='utf-8') as file:
            json_dict = json.load(file)

        assert json_dict['contract'] == {}
        assert json_dict['deployer'] == ''
        assert json_dict['endpoint_environment_key'] == ENDPOINT_ENV_KEY
        assert json_dict['private_environment_key'] == PRIVATE_ENVIRONMENT_KEY

    def test_02_of_03_extract_code(self):
        with open(f"scm_config/tests/{CONFIG_FILE_NAME}", 'r', encoding='utf-8') as file:
            json_dict = json.load(file)
        sclink = SCLink(
            endpoint=getenv(json_dict['endpoint_environment_key']))
        contract, contract_info = adm._extract_code(sclink=sclink,
                                                    path_to_solidity_file=f"scm_config/{SOLIDITY_FILE}")

        assert isinstance(contract, type(Contract))
        for key in ['abi', 'address', 'bin', 'code', 'description', 'version']:
            assert key in contract_info.keys()
        assert contract_info['address'] == ''
        assert isinstance(json.loads(contract_info['abi']), list)

    @utils.enclosure_prints(file=__file__, class_name=CLASS_NAME)
    def test_03_of_03_deploy_sc(self):
        assert CONFIG_FILE_NAME in listdir('scm_config/tests')

        config_data = utils.ignore_requests(function=adm.deploy_smart_contract,
                                            kwargs={'config_file': f"tests/{CONFIG_FILE_NAME}",
                                                    'timeout': 300,
                                                    'persist': 3},
                                            ignore=IGNORE_REQUESTS)
        with open(f"scm_config/tests/{CONFIG_FILE_NAME}", 'r', encoding='utf-8') as file:
            config_data_from_file = json.load(file)

        assert config_data_from_file == config_data

        deployer_address = Account.from_key(private_key=str(getenv(config_data['private_environment_key']))).address

        assert Web3.is_checksum_address(config_data['contract']['address'])
        assert config_data['deployer'] == deployer_address
