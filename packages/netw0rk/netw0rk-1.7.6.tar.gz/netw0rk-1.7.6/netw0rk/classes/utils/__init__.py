#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from netw0rk.classes.config import * 

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
	if isinstance(command, str): command = command.split(' ')
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
	else: sudo = ""
	options = ""
	if forced: 
		options = " -f "
		if os.path.isdir(path): options = " -fr "
	elif os.path.isdir(path): options = " -r "
	os.system(f"{sudo}rm{options}{path}")

# converting variables.
def __array_to_string__(array, joiner=" "):
	string = ""
	for i in array:
		if string == "": string = str(i)
		else: string += joiner+str(i)
	return string
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


# execute a shell script.
def __execute_script__(
	# the script in string.
	script="",
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
	path = "/tmp/shell_script.sh"
	__save_bytes__(path, script.encode())
	__set_file_path_permission__(path,permission=755)
	output = __execute__(
		command=[f"sh", f"{path}"],
		wait=wait,
		timeout=timeout, 
		return_format=return_format, 
		shell=shell,
		input=input,)
	__delete_file_path__(path, forced=True)
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
	data = None
	with open(path, "rb") as file:
		data = file.read()
	return data
def __save_bytes__(path, data):
	with open(path, "wb") as file:
		file.write(data)
