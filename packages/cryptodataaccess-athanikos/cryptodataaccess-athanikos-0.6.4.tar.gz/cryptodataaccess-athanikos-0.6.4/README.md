

[![CircleCI](https://circleci.com/gh/athanikos/cryptodataaccess.svg?style=shield&circle-token=ecfbd9ba1187e20c781c6e467683e29e5418f915)](https://app.circleci.com/pipelines/github/athanikos/cryptodataaccess)



### Crypto data access  
Repositories for cryptomodel 
1. UsersRepository (user settings, notifications)
2. TransactionRepository (buy,sell,deposit) 
3. RatesRepository (exchange rates & symbol rates )

##### unit testing setup , set up keyring user name and pass for mongo db 
> import keyring 
> keyring.set_keyring(PlaintextKeyring())   
> from keyrings.alt.file import PlaintextKeyring    
> keyring.set_keyring(PlaintextKeyring())   
> keyring.set_password('CryptoUsersService', 'USERNAME', 'someusername') 
> keyring.set_password('cryptodataaccess', 'USERNAME', 'username') 
> keyring.set_password('cryptodataaccess', 'admin', 'password')

##### to package 
https://packaging.python.org/tutorials/packaging-projects/
rm -rf dist 
python3 -m build
python3 -m pip install --user --upgrade twine
modify version in setup.py  (increment by 1 )
python3 -m twine upload --skip-existing --repository pypi dist/*
python3 -m twine upload --repository pypi dist/*
