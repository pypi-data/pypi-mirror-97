#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
import syst3m
from fil3s import *
from r3sponse import r3sponse
import getpass

# lib imports.
from encrypti0n.classes import aes

# the agent object class.
class Agent(syst3m.objects.Traceback):
	def __init__(self,
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
		traceback="encryption.Agent",
	):

		# traceback.
		syst3m.objects.Traceback.__init__(self, traceback=traceback)

		# check instances.
		if not isinstance(config, Dictionary):
			raise ValueError(f"{self.__traceback__()}: parameter [config] requires to be be a [Dictionary], not [{config.__class__.__name__}].")
		if not isinstance(database, Directory):
			raise ValueError(f"{self.__traceback__()}: parameter [database] requires to be be a [Directory], not [{database.__class__.__name__}].")
		if database.fp == False or database.fp == None:
			raise ValueError(f"{self.__traceback__()}: parameter [database.path] requires to be be a [FilePath], not [NoneType] (Pass a initialized dictionary with a file path).")

		# init.
		self.id = id
		self.host = host
		self.port = port
		self.config = config
		self.passphrase = passphrase
		self.interactive = interactive
		self.db_path = database

		# vars.
		self._activated = False

		# check cofig.
		self.config.check(save=True, default={
			"encryption": {
				"public_key":None,
				"private_key":None,
			}
		})
		# objects.
		self.webserver = syst3m.cache.WebServer(
			id=self.id,
			host=self.host,
			port=self.port,
			path=Files.join(self.db_path, ".cache"), # only used for tokens, rest is stored in python memory only.
		)
		self.aes = self.encryption = aes.AsymmetricAES(
			public_key=self.config["encryption"]["public_key"],
			private_key=self.config["encryption"]["private_key"],
			passphrase=self.passphrase,
			memory=True,)
		self.db = self.database = aes.Database(path=str(self.db_path), aes=self.encryption)

		#

	# generate encryption.
	def generate(self,
		# the passphrase (optional to prompt) (str).
		passphrase=None,
		# the verify passphrase (optional).
		verify_passphrase=None,
		# interactive (optional).
		interactive=None
	):

		# checks.
		if passphrase == None: passphrase = self.passphrase
		if interactive == None: interactive = self.interactive
		if passphrase == None:
			if not interactive:
				return r3sponse.error(self.__traceback__(function="generate")+": Define parameter [passphrase].")
			else:
				passphrase = getpass.getpass("Enter the passphrase of the ssht00ls encryption:")
		elif len(passphrase) < 8: 
			return r3sponse.error("The passphrase must contain at least 8 characters.")
		elif passphrase.lower() == passphrase: 
			return r3sponse.error("The passphrase must contain capital characters.")
		elif (interactive and passphrase != getpass.getpass("Enter the same passphrase:")) or (verify_passphrase != None and passphrase != verify_passphrase): 
			return r3sponse.error("The passphrase must contain at least 8 characters.")

		# check webserver.
		if not self.webserver.running:
			if not interactive:
				return r3sponse.error(f"{self.__traceback__()}: The webserver is not running.")
			else:
				if syst3m.defaults.options.log_level >= 1: r3sponse.log(f"{ALIAS}: forking {self.id} webserver.")
				response = self.webserver.fork()
				if not response.success: return response

		# generate.
		self.encryption.rsa.passphrase = passphrase
		response = self.encryption.generate_keys()
		if not response["success"]: 
			return r3sponse.error(f"Encoutered an error while generating the master encryption key: {response['error']}")
		self.passphrase = passphrase
		self.encryption.rsa.private_key = response.private_key
		self.encryption.rsa.public_key = response.public_key
		try: self.config["encryption"]
		except KeyError: self.config["encryption"] = {}
		self.config["encryption"]["public_key"] = self.encryption.rsa.public_key
		self.config["encryption"]["private_key"] = self.encryption.rsa.private_key
		self.config.save()
		response = self.encryption.load_keys()
		if not response["success"]: 
			return r3sponse.error(f"Encoutered an error while activating the ssht00ls encryption: {response['error']}")

		# cache.
		response = self.webserver.set(group="passphrases", id="master", data=passphrase)
		if not response["success"]: 
			return r3sponse.error(f"Encoutered an error while caching the passphrase (#1): {response['error']}")

		# database.
		self.db = aes.Database(path=str(self.db_path), aes=self.encryption)
		response = self.db.activate()
		if not response["success"]: 
			return r3sponse.error(f"Encoutered an error while activating the encrypted cache: {response['error']}")

		# hander.
		return r3sponse.success("Successfully generated the encryption.")

		#

	# activate encryption.
	def activate(self,
		# the key's passphrase (optional to retrieve from webserver) (str).
		passphrase=None,
		# interactive (optional) 
		interactive=None,
	):
		if passphrase == None: passphrase = self.passphrase
		if interactive == None: interactive = self.interactive
		new = False
		if passphrase in [False, None, "", "null", "None", "none"]:
			
			# check webserver.
			if not self.webserver.running:
				if not interactive:
					return r3sponse.error(f"{self.__traceback__()}: The webserver is not running.")
				else:
					if syst3m.defaults.options.log_level >= 1: r3sponse.log(f"{ALIAS}: forking {self.id} webserver.")
					response = self.webserver.fork()
					if not response.success: return response

			# get pass.
			response, passphrase = self.webserver.get(group="passphrases", id="master"), None
			if not response.success and "There is no data cached for" not in response["error"]: return response
			elif response["success"]: passphrase = response["data"]
			if passphrase in [False, None, "", "null", "None", "none"]:
				if not interactive:
					return r3sponse.error(self.__traceback__(function="activate")+": Define parameter [passphrase].")
				else:
					new = True
					passphrase = getpass.getpass("Enter the passphrase of the ssht00ls encryption:")

		# activate.
		self.encryption.rsa.passphrase = passphrase
		response = self.encryption.load_keys()
		if not response["success"]: 
			return r3sponse.error(f"Encoutered an error while activating the ssht00ls encryption: {response['error']}")
		self.passphrase = passphrase
		self.db.aes.rsa.passphrase = passphrase
		response = self.db.activate()
		if not response["success"]: 
			return r3sponse.error(f"Encoutered an error while activating the encrypted cache: {response['error']}")

		# chache.
		if new:
			response = self.webserver.set(group="passphrases", id="master", data=passphrase)
			if not response["success"]: 
				return r3sponse.error(f"Encoutered an error while caching the passphrase (#2): {response['error']}")

		# handler.
		return r3sponse.success("Successfully activated the encryption.")

		#

	# copy functions (only these!).
	def encrypt(self, string, decode=False):
		self.encryption.encrypt(string, decode=decode)
		#
	def decrypt(self, string, decode=False):
		self.encryption.decrypt(string, decode=decode)
		#

	# properties.
	@property
	def activated(self):
		return self.encryption.activated and self.db.aes.activated
		#
	@property
	def public_key_activated(self):
		return self.encryption.public_key_activated and self.db.aes.public_key_activated
		#
	@property
	def private_key_activated(self):
		return self.encryption.private_key_activated and self.db.aes.private_key_activated
		#
	@property
	def generated(self):
		return self.encryption.rsa.private_key != None and self.encryption.rsa.public_key != None
		#

	# repr.
	def __repr__(self):
		return f"<{self.__traceback__()} (activated: {self.activated}) (generated: {self.generated}) >"
		#

	#
	
