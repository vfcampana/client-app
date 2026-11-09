"""
example
=======

This module demonstrates the use of the SCManager package. It includes functions for generating dummy data such as CNPJs, users,
mining blocks, and transfers, as well as a function to execute a series of demo operations.

Imports
-------
- from scmanager import SCManager
- from scmanager.admin_tools import create_config_file
- from pprint import pprint
- from pathlib import Path
- import random
- import string
- import shutil
- import json
- import re

Functions
---------
1. generate_cnpj() -> str
   Generates a random CNPJ number.

2. generate_dummy_users(number_of_users: int = 1) -> dict[str, list]
   Generates dummy users with random names, CNPJs, and email addresses.

3. generate_dummy_blocks(owner_uids_list: list) -> dict[str, list]
   Generates dummy blocks with random mining data, properties, and unique identifiers.

4. generate_dummy_transfers(block_uids_list: list[str], new_owner_uids_list: list[str]) -> dict[str, list]
   Generates dummy transfer data with random invoice numbers for ornamental blocks.

5. run()
   Executes a series of operations to demonstrate the usage of the SCLibrary package.

Usage
-----
To use this module, import the desired functions and execute them as needed. For example:

    from scmanager.example import generate_dummy_users, generate_dummy_blocks, run

    # Generate dummy users:
    users = generate_dummy_users(number_of_users=5)
    print(users)

    # Generate dummy blocks:
    owner_uids = ['uid1', 'uid2', 'uid3']
    blocks = generate_dummy_blocks(owner_uids_list=owner_uids)
    print(blocks)

    # Run the function to execute the full demo:
    run()
    This module simplifies the creation of dummy data for testing and examples and demonstrates
    the usage of the SCManager.

Environment
-----------

The module 'admin_tools' uses environment variables loaded from a .env file to manage
sensitive information such as private keys. Ensure that the .env file is properly configured

Dependencies
------------

- SCManager: Main package used for demonstration.
- pprint: Formats and prints data in a readable way.
- pathlib: Handles file and directory paths.
- random: Generates random values.
- string: Manipulates strings.
- shutil: Handles high-level file operations.
- json: Manipulates JSON data.
- re: Regular expressions for pattern matching.
"""
from scmanager.admin_tools import create_config_file
from scmanager import SCManager
from pprint import pprint
from pathlib import Path
import random
import string
import shutil
import json
import re

SCREEN_LENGTH = shutil.get_terminal_size()[0]


def _generate_cnpj() -> str:
    """
    Generates a random CNPJ number.

    This function generates a random CNPJ number by creating a list of 8 random digits followed by
    four fixed digits (0001), and then adding two check digits.

    :return: The generated CNPJ number in the format 'XX.XXX.XXX/XXXX-XX'.
    :rtype: str
    """
    cnpj_number = [random.randrange(10) for _ in range(8)] + [0, 0, 0, 1]
    for _ in range(2):
        value = sum(v * (i % 8 + 2) for i, v in enumerate(reversed(cnpj_number)))
        digit = 11 - value % 11
        cnpj_number.append(digit if digit < 10 else 0)
    return re.sub(r'(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})',
                  '\\1.\\2.\\3/\\4-\\5',
                  "".join(str(x) for x in cnpj_number))


def generate_dummy_users(number_of_users: int = 1) -> dict[str, list]:
    """
    Generates dummy users with random names, CNPJs, and email addresses.

    This function generates a specified number of dummy users, each with a random name, CNPJ, and email address. The user data is returned in a dictionary format.

    :param number_of_users: The number of dummy users to generate. Defaults to 1.
    :type number_of_users: int
    :return: A dictionary containing three lists:
        - user_name_list: A list of generated user names.
        - user_cnpj_list: A list of generated CNPJs.
        - user_email_address_list: A list of generated email addresses.
    :rtype: dict[str, list]
    """
    users_dict = {'user_name_list': [],
                  'user_cnpj_list': [],
                  'user_email_address_list': []}
    for _ in range(number_of_users):
        number_of_characters = random.randrange(10, 20, 1)
        user_name = ''.join(random.choices(string.ascii_lowercase, k=number_of_characters))
        users_dict['user_name_list'].append(user_name)
        users_dict['user_cnpj_list'].append(_generate_cnpj())
        users_dict['user_email_address_list'].append(f"contato@{user_name[:5]}.com")

    return users_dict


def generate_dummy_blocks(owner_uids_list: list[str]) -> dict[str, list]:
    """
    Generates dummy blocks with random mining data, properties, and unique identifiers.

    This function generates a block of data for each owner UID provided in the list. Each block contains
    random mining data, properties, a code, and a hash. The data is returned in a dictionary format.

    :param owner_uids_list: A list of owner UIDs for which the blocks will be generated.
    :type owner_uids_list: list[str]
    :return: A dictionary containing five lists:
        - mining_data_list: A list of dictionaries with random mining data.
        - code_list: A list of generated codes.
        - properties_list: A list of dictionaries with random properties.
        - hash_list: A list of generated hashes.
        - owners_uid_list: The list of provided owner UIDs.
    :rtype: dict[str, list]
    """
    blocks_dict = {'mining_data_list': [],
                   'code_list': [],
                   'properties_list': [],
                   'hash_list': [],
                   'owners_uid_list': owner_uids_list}
    for _ in range(len(owner_uids_list)):
        number_of_characters = random.randrange(10, 15, 1)
        blocks_dict['mining_data_list'].append(
            {'company': ''.join(random.choices(string.ascii_lowercase, k=number_of_characters)),
             'mining_site': ''.join(random.choices(string.ascii_lowercase, k=number_of_characters)),
             'mining_date': ''.join(random.choices(string.ascii_lowercase, k=10))})
        blocks_dict['properties_list'].append(
            {'material': ''.join(random.choices(string.ascii_lowercase, k=number_of_characters)),
             'dimensions': f"{random.randrange(100, 300, 1) / 100}, "
                           f"{random.randrange(100, 300, 1) / 100}, "
                           f"{random.randrange(100, 300, 1) / 100}",
             'weight': f"{random.randrange(2000, 7000, 1)}"})
        blocks_dict['code_list'].append(''.join(random.choices(string.ascii_lowercase, k=10)))
        blocks_dict['hash_list'].append(''.join(random.choices((string.ascii_letters + string.digits), k=42)))

    return blocks_dict


def generate_dummy_transfers(block_uids_list: list[str], new_owner_uids_list: list[str]):
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
    transfer_data = {'ornamental_block_uid_list': block_uids_list,
                     'new_owner_uid_list': new_owner_uids_list,
                     'invoice_number_list': []}
    for _ in block_uids_list:
        transfer_data['invoice_number_list'].append(''.join(random.choices(string.digits, k=10)))
    return transfer_data


def run(step_by_step: bool = True) -> None:
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

    def _print_description(msg_: str):
        msg_ = ' ' + msg_ + ' '
        print(f"\n{msg_:*^{SCREEN_LENGTH}}\n")

    _print_description('Importing scmanager package')
    print(f" >>> from scmanager.admin_tools import create_config_file\n"
          f"     from scmanager import SCManager")

    Path("scm_config/examples").mkdir(parents=True, exist_ok=True)
    CONFIG_FILE = f"cfg_example_{str(random.randrange(1, 999))}.json"
    _print_description('Creating a config file and deploying a smart contract')
    print(f" >>> create_config_file(file_name=\'examples/{CONFIG_FILE}\')")
    create_config_file(file_name=f"examples/{CONFIG_FILE}")

    if step_by_step:
        input('Press ENTER to continue...\n')

    _print_description('Instantiating an SCManager object')
    print(f" >>> scm = SCManager(config_file=\'examples/{CONFIG_FILE}\', persist=1, show=True)")
    scm = SCManager(config_file=f"examples/{CONFIG_FILE}", persist=1, show=True)

    if step_by_step:
        input('Press ENTER to continue...\n')

    _print_description('Extracting all data from the smart contract')
    print(" >>> scm.get_contract_data()")
    pprint(scm.get_contract_data())

    if step_by_step:
        input('Press ENTER to continue...\n')

    _print_description('Registering 3 users')
    users = generate_dummy_users(3)
    print(f" >>> scm.add_new_users(user_name_list=[\'{users['user_name_list'][0]}\', "
          f"\'{users['user_name_list'][1]}\', \'{users['user_name_list'][2]}\'],\n"
          f"\t\t\t\t\t   user_cnpj_list=[\'{users['user_cnpj_list'][0]}\', "
          f"\'{users['user_cnpj_list'][1]}\', \'{users['user_cnpj_list'][2]}\'],\n"
          f"\t\t\t\t\t   user_email_address_list=[\'{users['user_email_address_list'][0]}\', "
          f"\'{users['user_email_address_list'][1]}\', \'{users['user_email_address_list'][2]}\'])")
    pprint(scm.add_new_users(**users))

    if step_by_step:
        input('Press ENTER to continue...\n')

    _print_description('Getting the users uid list')
    print(f" >>> scm.get_user_uids_list()")
    users_uid = scm.get_user_uids_list()
    pprint(users_uid)

    if step_by_step:
        input('Press ENTER to continue...\n')

    _print_description('Adding 4 ornamental blocks to the first user')
    blocks = generate_dummy_blocks([users_uid[0]] * 4)
    print(f" >>> scm.add_new_ornamental_blocks(mining_data_list=[{json.dumps(blocks['mining_data_list'][0])},\n"
          f"\t\t\t\t\t\t\t\t\t\t\t\t\t {json.dumps(blocks['mining_data_list'][1])},\n"
          f"\t\t\t\t\t\t\t\t\t\t\t\t\t {json.dumps(blocks['mining_data_list'][2])},\n"
          f"\t\t\t\t\t\t\t\t\t\t\t\t\t {json.dumps(blocks['mining_data_list'][3])}],\n"
          f"\t\t\t\t\t\t\t\t   code_list={json.dumps(blocks['code_list'])},\n"
          f"\t\t\t\t\t\t\t\t   properties_list=[{json.dumps(blocks['properties_list'][0])},\n"
          f"\t\t\t\t\t\t\t\t\t\t\t\t\t {json.dumps(blocks['properties_list'][1])},\n"
          f"\t\t\t\t\t\t\t\t\t\t\t\t\t {json.dumps(blocks['properties_list'][2])},\n"
          f"\t\t\t\t\t\t\t\t\t\t\t\t\t {json.dumps(blocks['properties_list'][3])}],\n"
          f"\t\t\t\t\t\t\t\t   hash_list={json.dumps(blocks['hash_list'])},\n"
          f"\t\t\t\t\t\t\t\t   owners_uid_list={json.dumps(blocks['owners_uid_list'])})")
    pprint(scm.add_new_ornamental_blocks(**blocks))

    if step_by_step:
        input('Press ENTER to continue...\n')

    _print_description('Getting the ornamental blocks uid list')
    print(f" >>> scm.get_ornamental_block_uids_list()")
    blocks_uids = scm.get_ornamental_block_uids_list()
    pprint(blocks_uids)

    if step_by_step:
        input('Press ENTER to continue...\n')

    _print_description('Extracting data from the first user')
    print(f" >>> scm.get_user_data(\'{users_uid[0]}\')")
    pprint(scm.get_user_data(users_uid[0]))

    if step_by_step:
        input('Press ENTER to continue...\n')

    _print_description('Transfering 1 ornamental block to the second and third users')
    transfers = generate_dummy_transfers(blocks_uids[1:3], users_uid[1:])
    print(f" >>> scm.transfer_ornamental_blocks(ornamental_block_uid_list="
          f"{json.dumps(transfers['ornamental_block_uid_list'])}, \n"
          f"\t\t\t\t\t\t\t\t\tnew_owner_uid_list={json.dumps(transfers['new_owner_uid_list'])}, \n"
          f"\t\t\t\t\t\t\t\t\tinvoice_number_list={json.dumps(transfers['invoice_number_list'])})")
    pprint(scm.transfer_ornamental_blocks(**transfers))

    if step_by_step:
        input('Press ENTER to continue...\n')

    _print_description('Extracting data from the second user')
    print(f" >>> scm.get_user_data(\'{users_uid[1]}\')")
    pprint(scm.get_user_data(users_uid[1]))

    if step_by_step:
        input('Press ENTER to continue...\n')

    _print_description('Extracting data from the third user')
    print(f" >>> scm.get_user_data(\'{users_uid[2]}\')")
    pprint(scm.get_user_data(users_uid[2]))

    if step_by_step:
        input('Press ENTER to continue...\n')

    _print_description('Deactivating 1 ornamental block from the first user')
    print(f" >>> scm.deactivate_ornamental_blocks([\'{blocks_uids[-1]}\'])")
    pprint(scm.deactivate_ornamental_blocks([blocks_uids[-1]]))

    if step_by_step:
        input('Press ENTER to continue...\n')

    _print_description('Extracting data from the first user')
    print(f" >>> scm.get_user_data(\'{users_uid[0]}\')")
    pprint(scm.get_user_data(users_uid[0]))

    if step_by_step:
        input('Press ENTER to continue...\n')

    _print_description('Extracting data from the deactivated ornamental block')
    print(f" >>> scm.get_ornamental_block_data(\'{blocks_uids[-1]}\')")
    pprint(scm.get_ornamental_block_data(blocks_uids[-1]))

    if step_by_step:
        input('Press ENTER to continue...\n')

    _print_description('Getting the inactive ornamental block uids list')
    print(f" >>> scm.get_inactive_ornamental_block_uids_list()")
    pprint(scm.get_inactive_ornamental_block_uids_list())

    if step_by_step:
        input('Press ENTER to continue...\n')

    _print_description('Extracting all data from the smart contract')
    print(" >>> scm.get_contract_data()")
    pprint(scm.get_contract_data())

    print('End of the example.')
