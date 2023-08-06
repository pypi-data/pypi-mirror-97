# encrypti0n
Author(s):  Daan van den Bergh.<br>
Copyright:  © 2020 Daan van den Bergh All Rights Reserved.<br>
Supported Operating Systems: macos & linux.<br>
<br>
<br>
<p align="center">
  <img src="https://raw.githubusercontent.com/vandenberghinc/public-storage/master/vandenberghinc/icon/icon.png" alt="Bergh-Encryption" width="50"> 
</p>

## Table of content:
  * [Description](#description)
  * [Installation](#installation)
  * [CLI Usage](#cli-usage)
  * [Code Examples](#code-examples)

# Description:
Python & cli encryption toolset.

# Installation:
Install the package.

	pip3 install encrypti0n --upgrade && python3 -c "import encrypti0n" --create-alias encrypti0n

# CLI Usage:
	Usage: encrypti0n <mode> <options> 
	Modes:
	    --encrypt /path/to/input /path/to/output : Encrypt the provided file path.
	    --decrypt /path/to/input /path/to/output : Decrypt the provided file path.
	    --generate-keys : Generate a key pair.
	    --generate-passphrase --length 32 : Generate a passphrase.
	    -h / --help : Show the documentation.
	Options:
	    --remove : Remove the input file.
	    --key /path/to/directory/ : Specify the path to the key's directory.
	    --public-key /path/to/directory/public_key : Specify the path to the public key.
	    --private-key /path/to/directory/private_key : Specify the path to the private key.
	    -p / --passphrase 'Passphrase123!' : Specify the key's passphrase.
	Author: Daan van den Bergh. 
	Copyright: © Daan van den Bergh 2021. All rights reserved.
	Usage at own risk.

# Code Examples:

### Table of content:
- [__AES__](#aes)
  * [encrypt](#encrypt)
  * [decrypt](#decrypt)
  * [get_key](#get_key)
  * [generate_salt](#generate_salt)
- [__Agent__](#agent)
  * [generate](#generate)
  * [activate](#activate)
  * [encrypt](#encrypt-1)
  * [decrypt](#decrypt-1)
  * [activated](#properties)
- [__AsymmetricAES__](#asymmetricaes)
  * [generate_keys](#generate_keys)
  * [edit_passphrase](#edit_passphrase)
  * [load_keys](#load_keys)
  * [load_private_key](#load_private_key)
  * [load_public_key](#load_public_key)
  * [encrypt](#encrypt-2)
  * [decrypt](#decrypt-2)
  * [encrypt_file](#encrypt_file)
  * [decrypt_file](#decrypt_file)
  * [encrypt_directory](#encrypt_directory)
  * [decrypt_directory](#decrypt_directory)
  * [activated](#properties-1)
- [__Database__](#database)
  * [activate](#activate-1)
  * [check](#check)
  * [load](#load)
  * [save](#save)
  * [activated](#properties-2)
- [__RSA__](#rsa)
  * [generate_keys](#generate_keys-1)
  * [load_keys](#load_keys-1)
  * [load_public_key](#load_public_key-1)
  * [load_private_key](#load_private_key-1)
  * [edit_passphrase](#edit_passphrase-1)
  * [encrypt_string](#encrypt_string)
  * [encrypt_file](#encrypt_file-1)
  * [encrypt_directory](#encrypt_directory-1)
  * [decrypt_string](#decrypt_string)
  * [decrypt_file](#decrypt_file-1)
  * [decrypt_directory](#decrypt_directory-1)
  * [activated](#properties-3)

## AES:
The aes object class.
``` python 

# initialize the aes object class.
aes = AES(passphrase=None)

```

#### Functions:

##### encrypt:
``` python

# call aes.encrypt.
response = aes.encrypt(raw)

```
##### decrypt:
``` python

# call aes.decrypt.
response = aes.decrypt(enc)

```
##### get_key:
``` python

# call aes.get_key.
response = aes.get_key(salt=None)

```
##### generate_salt:
``` python

# call aes.generate_salt.
response = aes.generate_salt()

```

## Agent:
The agent object class.
``` python 

# initialize the agent object class.
agent = Agent(
    # the encryption & webserver's id.
    id="encrypti0n-agent",
    # the configuration file (Dictionary).
    config=Dictionary,
    # the path to the encrypted database.
    database=Directory,
    # the passphrase (optional to prompt) (str).
    passphrase=None,
    # the interactive mode (prompt for password) (bool).
    interactive=True,
    # the webserver's host.
    host="127.0.0.1",
    # the webserver's port.
    port=52379,
    # the object traceback.
    traceback="encryption.Agent", )

```

#### Functions:

##### generate:
``` python

# call agent.generate.
response = agent.generate(
    # the passphrase (optional to prompt) (str).
    passphrase=None,
    # the verify passphrase (optional).
    verify_passphrase=None,
    # interactive (optional).
    interactive=None )

```
##### activate:
``` python

# call agent.activate.
response = agent.activate(
    # the key's passphrase (optional to retrieve from webserver) (str).
    passphrase=None,
    # interactive (optional)
    interactive=None, )

```
##### encrypt:
``` python

# call agent.encrypt.
_ = agent.encrypt(string, decode=False)

```
##### decrypt:
``` python

# call agent.decrypt.
_ = agent.decrypt(string, decode=False)

```

#### Properties:
```python

# the activated property.
activated = agent.activated
```
```python

# the public key activated property.
public_key_activated = agent.public_key_activated
```
```python

# the private key activated property.
private_key_activated = agent.private_key_activated
```
```python

# the generated property.
generated = agent.generated
```

## AsymmetricAES:
The asymmetricaes object class.
``` python 

# initialize the asymmetricaes object class.
asymmetricaes = AsymmetricAES(
    # the public key (str).
    public_key=None,
    # the private key (str).
    private_key=None,
    # the key passphrase (str / null).
    passphrase=None,
    # enable memory when the keys are not saved.
    memory=False, )

```

#### Functions:

##### generate_keys:
``` python

# call asymmetricaes.generate_keys.
_ = asymmetricaes.generate_keys()

```
##### edit_passphrase:
``` python

# call asymmetricaes.edit_passphrase.
_ = asymmetricaes.edit_passphrase(passphrase=None)

```
##### load_keys:
``` python

# call asymmetricaes.load_keys.
_ = asymmetricaes.load_keys()

```
##### load_private_key:
``` python

# call asymmetricaes.load_private_key.
_ = asymmetricaes.load_private_key()

```
##### load_public_key:
``` python

# call asymmetricaes.load_public_key.
_ = asymmetricaes.load_public_key()

```
##### encrypt:
``` python

# call asymmetricaes.encrypt.
response = asymmetricaes.encrypt(string, decode=False)

```
##### decrypt:
``` python

# call asymmetricaes.decrypt.
response = asymmetricaes.decrypt(string, decode=False)

```
##### encrypt_file:
``` python

# call asymmetricaes.encrypt_file.
response = asymmetricaes.encrypt_file(input=None, output=None, remove=False, base64_encoding=False)

```
##### decrypt_file:
``` python

# call asymmetricaes.decrypt_file.
response = asymmetricaes.decrypt_file(input=None, output=None, remove=False, base64_encoding=False)

```
##### encrypt_directory:
``` python

# call asymmetricaes.encrypt_directory.
response = asymmetricaes.encrypt_directory(input=None, output=None, remove=False)

```
##### decrypt_directory:
``` python

# call asymmetricaes.decrypt_directory.
response = asymmetricaes.decrypt_directory(input=None, output=None, remove=False)

```

#### Properties:
```python

# the activated property.
activated = asymmetricaes.activated
```
```python

# the public key activated property.
public_key_activated = asymmetricaes.public_key_activated
```
```python

# the private key activated property.
private_key_activated = asymmetricaes.private_key_activated
```

## Database:
The database object class.
``` python 

# initialize the database object class.
database = Database(
    # the aes object class.
    aes=None,
    # the root path of the database.
    path=None, )

```

#### Functions:

##### activate:
``` python

# call database.activate.
response = database.activate(
    # the key;s passphrase (optional).
    passphrase=None, )

```
##### check:
``` python

# call database.check.
response = database.check(
    # the subpath of the content (! param number 1).
    path=None,
    # the default content data (! param number 2).
    default=None,
    # save the changes.
    save=True, )

```
##### load:
``` python

# call database.load.
response = database.load(
    # the subpath of the content (! param number 1).
    path=None,
    # the default data, specify to call database.check() automatically on the data object.
    default=None, )

```
##### save:
``` python

# call database.save.
response = database.save(
    # the content object (! param number 1).
    content=None, )

```

#### Properties:
```python

# the activated property.
activated = database.activated
```
```python

# the public key activated property.
public_key_activated = database.public_key_activated
```
```python

# the private key activated property.
private_key_activated = database.private_key_activated
```

## RSA:
The rsa object class.
``` python 

# initialize the rsa object class.
rsa = RSA(
    # option 1:
    #     the key directory.
    directory=None,
    # option 2:
    public_key=None,
    private_key=None,
    memory=False, # enable memory when the keys are not saved.
    # the key's passphrase (Leave None for no passphrase).
    passphrase=None, )

```

#### Functions:

##### generate_keys:
``` python

# call rsa.generate_keys.
response = rsa.generate_keys(log_level=0)

```
##### load_keys:
``` python

# call rsa.load_keys.
response = rsa.load_keys()

```
##### load_public_key:
``` python

# call rsa.load_public_key.
response = rsa.load_public_key()

```
##### load_private_key:
``` python

# call rsa.load_private_key.
response = rsa.load_private_key()

```
##### edit_passphrase:
``` python

# call rsa.edit_passphrase.
_ = rsa.edit_passphrase(passphrase=None)

```
##### encrypt_string:
``` python

# call rsa.encrypt_string.
response = rsa.encrypt_string(string, layers=1, decode=True)

```
##### encrypt_file:
``` python

# call rsa.encrypt_file.
response = rsa.encrypt_file(path, layers=1)

```
##### encrypt_directory:
``` python

# call rsa.encrypt_directory.
response = rsa.encrypt_directory(path, recursive=False, layers=1)

```
##### decrypt_string:
``` python

# call rsa.decrypt_string.
response = rsa.decrypt_string(string, layers=1, decode=True)

```
##### decrypt_file:
``` python

# call rsa.decrypt_file.
response = rsa.decrypt_file(path, layers=1)

```
##### decrypt_directory:
``` python

# call rsa.decrypt_directory.
response = rsa.decrypt_directory(path, recursive=False, layers=1)

```

#### Properties:
```python

# the activated property.
activated = rsa.activated
```
```python

# the private key activated property.
private_key_activated = rsa.private_key_activated
```
```python

# the public key activated property.
public_key_activated = rsa.public_key_activated
```

