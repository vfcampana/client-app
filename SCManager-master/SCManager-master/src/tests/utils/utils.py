from datetime import datetime
from functools import wraps
from unittest import mock
from web3 import Web3
import builtins
import requests
import winsound
import shutil
import json
import time
import os

SCREEN_LENGTH = shutil.get_terminal_size()[0]


def decorator_with_args(decorator_to_enhance):
    """
    Enhances a decorator with arguments.

    This function enhances a decorator to accept arguments. It creates a new decorator that accepts
    only a function but keeps the passed arguments from the maker.

    Args:
        decorator_to_enhance: The decorator to be enhanced.

    Returns:
        The enhanced decorator.
    """

    def decorator_maker(*args, **kwargs):
        # We create on the fly a decorator that accepts only a function
        # but keeps the passed arguments from the maker.
        def decorator_wrapper(func):
            # We return the result of the original decorator, which, after all,
            # IS JUST AN ORDINARY FUNCTION (which returns a function).
            # Only pitfall: the decorator must have this specific signature, or it won't work:
            return decorator_to_enhance(func, *args, **kwargs)

        return decorator_wrapper

    return decorator_maker


@decorator_with_args
def enclosure_prints(func, file: str, class_name: str):

    @wraps(func)
    def wrapper(self,
                *args,
                **kwargs):
        print(f"\n{'-' * SCREEN_LENGTH}")
        returned = func(self, *args, **kwargs)
        file_name = file.rsplit('\\', 1)[-1]
        print(f"{'-' * SCREEN_LENGTH}")
        print(f"src\\tests\\{file_name}::{class_name}::{func.__name__} ", end='')
        return returned

    return wrapper


def check_internet_status() -> bool:
    try:
        response = requests.get('http://www.google.com', timeout=2)
        return True if response.status_code == 200 else False
    except requests.ConnectionError:  # pragma: no cover
        return False


@decorator_with_args
def only_online(func, timeout: int = 20):
    @wraps(func)
    def wrapper(self,
                *args,
                **kwargs):
        if not check_internet_status():
            msg = ' Conecte o seu dispositivo à internet: '
            wide = shutil.get_terminal_size()[0]
            print('\n', end='')
            for _ in range(0, timeout):
                remaining = f"{timeout - _: <2}"
                print(f"{msg + remaining + ' ':!^{wide}}", end='\r')
                time.sleep(1)
                if check_internet_status():
                    print(f"{' Conectado ':!^{wide}}", end='\r')
                    time.sleep(1)
                    break
            print(f"{' ' * wide}", end='\r')
        return func(self, *args, **kwargs)

    return wrapper


@only_online()
def calc_cost(self, previous: bool = False, test: str = 'All'):
    endpoint = str(os.getenv('ETHEREUM_ENDPOINT'))
    blockchain = Web3(Web3.HTTPProvider(endpoint_uri=endpoint, request_kwargs={'timeout': 20}))
    main_balance = float(blockchain.from_wei(
        blockchain.eth.get_balance('0xcEB8dDd79E5C794c4CA8058B0f7fF8876533F168'), 'ether'))
    test_balance = float(blockchain.from_wei(
        blockchain.eth.get_balance('0x40212Ac083FEc30E79439A84d8e30aa0D573FE38'), 'ether'))
    testing_costs_file = 'scm_config/tests/testing_costs_log.json'
    costs = []
    if testing_costs_file.split('/')[-1] in os.listdir('scm_config/tests'):
        with open(testing_costs_file, 'r', encoding="utf-8") as file:
            costs = json.load(file)
    if previous:
        if (costs
                and costs[-1]['main account']['new balance'] == -1
                and costs[-1]['test account']['new balance'] == -1):  # pragma: no cover
            costs.pop()
        dic = {'datetime': datetime.now().strftime("%Y/%m/%d, %H:%M"),
               'test': test,
               'duration': ['starting time', time.perf_counter()],
               'main account': {'cost': ['starting cost', main_balance],
                                'new balance': -1},
               'test account': {'cost': ['starting cost', test_balance],
                                'new balance': -1}}
        costs.append(dic)
        print()
        msg = f"Tests starting at: {dic['datetime']}"
        print(f"{msg: ^{SCREEN_LENGTH}}")
        msg = f"Previous main account balance: {round(costs[-1]['main account']['cost'][1], 6)} eth"
        print(f"{msg: ^{SCREEN_LENGTH}}")
        msg = f"Previous test account balance: {round(costs[-1]['test account']['cost'][1], 6)} eth"
        print(f"{msg: ^{SCREEN_LENGTH}}")
        with open(testing_costs_file, 'w', encoding="utf-8") as file:
            json.dump(costs, file, ensure_ascii=False, indent=4)
        return
    costs[-1]['main account']['cost'] = costs[-1]['main account']['cost'][1] - main_balance
    costs[-1]['test account']['cost'] = costs[-1]['test account']['cost'][1] - test_balance
    costs[-1]['duration'] = time.strftime('%Hh %Mm %Ss', time.gmtime(time.perf_counter() - costs[-1]['duration'][1]))
    costs[-1]['main account']['new balance'] = main_balance
    costs[-1]['test account']['new balance'] = test_balance
    print(f"\r{' ' * SCREEN_LENGTH}")
    msg = f"Total testing costs for main account: {round(costs[-1]['main account']['cost'], 6)} eth"
    print(f"{msg: ^{SCREEN_LENGTH}}")
    msg = f"Current balance of main account: {round(main_balance, 6)} eth"
    print(f"{msg: ^{SCREEN_LENGTH}}")
    msg = f"Total testing costs for test account: {round(costs[-1]['test account']['cost'], 6)} eth"
    print(f"{msg: ^{SCREEN_LENGTH}}")
    msg = f"Current balance of test account: {round(test_balance, 6)} eth"
    print(f"{msg: ^{SCREEN_LENGTH}}")
    msg = f"Total Duration of the tests: {costs[-1]['duration']}"
    print(f"{msg: ^{SCREEN_LENGTH}}")
    if costs[-1]['main account']['cost'] == 0.0 and costs[-1]['test account']['cost'] == 0.0:  # pragma: no cover
        costs.pop()
    with open(testing_costs_file, 'w', encoding="utf-8") as file:
        json.dump(costs, file, ensure_ascii=False, indent=4)
    for _ in range(2):
        winsound.Beep(frequency=1320, duration=300)
        time.sleep(0.3)
    winsound.Beep(frequency=1320, duration=1000)


@decorator_with_args
def print_class_test_name(func, file: str):
    @wraps(func)
    def wrapper(self,
                *args,
                **kwargs):
        filename = file.rsplit('\\', 1)[-1]
        full_name = f"src\\tests\\{filename}::{self.__class__.__name__}::{func.__name__} "
        print(f"\r{' '*(len(full_name)+20)}", end='\n')
        print(f"{self.__class__.__name__}:\n")
        print(full_name, end='')
        return func(self, *args, **kwargs)

    return wrapper


def ignore_requests(function, kwargs, ignore=False, key=''):
    if ignore:
        with mock.patch.object(builtins, 'input', lambda _: key):
            input('')
            return function(**kwargs)
    return function(**kwargs)
