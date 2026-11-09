from setuptools import find_packages, setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='scmanager',
    version='0.4.0',
    description='A package that can interact with a smart contract',
    package_dir={'': 'src'},
    packages=find_packages(where='src', exclude=['tests']),
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='<Marcus Romano',
    author_email='msouza@mogai.com.br',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    install_requires=['eth-account==0.11.2',
                      'web3==6.20.0',
                      'python-dotenv==1.0.1',
                      'py-solc-x==2.0.3'],
    extras_require={},
    python_requires='>=3.11',
)
