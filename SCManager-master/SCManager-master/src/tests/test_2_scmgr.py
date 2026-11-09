from datetime import datetime
from pytest import raises, fixture
from web3.contract import Contract
from web3 import Web3
from ..scmanager.scmanager import SCManager
from ..scmanager.sclink import SCLink
from ..scmanager import admin_tools
from ..scmanager.exceptions import InvalidParameterError
from eth_account import Account
from os import getenv, listdir
from .utils import utils
import json

ADDRESS_0 = Web3.to_checksum_address('0x' + '0' * 40)
CONFIG_FILE_NAME = 'tests/testing_config'
CLASS_NAME = 'TestSCMgr'
IGNORE_REQUESTS = True
TIMEOUT = 300
PERSIST = 3


# utils.calc_cost(None, previous=True, test='test_scmanager')


def deploy_new_testing_contract(endpoint_env_key: str, private_enviroment_key: str):  # pragma: no cover
    admin_tools.create_config_file(endpoint_env_key,
                                   private_enviroment_key,
                                   file_name=CONFIG_FILE_NAME)
    admin_tools.deploy_smart_contract(config_file=CONFIG_FILE_NAME,
                                      timeout=TIMEOUT)


def setup_testing_contract():
    if f"{CONFIG_FILE_NAME.split('/')[-1]}.json" not in listdir('scm_config/tests'):  # pragma: no cover
        raise FileNotFoundError(
            f'Arquivo \"scm_config/{CONFIG_FILE_NAME}.json\" de configuração para testes não encontrado')
    with open(f"scm_config/{CONFIG_FILE_NAME}.json", 'r', encoding='utf-8') as file:
        config_data = json.load(file)
    if config_data['deployer']:
        sclink_ = SCLink(endpoint=getenv(config_data['endpoint_environment_key']))
        account_test_ = Account.from_key(private_key=str(getenv(config_data['private_environment_key'])))
        contract_obj_ = sclink_.get_contract(contract_address=config_data['contract']['address'],
                                             abi=json.loads(config_data['contract']['abi']))
        inicial_contract_data = [[config_data['contract']['address']],
                                 ['0x0000000000000000000000000000000000000000'],
                                 [(('0x0000000000000000000000000000000000000000', 0, '', ''),
                                   '', '', '', [])], [], []]

    if (not config_data['deployer'] or
            not contract_obj_.functions.get_contract_data().call() == inicial_contract_data):  # pragma: no cover
        utils.ignore_requests(function=deploy_new_testing_contract,
                              kwargs={'endpoint_env_key': config_data['endpoint_environment_key'],
                                      'private_enviroment_key': config_data['private_environment_key']},
                              ignore=IGNORE_REQUESTS)
        return setup_testing_contract()
    return contract_obj_, account_test_, sclink_  # pragma: no cover


def new(type_: str, index: int):
    block_dict = {}
    if type_ == 'user':
        block_dict = {'cnpj': f"testing_cnpj_{index}",
                      'company_name': f"testing_username_{index}",
                      'email_address': f"testing_email_{index}",
                      'last_update_timestamp': '',
                      'list_index': index + 1,
                      'ornamental_blocks_list': [],
                      'registration_timestamp': '',
                      'uid': Account.from_key(private_key=Web3.keccak(
                          text=f"testing_username_{index}" + f"testing_cnpj_{index}"
                               + f"testing_email_{index}")).address}
    elif type_ == 'block':
        block_dict = {'code': f"testing_code_{index}",
                      'hash': f"testing_hash_{index}",
                      'invoice_numbers': [],
                      'is_active': True,
                      'last_owners': [],
                      'last_update_timestamp': '',
                      'list_index': index,
                      'mining_data': {'company': f"testing_company_{index}",
                                      'mining_date': f"testing_mining_date_{index}",
                                      'mining_site': f"testing_mining_site_{index}"},
                      'properties': {'dimensions': f"testing_dimensions_{index}",
                                     'material': f"testing_material_{index}",
                                     'weight': f"testing_weight_{index}"},
                      'registration_timestamp': '',
                      'uid': ''}
        block_dict['uid'] = Account.from_key(private_key=Web3.keccak(text=(json.dumps(block_dict['mining_data']) +
                                                                           block_dict['code'] +
                                                                           json.dumps(block_dict['properties']) +
                                                                           block_dict['hash']))).address
    return block_dict


def get_new_raw(type_: str, data: list[dict]):
    raw_data = {}
    if type_ == 'user':
        raw_data = {'user_cnpj_list': [],
                    'user_name_list': [],
                    'user_email_address_list': []}
        for d in data:
            raw_data['user_cnpj_list'].append(d['cnpj'])
            raw_data['user_name_list'].append(d['company_name'])
            raw_data['user_email_address_list'].append(d['email_address'])
    if type_ == 'block':
        raw_data = {'mining_data_list': [],
                    'code_list': [],
                    'properties_list': [],
                    'hash_list': [],
                    'owners_uid_list': []}
        for d in data:
            raw_data['mining_data_list'].append(d['mining_data'])
            raw_data['code_list'].append(d['code'])
            raw_data['properties_list'].append(d['properties'])
            raw_data['hash_list'].append(d['hash'])
            raw_data['owners_uid_list'].append(d['last_owners'])
    return raw_data


contract_obj, account, sclink = setup_testing_contract()
shared_data = {
    'users': [],  # [new('user', i) for i in range(10)],
    'blocks': [],  # [new('block', i) for i in range(9)],
    'inactive_blocks': []}
# contract_data = contract_obj.functions.get_contract_data().call()
scmgr = SCManager(config_file=f"{CONFIG_FILE_NAME}.json",
                  timeout=TIMEOUT,
                  persist=PERSIST)


@fixture(autouse=True, scope='session')
def setup_teardown():
    yield

    print()
    utils.calc_cost(None)


def get_repr():
    data = contract_obj.functions.get_contract_data().call()
    bin_ = contract_obj.functions.get_user_data(ADDRESS_0).call()[7]
    users_list = SCManager._process_user_list(data[2])[1:]
    ob_list = SCManager._process_ornamental_block_list(data[4])
    text = f"Contract {data[0][-1]} conected:\n"
    text += (f"\t{len(users_list)} user(s) and {len(data[3]) - len(bin_)} "
             f"active ornamental block(s) found:\n")

    for user in users_list:
        uid = user['metadata']['uid']
        text += (f"\t\tUser {user['metadata']['list_index']: >2} - uid {uid} "
                 f"with {len(user['ornamental_blocks_list'])} ornamental block(s):\n")

        for block_uid in user['ornamental_blocks_list']:
            index = data[3].index(block_uid)
            block = ob_list[index]
            text += f"\t\t\tBlock {block['metadata']['list_index']: >3} - uid {block_uid}\n"

    text += f"\tDump list ({len(bin_)} inactive block(s)):\n"
    for block_uid in bin_:
        index = data[3].index(block_uid)
        block = ob_list[index]
        text += f"\t\tBlock {block['metadata']['list_index']: >3} - uid {block_uid}\n"
    return text


class TestSCMgr:
    @utils.print_class_test_name(__file__)
    def test_01_of_61_init(self):
        assert scmgr.sclink.endpoint == sclink.endpoint
        assert scmgr.account == account
        assert isinstance(scmgr.web3_contract_object, Contract)

    def test_02_of_61_check_type_list_false(self):
        assert not SCManager._check_type_list(list_=[0, 1, 'a'],
                                              type_=int)

    def test_03_of_61_check_type_list_true(self):
        assert SCManager._check_type_list(list_=[0, 1, 2],
                                          type_=int)

    def test_04_of_61_verify_list_parameters_invalid_function_name(self):
        with raises(NameError):
            assert scmgr._verify_list_parameters(data=[],
                                                 function_name='a')

    def test_05_of_61_verify_list_parameters_empty_data(self):
        with raises(InvalidParameterError):
            assert scmgr._verify_list_parameters(data=[],
                                                 function_name='deactivate_ornamental_blocks')

    @utils.enclosure_prints(file=__file__, class_name=CLASS_NAME)
    def test_06_of_61_verify_list_parameters_data_wrong_type(self):
        with raises(TypeError):
            assert scmgr._verify_list_parameters(data=1,
                                                 function_name='deactivate_ornamental_blocks')

    @utils.enclosure_prints(file=__file__, class_name=CLASS_NAME)
    def test_07_of_61_verify_list_parameters_list_data_wrong_type(self):
        with raises(InvalidParameterError):
            assert scmgr._verify_list_parameters(data=['a'],
                                                 function_name='deactivate_ornamental_blocks')

    @utils.enclosure_prints(file=__file__, class_name=CLASS_NAME)
    def test_08_of_61_verify_list_parameters_list_data_not_block(self):
        with raises(InvalidParameterError):
            assert scmgr._verify_list_parameters(data=[ADDRESS_0],
                                                 function_name='deactivate_ornamental_blocks')

    def test_09_of_61_verify_dictionary_parameters_check_parameters_validity_invalid_function_name(self):
        with raises(NameError):
            assert scmgr._verify_dictionary_parameters(data=[],
                                                       function_name='a')

    def test_10_of_61_verify_dictionary_parameters_check_parameters_validity_wrong_type(self):
        with raises(TypeError):
            assert scmgr._verify_dictionary_parameters(data='',
                                                       function_name='add_new_users')

    def test_11_of_61_verify_dictionary_parameters_check_parameters_validity_wrong_type_in_dict_values(self):
        with raises(TypeError):
            assert scmgr._verify_dictionary_parameters(data={'a'},
                                                       function_name='add_new_users')

    def test_12_of_61_verify_dictionary_parameters_check_parameters_validity_wrong_keys(self):
        with raises(KeyError):
            assert scmgr._verify_dictionary_parameters(data={'a': ['a']},
                                                       function_name='add_new_users')

    def test_13_of_61_verify_dictionary_parameters_check_parameters_validity_lists_length_empty(self):
        with raises(InvalidParameterError):
            assert scmgr._verify_dictionary_parameters(data={'user_cnpj_list': [],
                                                             'user_email_address_list': [],
                                                             'user_name_list': []},
                                                       function_name='add_new_users')

    def test_14_of_61_verify_dictionary_parameters_check_parameters_validity_lists_length_not_equal(self):
        with raises(InvalidParameterError):
            assert scmgr._verify_dictionary_parameters(data={'user_cnpj_list': [1, 2],
                                                             'user_email_address_list': [3, 4],
                                                             'user_name_list': [5]},
                                                       function_name='add_new_users')

    def test_15_of_61_verify_dictionary_parameters_check_str_type_values_wrong_type_in_dict_list_values(self):
        with raises(TypeError):
            assert scmgr._verify_dictionary_parameters(data={'user_cnpj_list': [1, 2],
                                                             'user_email_address_list': [3, 4],
                                                             'user_name_list': [5, 6]},
                                                       function_name='add_new_users')

    @utils.enclosure_prints(file=__file__, class_name=CLASS_NAME)
    def test_16_of_61_verify_dictionary_parameters_check_nested_dictionary_wrong_type_in_dict_list_values(self):
        with raises(InvalidParameterError):
            assert scmgr._verify_dictionary_parameters(data={'code_list': [1],
                                                             'hash_list': [1],
                                                             'mining_data_list': ['a'],
                                                             'owners_uid_list': [1],
                                                             'properties_list': [1]},
                                                       function_name='add_new_ornamental_blocks')

    @utils.enclosure_prints(file=__file__, class_name=CLASS_NAME)
    def test_17_of_61_verify_dictionary_parameters_check_nested_dictionary_wrong_nested_keys(self):
        with raises(InvalidParameterError):
            assert scmgr._verify_dictionary_parameters(data={'code_list': ['a'],
                                                             'hash_list': ['a'],
                                                             'mining_data_list': [{'a': 1}],
                                                             'owners_uid_list': ['a'],
                                                             'properties_list': ['a']},
                                                       function_name='add_new_ornamental_blocks')

    @utils.enclosure_prints(file=__file__, class_name=CLASS_NAME)
    def test_18_of_61_verify_dictionary_parameters_check_nested_dictionary_wrong_type_in_nested_values(self):
        with raises(InvalidParameterError):
            assert scmgr._verify_dictionary_parameters(data={'code_list': ['a'],
                                                             'hash_list': ['a'],
                                                             'mining_data_list': [{'company': 1,
                                                                                   'mining_date': 'a',
                                                                                   'mining_site': 'a'}],
                                                             'owners_uid_list': ['a'],
                                                             'properties_list': ['a']},
                                                       function_name='add_new_ornamental_blocks')

    @utils.enclosure_prints(file=__file__, class_name=CLASS_NAME)
    def test_19_of_61_verify_dictionary_parameters_in_add_new_ornamental_blocks_invalid_owner_uid(self):
        with raises(InvalidParameterError):
            assert scmgr._verify_dictionary_parameters(data={'code_list': ['a'],
                                                             'hash_list': ['a'],
                                                             'mining_data_list': [{'company': 'a',
                                                                                   'mining_date': 'a',
                                                                                   'mining_site': 'a'}],
                                                             'owners_uid_list': ['a'],
                                                             'properties_list': [{'dimensions': 'a',
                                                                                  'material': 'a',
                                                                                  'weight': 'a'}]},
                                                       function_name='add_new_ornamental_blocks')

    @utils.enclosure_prints(file=__file__, class_name=CLASS_NAME)
    def test_20_of_61_verify_dictionary_parameters_in_add_new_ornamental_blocks_owner_not_user(self):
        with raises(InvalidParameterError):
            assert scmgr._verify_dictionary_parameters(data={'code_list': ['a'],
                                                             'hash_list': ['a'],
                                                             'mining_data_list': [{'company': 'a',
                                                                                   'mining_date': 'a',
                                                                                   'mining_site': 'a'}],
                                                             'owners_uid_list': [account.address],
                                                             'properties_list': [{'dimensions': 'a',
                                                                                  'material': 'a',
                                                                                  'weight': 'a'}]},
                                                       function_name='add_new_ornamental_blocks')

    @utils.enclosure_prints(file=__file__, class_name=CLASS_NAME)
    def test_21_of_61_verify_dictionary_parameters_in_transfer_ornamental_blocks_invalid_block_uid(self):
        with raises(InvalidParameterError):
            assert scmgr._verify_dictionary_parameters(data={'invoice_number_list': ['a'],
                                                             'new_owner_uid_list': ['a'],
                                                             'ornamental_block_uid_list': ['a']},
                                                       function_name='transfer_ornamental_blocks')

    @utils.enclosure_prints(file=__file__, class_name=CLASS_NAME)
    def test_22_of_61_verify_dictionary_parameters_in_transfer_ornamental_blocks_invalid_owner_uid(self):
        with raises(InvalidParameterError):
            assert scmgr._verify_dictionary_parameters(data={'invoice_number_list': ['a'],
                                                             'new_owner_uid_list': ['a'],
                                                             'ornamental_block_uid_list': [account.address]},
                                                       function_name='transfer_ornamental_blocks')

    @utils.enclosure_prints(file=__file__, class_name=CLASS_NAME)
    def test_23_of_61_verify_dictionary_parameters_in_transfer_ornamental_blocks_owner_not_user(self):
        with raises(InvalidParameterError):
            assert scmgr._verify_dictionary_parameters(data={'invoice_number_list': ['a'],
                                                             'new_owner_uid_list': [account.address],
                                                             'ornamental_block_uid_list': [account.address]},
                                                       function_name='transfer_ornamental_blocks')

    def test_24_of_61_extract_new_user_args(self):
        new_users = [new('user', i) for i in range(20)]
        raw_data_1 = get_new_raw(type_='user', data=[new_users[0]])
        args_single_user = scmgr._extract_new_user_args(user_data=raw_data_1, list_length=1)

        assert args_single_user['user_name'] == new_users[0]['company_name']
        assert args_single_user['user_cnpj'] == new_users[0]['cnpj']
        assert args_single_user['user_email_address'] == new_users[0]['email_address']
        assert args_single_user['user_uid'] == Account.from_key(private_key=Web3.keccak(
            text=(new_users[0]['company_name'] + new_users[0]['cnpj']
                  + new_users[0]['email_address']))).address
        assert args_single_user['timestamp'][:10] == datetime.now().strftime("%Y/%m/%d")

        raw_data_5 = get_new_raw(type_='user', data=new_users[:5])
        args_5_users = scmgr._extract_new_user_args(user_data=raw_data_5, list_length=5)

        assert args_5_users['user_name_list'] == [new_user['company_name'] for new_user in new_users[:5]]
        assert args_5_users['user_cnpj_list'] == [new_user['cnpj'] for new_user in new_users[:5]]
        assert args_5_users['user_email_address_list'] == [new_user['email_address']
                                                           for new_user in new_users[:5]]
        assert args_5_users['user_uid_list'] == [Account.from_key(private_key=Web3.keccak(
            text=(new_user['company_name'] + new_user['cnpj']
                  + new_user['email_address']))).address for new_user in new_users[:5]]
        assert args_5_users['timestamp'][:10] == datetime.now().strftime("%Y/%m/%d")

        raw_data_10 = get_new_raw(type_='user', data=new_users[:10])
        args_10_users = scmgr._extract_new_user_args(user_data=raw_data_10, list_length=20)

        assert args_10_users['user_name_list'] == [new_user['company_name'] for new_user in new_users[:10]] + [''] * 10
        assert args_10_users['user_cnpj_list'] == [new_user['cnpj'] for new_user in new_users[:10]] + [''] * 10
        assert args_10_users['user_email_address_list'] == [new_user['email_address']
                                                            for new_user in new_users[:10]] + [''] * 10
        assert args_10_users['user_uid_list'] == [Account.from_key(private_key=Web3.keccak(
            text=(new_user['company_name'] + new_user['cnpj']
                  + new_user['email_address']))).address for new_user in new_users[:10]] + [ADDRESS_0] * 10
        assert args_10_users['timestamp'][:10] == datetime.now().strftime("%Y/%m/%d")

        raw_data_20 = get_new_raw(type_='user', data=new_users)
        args_20_users = scmgr._extract_new_user_args(user_data=raw_data_20, list_length=20)

        assert args_20_users['user_name_list'] == [new_user['company_name'] for new_user in new_users]
        assert args_20_users['user_cnpj_list'] == [new_user['cnpj'] for new_user in new_users]
        assert args_20_users['user_email_address_list'] == [new_user['email_address']
                                                            for new_user in new_users]
        assert args_20_users['user_uid_list'] == [Account.from_key(private_key=Web3.keccak(
            text=(new_user['company_name'] + new_user['cnpj']
                  + new_user['email_address']))).address for new_user in new_users]
        assert args_20_users['timestamp'][:10] == datetime.now().strftime("%Y/%m/%d")

    def test_25_of_61_extract_new_ob_args(self):
        new_blocks = [new('block', i) for i in range(20)]
        raw_data_1 = get_new_raw(type_='block', data=[new_blocks[0]])
        raw_data_1['mining_data_list'] = [json.dumps(value_data) for value_data in raw_data_1['mining_data_list']]
        raw_data_1['properties_list'] = [json.dumps(value_data) for value_data in raw_data_1['properties_list']]
        args_single_block = scmgr._extract_new_ob_args(ornamental_block_data=raw_data_1, list_length=1)

        assert args_single_block['mining_data'] == json.dumps(new_blocks[0]['mining_data'])
        assert args_single_block['code'] == new_blocks[0]['code']
        assert args_single_block['properties'] == json.dumps(new_blocks[0]['properties'])
        assert args_single_block['hash'] == new_blocks[0]['hash']
        assert args_single_block['owners_uid'] == new_blocks[0]['last_owners']
        assert args_single_block['ornamental_block_uid'] == Account.from_key(private_key=Web3.keccak(
            text=(json.dumps(new_blocks[0]['mining_data']) +
                  new_blocks[0]['code'] +
                  json.dumps(new_blocks[0]['properties']) +
                  new_blocks[0]['hash']))).address
        assert args_single_block['timestamp'][:10] == datetime.now().strftime("%Y/%m/%d")

        raw_data_5 = get_new_raw(type_='block', data=new_blocks[:5])
        raw_data_5['mining_data_list'] = [json.dumps(value_data) for value_data in raw_data_5['mining_data_list']]
        raw_data_5['properties_list'] = [json.dumps(value_data) for value_data in raw_data_5['properties_list']]
        args_5_blocks = scmgr._extract_new_ob_args(ornamental_block_data=raw_data_5, list_length=5)

        assert args_5_blocks['mining_data_list'] == [json.dumps(new_block['mining_data']) for new_block in
                                                     new_blocks[:5]]
        assert args_5_blocks['code_list'] == [new_block['code'] for new_block in new_blocks[:5]]
        assert args_5_blocks['properties_list'] == [json.dumps(new_block['properties']) for new_block in new_blocks[:5]]
        assert args_5_blocks['hash_list'] == [new_block['hash'] for new_block in new_blocks[:5]]
        assert args_5_blocks['owners_uid_list'] == [new_block['last_owners'] for new_block in new_blocks[:5]]
        assert args_5_blocks['ornamental_block_uid_list'] == [Account.from_key(private_key=Web3.keccak(
            text=(json.dumps(new_block['mining_data']) +
                  new_block['code'] +
                  json.dumps(new_block['properties']) +
                  new_block['hash']))).address for new_block in new_blocks[:5]]
        assert args_5_blocks['timestamp'][:10] == datetime.now().strftime("%Y/%m/%d")

        raw_data_10 = get_new_raw(type_='block', data=new_blocks[:10])
        raw_data_10['mining_data_list'] = [json.dumps(value_data) for value_data in raw_data_10['mining_data_list']]
        raw_data_10['properties_list'] = [json.dumps(value_data) for value_data in raw_data_10['properties_list']]
        args_10_users = scmgr._extract_new_ob_args(ornamental_block_data=raw_data_10, list_length=20)

        assert args_10_users['mining_data_list'] == [json.dumps(new_block['mining_data']) for new_block in
                                                     new_blocks[:10]] + [''] * 10
        assert args_10_users['code_list'] == [new_block['code'] for new_block in new_blocks[:10]] + [''] * 10
        assert args_10_users['properties_list'] == [json.dumps(new_block['properties']) for new_block in
                                                    new_blocks[:10]] + [''] * 10
        assert args_10_users['hash_list'] == [new_block['hash'] for new_block in new_blocks[:10]] + [''] * 10
        assert args_10_users['owners_uid_list'] == [new_block['last_owners'] for new_block in new_blocks[:10]] + [
            ADDRESS_0] * 10
        assert args_10_users['ornamental_block_uid_list'] == [Account.from_key(private_key=Web3.keccak(
            text=(json.dumps(new_block['mining_data']) +
                  new_block['code'] +
                  json.dumps(new_block['properties']) +
                  new_block['hash']))).address for new_block in new_blocks[:10]] + [ADDRESS_0] * 10
        assert args_10_users['timestamp'][:10] == datetime.now().strftime("%Y/%m/%d")

        raw_data_20 = get_new_raw(type_='block', data=new_blocks)
        raw_data_20['mining_data_list'] = [json.dumps(value_data) for value_data in raw_data_20['mining_data_list']]
        raw_data_20['properties_list'] = [json.dumps(value_data) for value_data in raw_data_20['properties_list']]
        args_20_users = scmgr._extract_new_ob_args(ornamental_block_data=raw_data_20, list_length=20)

        assert args_20_users['mining_data_list'] == [json.dumps(new_block['mining_data']) for new_block in new_blocks]
        assert args_20_users['code_list'] == [new_block['code'] for new_block in new_blocks]
        assert args_20_users['properties_list'] == [json.dumps(new_block['properties']) for new_block in new_blocks]
        assert args_20_users['hash_list'] == [new_block['hash'] for new_block in new_blocks]
        assert args_20_users['owners_uid_list'] == [new_block['last_owners'] for new_block in new_blocks]
        assert args_20_users['ornamental_block_uid_list'] == [Account.from_key(private_key=Web3.keccak(
            text=(json.dumps(new_block['mining_data']) +
                  new_block['code'] +
                  json.dumps(new_block['properties']) +
                  new_block['hash']))).address for new_block in new_blocks]
        assert args_20_users['timestamp'][:10] == datetime.now().strftime("%Y/%m/%d")

    def test_26_of_61_extract_transfer_ob_args(self):
        new_blocks = [new('block', i) for i in range(20)]
        new_users = [new('user', i) for i in range(20)]
        raw_data_1 = {'ornamental_block_uid_list': [new_blocks[0]['uid']],
                      'new_owner_uid_list': [new_users[0]['uid']],
                      'invoice_number_list': ['invoice_number_0']}
        args_single_transfer = scmgr._extract_transfer_ob_args(transfer_data=raw_data_1, list_length=1)

        assert args_single_transfer['ornamental_block_uid'] == new_blocks[0]['uid']
        assert args_single_transfer['new_owner_uid'] == new_users[0]['uid']
        assert args_single_transfer['invoice_number'] == 'invoice_number_0'
        assert args_single_transfer['timestamp'][:10] == datetime.now().strftime("%Y/%m/%d")

        raw_data_5 = {'ornamental_block_uid_list': [new_block['uid'] for new_block in new_blocks[:5]],
                      'new_owner_uid_list': [new_users[0]['uid']] * 5,
                      'invoice_number_list': [f"invoice_number_{i}" for i in range(5)]}
        args_5_transfer = scmgr._extract_transfer_ob_args(transfer_data=raw_data_5, list_length=5)

        assert args_5_transfer['ornamental_block_uid_list'] == [new_block['uid'] for new_block in new_blocks[:5]]
        assert args_5_transfer['new_owner_uid_list'] == [new_users[0]['uid']] * 5
        assert args_5_transfer['invoice_number_list'] == [f"invoice_number_{i}" for i in range(5)]
        assert args_5_transfer['timestamp'][:10] == datetime.now().strftime("%Y/%m/%d")

        raw_data_10 = {'ornamental_block_uid_list': [new_block['uid'] for new_block in new_blocks[:10]],
                       'new_owner_uid_list': [new_users[0]['uid']] * 10,
                       'invoice_number_list': [f"invoice_number_{i}" for i in range(10)]}
        args_10_transfer = scmgr._extract_transfer_ob_args(transfer_data=raw_data_10, list_length=20)

        assert (args_10_transfer['ornamental_block_uid_list'] ==
                [new_block['uid'] for new_block in new_blocks[:10]] + [ADDRESS_0] * 10)
        assert args_10_transfer['new_owner_uid_list'] == [new_users[0]['uid']] * 10 + [ADDRESS_0] * 10
        assert args_10_transfer['invoice_number_list'] == [f"invoice_number_{i}" for i in range(10)] + [''] * 10
        assert args_10_transfer['timestamp'][:10] == datetime.now().strftime("%Y/%m/%d")

        raw_data_20 = {'ornamental_block_uid_list': [new_block['uid'] for new_block in new_blocks],
                       'new_owner_uid_list': [new_users[0]['uid']] * 20,
                       'invoice_number_list': [f"invoice_number_{i}" for i in range(20)]}
        args_20_transfer = scmgr._extract_transfer_ob_args(transfer_data=raw_data_20, list_length=20)

        assert args_20_transfer['ornamental_block_uid_list'] == [new_block['uid'] for new_block in new_blocks]
        assert args_20_transfer['new_owner_uid_list'] == [new_users[0]['uid']] * 20
        assert args_20_transfer['invoice_number_list'] == [f"invoice_number_{i}" for i in range(20)]
        assert args_20_transfer['timestamp'][:10] == datetime.now().strftime("%Y/%m/%d")

    def test_27_of_61_extract_deactivate_ob_args(self):
        new_blocks = [new('block', i) for i in range(20)]
        raw_data_1 = {'ornamental_block_uid_list': [new_blocks[0]['uid']]}
        args_single_deactivation = scmgr._extract_deactivate_ob_args(ornamental_block_data=raw_data_1, list_length=1)

        assert args_single_deactivation['ornamental_block_uid'] == new_blocks[0]['uid']
        assert args_single_deactivation['timestamp'][:10] == datetime.now().strftime("%Y/%m/%d")

        raw_data_5 = {'ornamental_block_uid_list': [new_block['uid'] for new_block in new_blocks[:5]]}
        args_5_deactivation = scmgr._extract_deactivate_ob_args(ornamental_block_data=raw_data_5, list_length=5)

        assert args_5_deactivation['ornamental_block_uid_list'] == [new_block['uid'] for new_block in new_blocks[:5]]
        assert args_5_deactivation['timestamp'][:10] == datetime.now().strftime("%Y/%m/%d")

        raw_data_10 = {'ornamental_block_uid_list': [new_block['uid'] for new_block in new_blocks[:10]]}
        args_10_deactivation = scmgr._extract_deactivate_ob_args(ornamental_block_data=raw_data_10, list_length=20)

        assert (args_10_deactivation['ornamental_block_uid_list'] ==
                [new_block['uid'] for new_block in new_blocks[:10]] + [ADDRESS_0] * 10)
        assert args_10_deactivation['timestamp'][:10] == datetime.now().strftime("%Y/%m/%d")

        raw_data_20 = {'ornamental_block_uid_list': [new_block['uid'] for new_block in new_blocks]}
        args_20_deactivation = scmgr._extract_deactivate_ob_args(ornamental_block_data=raw_data_20, list_length=20)

        assert args_20_deactivation['ornamental_block_uid_list'] == [new_block['uid'] for new_block in new_blocks]
        assert args_20_deactivation['timestamp'][:10] == datetime.now().strftime("%Y/%m/%d")

    # @utils.enclosure_prints(file=__file__, class_name=CLASS_NAME)
    # def test_28_of_61_make_transaction_three_users(self):
    #     [shared_data['users'].append(new('user', n)) for n in range(3)]
    #     users = shared_data['users']
    #     args = {'sc_functions_list': [contract_obj.functions.add_new_user,
    #                                   contract_obj.functions.add_up_to_5_new_users,
    #                                   contract_obj.functions.add_up_to_20_new_users],
    #             'extract_args_function': SCManager._extract_new_user_args,
    #             'data': {'user_name_list': [user['company_name'] for user in users],
    #                      'user_cnpj_list': [user['cnpj'] for user in users],
    #                      'user_email_address_list': [user['email_address'] for user in users]},
    #             'account': account,
    #             'sclink': sclink,
    #             'timeout': TIMEOUT,
    #             'persist': PERSIST,
    #             'estimate_cost': True}
    #
    #     data = utils.ignore_requests(function=SCManager._make_transaction,
    #                                  kwargs=args,
    #                                  ignore=IGNORE_REQUESTS)
    #
    #     assert data[0]['contract_address'] == contract_obj.address
    #     assert data[0]['from'] == account.address
    #     assert data[0]['function'] == 'add_new_user'
    #     new_users = {'uid': contract_obj.functions.get_user_uids_list().call()[1]}
    #     assert [new_user['uid'] for new_user in new_users] == [user['uid'] for user in users]
    #     user_data_list = [contract_obj.functions.get_user_data(new_user['uid']).call() for new_user in new_users]
    #     assert user_data_list[0] == user_0['uid']
    #     assert user_data_list[1] == user_0['list_index']
    #     assert user_data_list[4] == user_0['company_name']
    #     assert user_data_list[5] == user_0['cnpj']
    #     assert user_data_list[6] == user_0['email_address']
    #     assert user_data_list[7] == []
    #     shared_data['users'][0]['registration_timestamp'] = user_data_list[2]
    #     shared_data['users'][0]['last_update_timestamp'] = user_data_list[3]

    @utils.enclosure_prints(file=__file__, class_name=CLASS_NAME)
    def test_28_of_61_make_transaction_three_users(self):
        [shared_data['users'].append(new('user', n)) for n in range(3)]
        users = shared_data['users']
        args = {'sc_functions_list': [contract_obj.functions.add_new_user,
                                      contract_obj.functions.add_up_to_5_new_users,
                                      contract_obj.functions.add_up_to_20_new_users],
                'extract_args_function': SCManager._extract_new_user_args,
                'data': {'user_name_list': [user['company_name'] for user in users],
                         'user_cnpj_list': [user['cnpj'] for user in users],
                         'user_email_address_list': [user['email_address'] for user in users]},
                'account': account,
                'sclink': sclink,
                'timeout': TIMEOUT,
                'persist': 3,
                'estimate_cost': True}

        data = utils.ignore_requests(function=SCManager._make_transaction,
                                     kwargs=args,
                                     ignore=IGNORE_REQUESTS)

        assert data[0]['contract_address'] == contract_obj.address
        assert data[0]['from'] == account.address
        assert data[0]['function'] == 'add_up_to_5_new_users'
        new_users = {'uid': contract_obj.functions.get_user_uids_list().call()[1:]}
        assert new_users['uid'] == [user['uid'] for user in users]
        user_data_list = [contract_obj.functions.get_user_data(uid).call() for uid in new_users['uid']]
        assert [user_data[0] for user_data in user_data_list] == [user['uid'] for user in users]
        assert [user_data[1] for user_data in user_data_list] == [user['list_index'] for user in users]
        assert [user_data[4] for user_data in user_data_list] == [user['company_name'] for user in users]
        assert [user_data[5] for user_data in user_data_list] == [user['cnpj'] for user in users]
        assert [user_data[6] for user_data in user_data_list] == [user['email_address'] for user in users]
        assert [user_data[7] for user_data in user_data_list] == [user['ornamental_blocks_list'] for user in users]
        for _ in range(3):
            shared_data['users'][_]['registration_timestamp'] = user_data_list[_][2]
            shared_data['users'][_]['last_update_timestamp'] = user_data_list[_][3]

    def test_29_of_61_get_user_data_valid(self):
        user_0 = shared_data['users'][0]
        testing_user_0 = scmgr.get_user_data(user_uid=user_0['uid'])
        assert testing_user_0['uid'] == user_0['uid']
        assert testing_user_0['list_index'] == user_0['list_index']
        assert testing_user_0['registration_timestamp'] == user_0['registration_timestamp']
        assert testing_user_0['last_update_timestamp'] == user_0['last_update_timestamp']
        assert testing_user_0['company_name'] == user_0['company_name']
        assert testing_user_0['cnpj'] == user_0['cnpj']
        assert testing_user_0['email_address'] == user_0['email_address']
        assert testing_user_0['ornamental_blocks_list'] == user_0['ornamental_blocks_list']
        assert testing_user_0 == user_0

    @utils.enclosure_prints(file=__file__, class_name=CLASS_NAME)
    def test_30_of_61_verify_dictionary_parameters_in_transfer_ornamental_blocks_not_block(self):
        with raises(InvalidParameterError):
            assert scmgr._verify_dictionary_parameters(data={'invoice_number_list': ['a'],
                                                             'new_owner_uid_list': [shared_data['users'][0]['uid']],
                                                             'ornamental_block_uid_list': [account.address]},
                                                       function_name='transfer_ornamental_blocks')

    def test_31_of_61_get_account_balance(self):
        account_balance = sclink.get_balance(account.address)
        assert scmgr.get_account_balance() == account_balance

    def test_32_of_61_get_contract_data(self):
        contract_data = contract_obj.functions.get_contract_data().call()
        testing_data = scmgr.get_contract_data()
        assert testing_data['recovered_contracts_address_list'] == contract_data[0]
        assert testing_data['user_uids_list'] == contract_data[1][1:]
        assert testing_data['users_list'] == SCManager._process_user_list(contract_data[2])[1:]
        assert testing_data['ornamental_block_uids_list'] == contract_data[3]
        assert testing_data['ornamental_blocks_list'] == SCManager._process_ornamental_block_list(contract_data[4])

    def test_33_of_61_get_inactive_ornamental_block_uids_list_empty(self):
        dump_list = contract_obj.functions.get_user_data(ADDRESS_0).call()[7]
        assert scmgr.get_inactive_ornamental_block_uids_list() == dump_list

    def test_34_of_61_get_last_updated_timestamp(self):
        last_upd = contract_obj.functions.get_last_updated_timestamp().call()
        assert scmgr.get_last_updated_timestamp() == last_upd

    def test_35_of_61_get_user_uids_list(self):
        uids_list = [user['uid'] for user in shared_data['users']]
        assert scmgr.get_user_uids_list() == uids_list

    def test_36_of_61_get_ornamental_block_uids_list_empty(self):
        uids_list = []
        assert scmgr.get_ornamental_block_uids_list() == uids_list

    def test_37_of_61_is_user_invalid_checksum_address(self):
        with raises(InvalidParameterError):
            assert scmgr.is_user(uid=1)

    def test_38_of_61_is_user_invalid_null(self):
        assert not scmgr.is_user(uid=ADDRESS_0)

    def test_39_of_61_is_user_false(self):
        assert not scmgr.is_user(uid=scmgr.web3_contract_object.address)

    def test_40_of_61_is_user_success(self):
        assert scmgr.is_user(uid=shared_data['users'][0]['uid'])

    def test_41_of_61_is_ornamental_block_invalid_checksum_address(self):
        with raises(InvalidParameterError):
            assert scmgr.is_ornamental_block(uid=1)

    def test_42_of_61_is_ornamental_block_false(self):
        assert not scmgr.is_ornamental_block(uid=scmgr.web3_contract_object.address)

    def test_43_of_61_get_user_data_invalid(self):
        with raises(InvalidParameterError):
            assert scmgr.get_user_data(user_uid=scmgr.web3_contract_object.address)

    def test_44_of_61_get_user_data_null(self):
        with raises(InvalidParameterError):
            assert scmgr.get_user_data(user_uid=ADDRESS_0)

    def test_45_of_61_get_ornamental_block_data_invalid(self):
        with raises(InvalidParameterError):
            assert scmgr.get_ornamental_block_data(ornamental_block_uid=ADDRESS_0)

    def test_46_of_61_is_ornamental_block_active_invalid(self):
        with raises(InvalidParameterError):
            assert scmgr.is_ornamental_block_active(ornamental_block_uid=ADDRESS_0)

    @utils.enclosure_prints(file=__file__, class_name=CLASS_NAME)
    def test_47_of_61_add_new_users_single_user(self):
        shared_data['users'].append(new('user', len(shared_data['users'])))
        new_user = shared_data['users'][3]
        args = {'user_name_list': [new_user['company_name']],
                'user_cnpj_list': [new_user['cnpj']],
                'user_email_address_list': [new_user['email_address']],
                'estimate_cost': True}

        users, txs = utils.ignore_requests(function=scmgr.add_new_users,
                                           kwargs=args,
                                           ignore=IGNORE_REQUESTS)

        assert scmgr.get_last_updated_timestamp() == users[0]['registration_timestamp']
        assert scmgr.is_user(new_user['uid'])
        assert scmgr.get_contract_data()['user_uids_list'] == [user['uid'] for user in shared_data['users']]
        assert scmgr.get_user_uids_list() == [user['uid'] for user in shared_data['users']]

        assert users[0]['uid'] == new_user['uid']
        assert users[0]['list_index'] == new_user['list_index']
        assert users[0]['company_name'] == new_user['company_name']
        assert users[0]['cnpj'] == new_user['cnpj']
        assert users[0]['email_address'] == new_user['email_address']
        assert users[0]['ornamental_blocks_list'] == new_user['ornamental_blocks_list']

        shared_data['users'][3]['registration_timestamp'] = users[0]['registration_timestamp']
        shared_data['users'][3]['last_update_timestamp'] = users[0]['last_update_timestamp']

        assert scmgr.get_user_data(new_user['uid']) == shared_data['users'][3]

        assert txs[0]['contract_address'] == contract_obj.address
        assert txs[0]['from'] == account.address
        assert txs[0]['function'] == 'add_new_user'

    @utils.enclosure_prints(file=__file__, class_name=CLASS_NAME)
    def test_48_of_61_add_new_ornamental_blocks_three_blocks(self):
        [shared_data['blocks'].append(new('block', i)) for i in range(3)]
        new_blocks = shared_data['blocks']
        for new_block in new_blocks:
            new_block['last_owners'] = [shared_data['users'][0]['uid']]

        args = {'mining_data_list': [new_block['mining_data'] for new_block in new_blocks],
                'code_list': [new_block['code'] for new_block in new_blocks],
                'properties_list': [new_block['properties'] for new_block in new_blocks],
                'hash_list': [new_block['hash'] for new_block in new_blocks],
                'owners_uid_list': [new_block['last_owners'][0] for new_block in new_blocks],
                'estimate_cost': True}

        blocks, txs = utils.ignore_requests(function=scmgr.add_new_ornamental_blocks,
                                            kwargs=args,
                                            ignore=IGNORE_REQUESTS)

        assert scmgr.get_last_updated_timestamp() == blocks[0]['registration_timestamp']
        assert all([scmgr.is_ornamental_block(new_block['uid']) for new_block in new_blocks])
        assert all([scmgr.is_ornamental_block_active(new_block['uid']) for new_block in new_blocks])
        assert scmgr.get_contract_data()['ornamental_block_uids_list'] == [block['uid'] for block in
                                                                           shared_data['blocks']]
        assert scmgr.get_ornamental_block_uids_list() == [block['uid'] for block in shared_data['blocks']]

        assert [block['uid'] for block in blocks] == [new_block['uid'] for new_block in new_blocks]
        assert [block['hash'] for block in blocks] == [new_block['hash'] for new_block in new_blocks]
        assert [block['invoice_numbers'] for block in blocks] == [new_block['invoice_numbers'] for new_block in
                                                                  new_blocks]
        assert [block['is_active'] for block in blocks] == [new_block['is_active'] for new_block in new_blocks]
        assert [block['last_owners'] for block in blocks] == [new_block['last_owners'] for new_block in new_blocks]
        assert [block['list_index'] for block in blocks] == [new_block['list_index'] for new_block in new_blocks]
        assert [block['mining_data'] for block in blocks] == [new_block['mining_data'] for new_block in new_blocks]
        assert [block['properties'] for block in blocks] == [new_block['properties'] for new_block in new_blocks]

        for i, block in enumerate(blocks):
            shared_data['blocks'][i]['registration_timestamp'] = block['registration_timestamp']
            shared_data['blocks'][i]['last_update_timestamp'] = block['last_update_timestamp']
            shared_data['blocks'][i]['last_owners'] = block['last_owners']
            shared_data['users'][0]['ornamental_blocks_list'].append(block['uid'])
        shared_data['users'][0]['last_update_timestamp'] = blocks[-1]['last_update_timestamp']

        assert [scmgr.get_ornamental_block_data(new_block['uid']) for new_block in new_blocks] == shared_data['blocks']

        assert txs[0]['contract_address'] == contract_obj.address
        assert txs[0]['from'] == account.address
        assert txs[0]['function'] == 'add_up_to_5_new_ornamental_blocks'

    def test_49_of_61_verify_dictionary_parameters_success(self):
        user_0 = shared_data['users'][0]
        ob_0_uid = shared_data['blocks'][0]['uid']
        add_user_data = {'user_cnpj_list': ['a'],
                         'user_email_address_list': ['a'],
                         'user_name_list': ['a']}
        add_ob_data = {'code_list': ['a'],
                       'hash_list': ['a'],
                       'mining_data_list': [{'company': 'a',
                                             'mining_date': 'a',
                                             'mining_site': 'a'}],
                       'owners_uid_list': [user_0['uid']],
                       'properties_list': [{'dimensions': 'a',
                                            'material': 'a',
                                            'weight': 'a'}]}
        transfer_data = {'invoice_number_list': ['a'],
                         'new_owner_uid_list': [user_0['uid']],
                         'ornamental_block_uid_list': [ob_0_uid]}

        testing_add_user_data = scmgr._verify_dictionary_parameters(data=add_user_data,
                                                                    function_name='add_new_users')
        testing_add_ob_data = scmgr._verify_dictionary_parameters(data=add_ob_data,
                                                                  function_name='add_new_ornamental_blocks')
        add_ob_data['mining_data_list'][0] = [json.dumps(value_data) for value_data in add_ob_data['mining_data_list']]
        add_ob_data['properties_list'][0] = [json.dumps(value_data) for value_data in add_ob_data['properties_list']]
        testing_transfer_data = scmgr._verify_dictionary_parameters(data=transfer_data,
                                                                    function_name='transfer_ornamental_blocks')

        assert testing_add_user_data == add_user_data
        assert testing_add_ob_data == add_ob_data
        assert testing_transfer_data == transfer_data

    @utils.enclosure_prints(file=__file__, class_name=CLASS_NAME)
    def test_50_of_61_deactivate_ornamental_blocks(self):
        block = shared_data['blocks'].pop(2)
        block['is_active'] = False
        block['last_owners'].append(ADDRESS_0)
        shared_data['inactive_blocks'].append(block)
        last_owner = shared_data['users'][0]

        args = {'ornamental_block_uid_list': [block['uid']],
                'estimate_cost': True}

        inactive_blocks, txs = utils.ignore_requests(function=scmgr.deactivate_ornamental_blocks,
                                                     kwargs=args,
                                                     ignore=IGNORE_REQUESTS)

        assert scmgr.get_last_updated_timestamp() == inactive_blocks[0]['last_update_timestamp']
        assert scmgr.is_ornamental_block(block['uid'])
        assert not scmgr.is_ornamental_block_active(block['uid'])
        assert scmgr.get_inactive_ornamental_block_uids_list() == [block['uid']]

        assert inactive_blocks[0]['uid'] == block['uid']
        assert inactive_blocks[0]['last_owners'] == [shared_data['users'][0]['uid'], ADDRESS_0]
        assert inactive_blocks[0]['registration_timestamp'] == block['registration_timestamp']

        web3_last_owner = scmgr.get_user_data(last_owner['uid'])

        assert web3_last_owner['last_update_timestamp'] == inactive_blocks[0]['last_update_timestamp']
        assert web3_last_owner['ornamental_blocks_list'] == [shared_data['blocks'][0]['uid'],
                                                             shared_data['blocks'][1]['uid']]

        shared_data['inactive_blocks'][0]['last_update_timestamp'] = inactive_blocks[0]['last_update_timestamp']
        shared_data['inactive_blocks'][0]['invoice_numbers'] = inactive_blocks[0]['invoice_numbers']
        shared_data['users'][0]['last_update_timestamp'] = inactive_blocks[0]['last_update_timestamp']
        shared_data['users'][0]['ornamental_blocks_list'].remove(block['uid'])

        assert scmgr.get_ornamental_block_data(block['uid']) == shared_data['inactive_blocks'][0]

        assert txs[0]['contract_address'] == contract_obj.address
        assert txs[0]['from'] == account.address
        assert txs[0]['function'] == 'deactivate_ornamental_block'

    @utils.enclosure_prints(file=__file__, class_name=CLASS_NAME)
    def test_51_of_61_transfer_ornamental_blocks(self):
        block = shared_data['blocks'][1]
        last_owner = shared_data['users'][0]
        new_owner = shared_data['users'][1]
        block['last_owners'].append(new_owner['uid'])

        args = {'ornamental_block_uid_list': [block['uid']],
                'new_owner_uid_list': [new_owner['uid']],
                'invoice_number_list': ['testing_invoice_number_0'],
                'estimate_cost': True}

        transfered_blocks, txs = utils.ignore_requests(function=scmgr.transfer_ornamental_blocks,
                                                       kwargs=args,
                                                       ignore=IGNORE_REQUESTS)

        assert scmgr.get_last_updated_timestamp() == transfered_blocks[0]['last_update_timestamp']
        assert scmgr.is_ornamental_block(block['uid'])
        assert scmgr.is_ornamental_block_active(block['uid'])

        assert transfered_blocks[0]['uid'] == block['uid']
        assert transfered_blocks[0]['last_owners'] == block['last_owners']
        assert transfered_blocks[0]['registration_timestamp'] == block['registration_timestamp']
        assert transfered_blocks[0]['invoice_numbers'] == ['testing_invoice_number_0']
        web3_last_owner = scmgr.get_user_data(last_owner['uid'])
        web3_new_owner = scmgr.get_user_data(new_owner['uid'])
        assert web3_last_owner['last_update_timestamp'] == transfered_blocks[0]['last_update_timestamp']
        assert web3_last_owner['ornamental_blocks_list'] == [shared_data['blocks'][0]['uid']]
        assert web3_new_owner['last_update_timestamp'] == transfered_blocks[0]['last_update_timestamp']
        assert web3_new_owner['ornamental_blocks_list'] == [shared_data['blocks'][1]['uid']]

        shared_data['blocks'][1]['last_update_timestamp'] = transfered_blocks[0]['last_update_timestamp']
        shared_data['blocks'][1]['invoice_numbers'] = transfered_blocks[0]['invoice_numbers']
        shared_data['users'][0]['last_update_timestamp'] = transfered_blocks[0]['last_update_timestamp']
        shared_data['users'][1]['last_update_timestamp'] = transfered_blocks[0]['last_update_timestamp']
        shared_data['users'][0]['ornamental_blocks_list'].remove(block['uid'])
        shared_data['users'][1]['ornamental_blocks_list'].append(block['uid'])

        assert scmgr.get_ornamental_block_data(block['uid']) == shared_data['blocks'][1]

        assert txs[0]['contract_address'] == contract_obj.address
        assert txs[0]['from'] == account.address
        assert txs[0]['function'] == 'transfer_ornamental_block'

    @utils.enclosure_prints(file=__file__, class_name=CLASS_NAME)
    def test_52_of_61_verify_list_parameters_invalid_data_elements(self):
        data = [0, ADDRESS_0, shared_data['inactive_blocks'][0]['uid']]
        with raises(InvalidParameterError):
            assert scmgr._verify_list_parameters(data=data,
                                                 function_name='deactivate_ornamental_blocks')

    def test_53_of_61_verify_list_parameters_success(self):
        data = [block['uid'] for block in shared_data['blocks'][:2]]
        testing_data = scmgr._verify_list_parameters(data=data,
                                                     function_name='deactivate_ornamental_blocks')
        assert testing_data == data

    @utils.enclosure_prints(file=__file__, class_name=CLASS_NAME)
    def test_54_of_61_verify_dictionary_parameters_in_transfer_ornamental_blocks_inactive_block(self):
        user_0 = shared_data['users'][0]
        ob_0_uid = shared_data['inactive_blocks'][0]['uid']
        with raises(InvalidParameterError):
            assert scmgr._verify_dictionary_parameters(data={'invoice_number_list': ['a'],
                                                             'new_owner_uid_list': [user_0['uid']],
                                                             'ornamental_block_uid_list': [ob_0_uid]},
                                                       function_name='transfer_ornamental_blocks')

    def test_55_of_61_get_ornamental_block_uids_list_not_empty(self):
        uids_list = contract_obj.functions.get_ornamental_block_uids_list().call()
        assert scmgr.get_ornamental_block_uids_list() == uids_list

    def test_56_of_61_get_inactive_ornamental_block_uids_list_not_empty(self):
        dump_list = contract_obj.functions.get_user_data(ADDRESS_0).call()[7]
        assert scmgr.get_inactive_ornamental_block_uids_list() == dump_list

    def test_57_of_61_is_ornamental_block_true(self):
        ob_0_uid = shared_data['blocks'][0]['uid']
        assert scmgr.is_ornamental_block(uid=ob_0_uid)

    #
    def test_58_of_61_get_ornamental_block_data_valid(self):
        ob_0 = shared_data['blocks'][0]
        testing_ob_0 = scmgr.get_ornamental_block_data(ornamental_block_uid=ob_0['uid'])
        assert testing_ob_0['uid'] == ob_0['uid']
        assert testing_ob_0['list_index'] == ob_0['list_index']
        assert testing_ob_0['registration_timestamp'] == ob_0['registration_timestamp']
        assert testing_ob_0['last_update_timestamp'] == ob_0['last_update_timestamp']
        assert testing_ob_0['mining_data'] == ob_0['mining_data']
        assert testing_ob_0['code'] == ob_0['code']
        assert testing_ob_0['properties'] == ob_0['properties']
        assert testing_ob_0['hash'] == ob_0['hash']
        assert testing_ob_0['is_active'] == ob_0['is_active']
        assert testing_ob_0['last_owners'] == ob_0['last_owners']
        assert testing_ob_0['invoice_numbers'] == ob_0['invoice_numbers']
        assert testing_ob_0 == ob_0

    def test_59_of_61_is_ornamental_block_active_false(self):
        block = shared_data['inactive_blocks'][0]
        assert not scmgr.is_ornamental_block_active(ornamental_block_uid=block['uid'])

    def test_60_of_61_is_ornamental_block_active_true(self):
        block = shared_data['blocks'][0]
        assert scmgr.is_ornamental_block_active(ornamental_block_uid=block['uid'])

    @utils.enclosure_prints(file=__file__, class_name=CLASS_NAME)
    def test_61_of_61_repr(self):
        print(scmgr)
        assert scmgr.__repr__() == get_repr()
