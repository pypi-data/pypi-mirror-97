# Encrypti0n
Author(s):  Daan van den Bergh.<br>
Copyright:  © 2020 Daan van den Bergh All Rights Reserved.<br>
Supported Operating Systems: macos & linux.<br>
<br>
<br>
<p align="center">
  <img src="https://raw.githubusercontent.com/vandenberghinc/public-storage/master/vandenberghinc/icon/icon.png" alt="Bergh-Encryption" width="50"/>
</p>


## Installation:

	pip3 install encrypti0n --upgrade && python3 -c "import encrypti0n" --create-alias encrypti0n

## Description.
Includes asymmetrical AES encryption.

## CLI:
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

## Python Examples.
Import the encryption package.
```python
# import the encryption object.
import encrypti0n
```

### The AES Database class.
All files remain encrypted at all times. <br>
Supports dict, list, str, int, float format data. <br>
Designed for dict formats.
```python

# initialize.
aes = encrypti0n.aes.AES(passphrase="SomePassphrase12345!?")
database = encrypti0n.aes.Database(
	path="/tmp/database.enc",
	aes=aes,)

# activate the database.
response = database.activate()

# check data, dict or list.
response = database.check("users/vandenberghinc", {
	"Hello":"World"
})

# load data.
response = database.load("users/vandenberghinc")
content = response.content

# save data.
content.format # dict
content["Hello"] = "World!"
response = database.save(content)

# int & float data.
response = database.check("someint", 1500)
content = response.content
content.format # int
content.content = 1501
response = database.save(content)

# string data.
response = database.check("somestring", "Hello World")
content = response.content
content.format # str
content.content = "Hello World!"
response = database.save(content)


```

### The AsymmetricAES class.
Initialize the encryption class (Leave the passphrase None if you require no passphrase).
```python
# initialize the encryption class.
encryption = encrypti0n.aes.AsymmetricAES(
	private_key='mykey/private_key',
	public_key='mykey/public_key',
	passphrase='MyPassphrase123!')
```

### The AES class.
Initialize the encryption class (Leave the passphrase None if you require no passphrase).
```python
# initialize the encryption class.
encryption = encrypti0n.aes.AES(
	passphrase='MyPassphrase123!')
```

### The RSA class.
Initialize the encryption class (Leave the passphrase None if you require no passphrase).
```python
# initialize the encryption class.
encryption = encrypti0n.rsa.RSA(
	directory='mykey/',
	passphrase='MyPassphrase123!')
```

Generating the keys.
```python
# generate the key pair.
response = encryption.generate_keys()
```

Load the generated keys before encrypting / decrypting.
```python
# load the key pair.
response = encryption.load_keys()
```

Edit the key's passphrase.
```python
# edit the key's passphrase.
response = encryption.edit_passphrase(passphrase="NewPassphrase123!")

```

Encrypting & decrypting files and strings.
```python

# encrypting & decrypting a file.
response = encryption.encrypt_file('file.txt', layers=1)
response = encryption.decrypt_file('file.txt', layers=1)

# encrypting & decrypting a string.
response = encryption.encrypt_string('hello world!', layers=1)
response = encryption.decrypt_string(response['encrypted'], layers=1)

```

Encrypting & decrypting directories.
```python

# encrypting & decrypting a directory.

# option 1: 
# (recursively encrypt each file in the directory).
response = encryption.encrypt_directory('directory/', recursive=True, layers=1)
response = encryption.decrypt_directory('directory/', recursive=True, layers=1)

# option 2:
# (create an encrypted zip of the directory and remove the directory).
response = encryption.encrypt_directory('directory/', layers=1)
response = encryption.decrypt_directory('directory/', layers=1)
```

### The EncryptedDictionary class.
The dictionary remains encrypted on file system while being decrypted in the local memory.
```python
# initialize the encrypted dictionary.
dictionary = encrypti0n.rsa.EncryptedDictionary(
	# the file path.
	path="encrypted-dict.json", 
	# the dictionary.
	dictionary=None, 
	# specify default to check & create the dict.
	default={
		"hello":"world!"
	}, 
	# the key's path.
	key="mykey/",
	# the key's passphrase.
	passphrase='MyPassphrase123!',
	# the encryption layers.
	layers=1,)

# initialize the encryption.
response = dictionary.initialize()

# load the dict.
response = dictionary.load()
print(dictionary.dictionary)

# save the dict.
response = dictionary.save({"hello":"world!"})
# equal to.
dictionary.dictionary = {"hello":"world!"}
response = dictionary.save()

# check the dict.
response = dictionary.check(
	save=True,
	dictionary={
		"hello":"world!"
		"foo":"bar",
	})
```

### Response Object.
When a function completed successfully, the "success" variable will be "True". When an error has occured the "error" variable will not be "None". The function returnables will also be included in the response.

	{
		"success":False,
		"message":None,
		"error":None,
		"...":"...",
	}