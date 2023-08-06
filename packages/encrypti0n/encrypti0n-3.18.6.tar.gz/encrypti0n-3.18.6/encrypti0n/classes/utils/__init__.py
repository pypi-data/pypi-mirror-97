#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from encrypti0n.classes.config import * 
import os, sys, ast, json, pathlib, glob, string, getpass, subprocess

# clean url / path.
def __clean_url__(url, strip_first=True, strip_last=True, remove_double_slash=True):
	while True:
		if strip_last and url[len(url)-1] == "/": url = url[:-1]
		elif strip_first and url[0] == "/": url = url[1:]
		elif remove_double_slash and "//" in url: url = url.replace("//","/")
		else: break
	return url

# safely pormpt a password throug the terminal.
def __prompt_password__(message="Password: "):
	try: 
		if message[len(message)-1] != " ": message += " "
	except IndexError: message = "Password: "
	password = getpass.getpass(prompt=message)
	return password

# get the size of an file / directory.
def __get_file_path_size__(path=None, mode="auto", options=["auto", "bytes", "kb", "mb", "gb", "tb"], type="string"):
	def get_size(directory):
		total = 0
		try:
			# print("[+] Getting the size of", directory)
			for entry in os.scandir(directory):
				if entry.is_file():
					# if it's a file, use stat() function
					total += entry.stat().st_size
				elif entry.is_dir():
					# if it's a directory, recursively call this function
					total += get_size(entry.path)
		except NotADirectoryError:
			# if `directory` isn't a directory, get the file size then
			return os.path.getsize(directory)
		except PermissionError:
			# if for whatever reason we can't open the folder, return 0
			return 0
		return total
	total_size = get_size(path)
	if mode == "auto":
		if int(total_size/1024**4) >= 10:
			total_size = '{:,} TB'.format(int(round(total_size/1024**4,2))).replace(',', '.')
		elif int(total_size/1024**3) >= 10:
			total_size = '{:,} GB'.format(int(round(total_size/1024**3,2))).replace(',', '.')
		elif int(total_size/1024**2) >= 10:
			total_size = '{:,} MB'.format(int(round(total_size/1024**2,2))).replace(',', '.')
		elif int(total_size/1024) >= 10:
			total_size = '{:,} KB'.format(int(round(total_size/1024,2))).replace(',', '.')
		else:
			total_size = '{:,} Bytes'.format(int(int(total_size))).replace(',', '.')
	elif mode == "bytes" or mode == "bytes".upper(): total_size = '{:,} Bytes'.format(int(total_size)).replace(',', '.') 
	elif mode == "kb" or mode == "kb".upper(): total_size = '{:,} KB'.format(int(round(total_size/1024,2))).replace(',', '.') 
	elif mode == "mb" or mode == "mb".upper(): total_size = '{:,} MB'.format(int(round(total_size/1024**2,2))).replace(',', '.') 
	elif mode == "gb" or mode == "gb".upper(): total_size = '{:,} GB'.format(int(round(total_size/1024**3,2))).replace(',', '.') 
	elif mode == "tb" or mode == "tb".upper(): total_size = '{:,} TB'.format(int(round(total_size/1024**4,2))).replace(',', '.') 
	else: __error__("selected an invalid size mode [{}], options {}.".format(mode, options))
	if type == "integer":
		return int(total_size.split(" ")[0])
	else: return total_size 
# get an file paths name.
def __get_file_path_name__(file):
	if file[len(file)-1] == "/": file = file[:-1]
	return file.split("/")[len(file.split("/"))-1]
# set a file path permission.
def __set_file_path_permission__(path, permission=755, sudo=False, recursive=False):
	if recursive: recursive = "-R "
	else: recursive = ""
	if sudo: sudo = "sudo "
	else: sudo = ""
	os.system(f"{sudo}chmod {recursive}{permission} {path}")
# set a file path ownership.
def __set_file_path_ownership__(path, owner=os.environ.get("USER"), group=None, sudo=False, recursive=False):
	if recursive: recursive = "-R "
	else: recursive = ""
	if sudo: sudo = "sudo "
	else: sudo = ""
	if group == None: group = __get_empty_group__()
	os.system(f"{sudo}chown {recursive}{owner}:{group} {path}")
def __get_empty_group__():
	if OS in ["macos"]: return "wheel"
	elif OS in ["linux"]: return "root"
def __delete_file_path__(path, sudo=False, forced=False):
	if sudo: sudo = "sudo "
	options = ""
	if forced: 
		options = " -f "
		if os.path.isdir(path): options = " -fr "
	elif os.path.isdir(path): options = " -r "
	os.system(f"{sudo}rm{options}{path}")

# open a directory.
def __open_directory__(path):
	if OS in ["macos"]:
		os.system(f"open {path}")
	elif OS in ["linux"]:
		os.system(f"nautilus {path}")
	else:
		raise ValueError(f"Invalid operating system: {OS}")

# check parameters.
def __check_parameter__(parameter=None, name="parameter", empty_value=None, response=None):
	if response == None: response = __default_response__()
	if parameter == empty_value: 
		response["error"] = f"Define parameter [{name}]."
		return False, response
	else: return True, response
def __check_parameters__(parameters={"parameter":None}, empty_value=None, response=None):
	response = __default_response__()
	for id, value in parameters.items():
		success, response = __check_parameter__(value, id, empty_value=empty_value, response=response)
		if not success: return False, response
	return True, response

# converting variables.
def __string_to_array__(string, split_char=","):
	array = []
	for i in string.split(split_char):
		for x in range(11):
			if i[0] == " ": i = i[1:]
			elif i[len(i)-1] == " ": i = i[:-1]
			else: break
		array.append(i)
	return array
def __string_to_boolean__(string):
	if string in ["true", "True", True]: return True
	elif string in ["false", "False", False]: return False
	else: raise ValueError(f"Could not convert string [{string}] to a boolean.")
def __string_to_bash__(string):
	a = string.replace('(','\(').replace(')','\)').replace("'","\'").replace(" ","\ ").replace("$","\$").replace("!","\!").replace("?","\?").replace("@","\@").replace("$","\$").replace("%","\%").replace("^","\^").replace("&","\&").replace("*","\*").replace("'","\'").replace('"','\"')       
	return a

# generation.
def __generate__(length=10, alphabetical=True, capitalize=True, digits=True):
	letters = ""
	if digits: letters += string.digits
	if capitalize: letters += string.ascii_uppercase
	if alphabetical: letters += string.ascii_lowercase
	return ''.join(random.choice(letters) for i in range(length))
def __generate_pincode__(characters=6, charset=string.digits):
	return ''.join(random.choice(charset) for x in range(characters))
	#
def __generate_shell_string__(characters=6, numerical_characters=False, special_characters=False):
	charset = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
	for x in ast.literal_eval(str(charset)): charset.append(x.upper())
	if numerical_characters:
		for x in [
			'1', '2', '3', '4', '5', '6', '7', '8', '9', '0'
		]: charset.append(x)
	if special_characters:
		for x in [
			'-', '+', '_'
		]: charset.append(x)
	return ''.join(random.choice(charset) for x in range(characters))
	#

# execute a shell command.
def __execute__(
	# the command in array.
	command=[],
	# wait till the command is pinished. 
	wait=False,
	# the commands timeout, [timeout] overwrites parameter [wait].
	timeout=None, 
	# the commands output return format: string / array.
	return_format="string", 
	# the subprocess.Popen.shell argument.
	shell=False,
	# pass a input string to the process.
	input=None,
):
	def __convert__(byte_array, return_format=return_format):
		if return_format == "string":
			lines = ""
			for line in byte_array:
				lines += line.decode()
			return lines
		elif return_format == "array":
			lines = []
			for line in byte_array:
				lines.append(line.decode().replace("\n","").replace("\\n",""))
			return lines

	# create process.
	p = subprocess.Popen(
		command, 
		shell=shell,
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE,
		stdin=subprocess.PIPE,)
	
	# send input.
	if input != None:
		if isinstance(input, list):
			for s in input:
				p.stdin.write(f'{s}\n'.encode())
		elif isinstance(input, str):
			p.stdin.write(f'{input}\n'.encode())
		else: raise ValueError("Invalid format for parameter [input] required format: [string, array].")
		p.stdin.flush()
	
	# timeout.
	if timeout != None:
		time.sleep(timeout)
		p.terminate()
	
	# await.
	elif wait:
		p.wait()

	# get output.
	output = __convert__(p.stdout.readlines(), return_format=return_format)
	if return_format == "string" and output == "":
		output = __convert__(p.stderr.readlines(), return_format=return_format)
	elif return_format == "array" and output == []:
		output = __convert__(p.stderr.readlines(), return_format=return_format)
	return output

# save & load jsons.
def __load_json__(path):
	data = None
	with open(path, "r") as json_file:
		data = json.load(json_file)
	return data
def __save_json__(path, data):
	with open(path, "w") as json_file:
		json.dump(data, json_file, indent=4, ensure_ascii=False)

# save & load files.
def __load_file__(path):
	file = open(path,mode='rb')
	data = file.read().decode()
	file.close()
	return data
def __save_file__(path, data):
	file = open(path, "w+") 
	file.write(data)
	file.close()

# save & load bytes.
def __load_bytes__(path):
	file = open(path,mode='rb')
	bytes = file.read()
	file.close()
	return bytes
def __save_bytes__(path, bytes):
	file = open(path, "wb") 
	file.write(bytes)
	file.close()

# init a default response.
def __default_response__():
	return r3sponse.ResponseObject({
		"success":False,
		"error":None,
		"message":None,
	})

# check a password.
def __check_password__(password, verify_password):
	response = __default_response__()
	if password != verify_password:
		response["error"] = "Passwords do not match."
		return False, response
	elif len(password) < 12:
		response["error"] = "The password must contain at least 12 characters."
		return False, response
	elif password.lower() == password:
		response["error"] = "The password must contain capital letters."
		return False, response
	match = False
	for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
		if  str(i) in password: match = True ; break
	if match == False:
		response["error"] = "The password must contain digits."
		return False, response
	return True, response

# the date class object.
class Date(object):
	def __init__(self):
		today = datetime.today()
		self.seconds = str(today.strftime('%S'))
		self.minute =  str(today.strftime('%M'))
		self.hour =  str(today.strftime('%H'))
		self.day =  str(today.strftime('%d'))
		self.day_name =  str(today.strftime('%a'))
		self.week =  str(today.strftime('%V'))
		self.month =  str(today.strftime('%m'))
		self.month_name = str(today.strftime('%h'))
		self.year =  str(today.strftime('%Y'))
		self.date =  str(today.strftime('%d-%m-%y'))
		self.timestamp =  str(today.strftime('%d-%m-%y %H:%M'))
		self.shell_timestamp =  str(today.strftime('%d_%m_%y-%H_%M'))
		self.seconds_timestamp =  str(today.strftime('%d-%m-%y %H:%M.%S'))
		self.shell_seconds_timestamp =  str(today.strftime('%d_%m_%y-%H_%M.%S'))
		self.time = self.hour + ":" + self.minute
	def compare(self, comparison, current, format="%d-%m-%y %H:%M"):
		comparison = self.to_seconds(comparison, format=format)
		current = self.to_seconds(current, format=format)
		if comparison >= current:
			return "future"
		elif comparison <= current:
			return "past"
		elif comparison == current:
			return "present"
		else:
			raise ValueError(f"Unexpected error, comparison seconds: {comparison} current seconds: {current}.")
	def increase(self, string, weeks=0, days=0, hours=0, seconds=0, format="%d-%m-%y %H:%M"):
		seconds += 3600*hours
		seconds += 3600*24*days
		seconds += 3600*24*7*weeks
		s = self.to_seconds(string, format=format)
		s += seconds
		return self.from_seconds(s, format=format)
	def decrease(self, string, weeks=0, days=0, hours=0, seconds=0, format="%d-%m-%y %H:%M"):
		seconds += 3600*hours
		seconds += 3600*24*days
		seconds += 3600*24*7*weeks
		s = self.to_seconds(string, format=format)
		s -= seconds
		return self.from_seconds(s, format=format)
	def to_seconds(self, string, format="%d-%m-%y %H:%M"):
		return time.mktime(datetime.strptime(string, format).timetuple())
		#
	def from_seconds(self, seconds, format="%d-%m-%y %H:%M"):
		return datetime.fromtimestamp(seconds).strftime(format)
		#
	def convert(self, string, input="%d-%m-%y %H:%M", output="%Y%m%d"):
		string = datetime.strptime(string, input)
		return string.strftime(output)
