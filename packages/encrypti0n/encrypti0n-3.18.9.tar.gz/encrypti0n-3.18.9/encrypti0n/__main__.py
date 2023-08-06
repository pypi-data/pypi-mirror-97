#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
import os, sys, syst3m ; sys.path.insert(1, syst3m.defaults.source_path(__file__, back=2))
from encrypti0n.classes.config import *
from encrypti0n.classes import utils
#from encrypti0n.classes.rsa import RSA,EncryptedDictionary
from encrypti0n.classes.aes import AsymmetricAES


# the cli object class.
class CLI(cl1.CLI):
	def __init__(self):
		
		# cli.
		cl1.CLI.__init__(self,
			modes={
				"--encrypt /path/to/input /path/to/output [optional: --remove]":"Encrypt the provided file path.",
				"--decrypt /path/to/input /path/to/output [optional: --remove]":"Decrypt the provided file path.",
				"--encrypt-env . [optional: --remove]":"Encrypt the specified enviroment (automatically fills: --key ./key --input ./data/ --output ./data.enc.zip).",
				"--decrypt-env . [optional: --remove]":"Decrypt the specified enviroment (automatically fills: --key ./key --input ./data.enc.zip --output ./data/).",
				"--generate-keys":"Generate a key pair.",
				"--generate-passphrase [optional: --length 32]":"Generate a passphrase.",
				"--generate-aes [optional: --length 64]":"Generate an aes passphrase.",
				"-h / --help":"Show the documentation.",
			},
			options={
				"--remove":"Remove the input file.",
				"--key /path/to/directory/":"Specify the path to the key's directory.",
				"--public-key /path/to/directory/public_key":"Specify the path to the public key.",
				"--private-key /path/to/directory/private_key":"Specify the path to the private key.",
				"-p / --passphrase 'Passphrase123!'":"Specify the key's passphrase.",
			},
			executable=__file__,
			alias=ALIAS,)

		#
	def start(self):
		
		# check arguments.
		self.arguments.check(json=syst3m.defaults.options.json)

		# help.
		if self.arguments.present(['-h', '--help']):
			self.docs(success=True, json=syst3m.defaults.options.json)

		# version.
		elif self.arguments.present(['--version']):
			self.stop(message=f"{ALIAS} version:"+Files.load(f"{SOURCE_PATH}/.version.py").replace("\n",""), json=syst3m.defaults.options.json)

		# encrypt.
		elif self.arguments.present('--encrypt'):
			input = self.arguments.get('--encrypt', index=1, json=syst3m.defaults.options.json)
			output = self.arguments.get('--encrypt', index=2, json=syst3m.defaults.options.json)
			encryption = self.get_encryption(prompt_passphrase=False)
			response = encryption.load_public_key()
			r3sponse.log(response=response, json=syst3m.defaults.options.json)
			if not response.success: sys.exit(1)
			if os.path.isdir(input): 
				response = encryption.encrypt_directory(input=input, output=output, remove=self.arguments.present("--remove"))
			else: 
				response = encryption.encrypt_file(input=input, output=output, remove=self.arguments.present("--remove"))
			self.stop(response=response, json=syst3m.defaults.options.json)

		# decrypt.
		elif self.arguments.present('--decrypt'):
			input = self.arguments.get('--decrypt', index=1, json=syst3m.defaults.options.json)
			output = self.arguments.get('--decrypt', index=2, json=syst3m.defaults.options.json)
			encryption = self.get_encryption()
			response = encryption.load_private_key()
			r3sponse.log(response=response, json=syst3m.defaults.options.json)
			if not response.success: sys.exit(1)
			if os.path.isdir(input) or (".enc.zip" in input and ".enc.zip" not in output): 
				response = encryption.decrypt_directory(input=input, output=output, remove=self.arguments.present("--remove"))
			else: 
				response = encryption.decrypt_file(input=input, output=output, remove=self.arguments.present("--remove"))
			self.stop(response=response, json=syst3m.defaults.options.json)

		# encrypt env.
		elif self.arguments.present('--encrypt-env'):
			env = self.arguments.get('--encrypt-env', json=syst3m.defaults.options.json)
			key = f"{env}/key/".replace("//","/").replace("//","/").replace("//","/")
			input = f"{env}/data/".replace("//","/").replace("//","/").replace("//","/")
			output = f"{env}/data.enc.zip".replace("//","/").replace("//","/").replace("//","/")
			encryption = self.get_encryption(prompt_passphrase=False, key=key)
			response = encryption.load_public_key()
			r3sponse.log(response=response, json=syst3m.defaults.options.json)
			if not response.success: sys.exit(1)
			response = encryption.encrypt_directory(input=input, output=output, remove=self.arguments.present("--remove"))
			r3sponse.log(response=response)
			self.stop(response=response, json=syst3m.defaults.options.json)

		# decrypt env.
		elif self.arguments.present('--decrypt-env'):
			env = self.arguments.get('--decrypt-env')
			key = f"{env}/key/".replace("//","/").replace("//","/").replace("//","/")
			input = f"{env}/data.enc.zip".replace("//","/").replace("//","/").replace("//","/")
			output = f"{env}/data/".replace("//","/").replace("//","/").replace("//","/")
			encryption = self.get_encryption(key=key)
			response = encryption.load_private_key()
			r3sponse.log(response=response, json=syst3m.defaults.options.json)
			if not response.success: sys.exit(1)
			response = encryption.decrypt_directory(input=input, output=output, remove=self.arguments.present("--remove"))
			self.stop(response=response, json=syst3m.defaults.options.json)

		# generate-keys.
		elif self.arguments.present('--generate-keys'):
			encryption = self.get_encryption(check_passphrase=True)
			response = encryption.generate_keys()
			self.stop(response=response, json=syst3m.defaults.options.json)

		# generate-aes.
		elif self.arguments.present('--generate-aes'):
			self.stop(message=f"Generated AES Passphrase: {utils.__generate__(length=int(self.arguments.get('--length', required=False, default=64)), capitalize=True, digits=True)}", json=syst3m.defaults.options.json)

		# generate passphrase.
		elif self.arguments.present('--generate-passphrase'):
			self.stop(message=f"Generated passphrase: {String('').generate(length=length, capitalize=True, digits=True)}", json=syst3m.defaults.options.json)

		# invalid.
		else: self.invalid(json=syst3m.defaults.options.json)

		#
	def get_encryption(self, prompt_passphrase=True, check_passphrase=False, key=None):
		# key.
		public_key = self.arguments.get('--public-key', required=False)
		private_key = self.arguments.get('--private-key', required=False)
		if public_key == None and private_key == None:
			if key == None: key = self.arguments.get('--key', required=True, json=syst3m.defaults.options.json)
			public_key = f"{key}/public_key"
			private_key = f"{key}/private_key"
		# passphrase.
		passphrase = None
		if prompt_passphrase:
			passphrase = self.arguments.get('-p', required=False)
			if passphrase == None:
				passphrase = self.arguments.get('--passphrase', required=False)
			if passphrase == None:
				passphrase = utils.__prompt_password__("Enter the key's passphrase (leave blank to use no passphrase):")
				if check_passphrase and passphrase != utils.__prompt_password__("Enter the same passphrase:"):
					print("Error: passphrases do not match.")
					sys.exit(1)
			if passphrase in ["", "none", "null"]: passphrase = None
		# encryption.
		return AsymmetricAES(
			public_key=public_key,
			private_key=private_key,
			passphrase=passphrase,)
	
# main.
if __name__ == "__main__":
	cli = CLI()
	cli.start()
