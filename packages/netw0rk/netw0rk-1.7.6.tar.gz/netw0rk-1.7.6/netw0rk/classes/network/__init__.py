#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from netw0rk.classes.config import *
from netw0rk.classes import utils

# the network object class.
class Network(object):
	def __init__(self):

		# variables.
		self._info_ = None
		self.api_key = None
		if os.environ.get("IPINFO_API_KEY") not in ["None", "", None]:
			self.api_key = os.environ.get("IPINFO_API_KEY")

		#
	def info(self):

		# get info.
		info = None
		if self.api_key == None: 
			info = requests.get('https://ipinfo.io/json').json()
		else: 
			info = requests.get('https://ipinfo.io/json', headers={'Authorization': 'Bearer {}'.format(self.api_key)}).json()
		try: 
			error = info["error"]
			if "rate limit exceeded" in str(error["title"]).lower():
				return r3sponse.error(f"(https://ipinfo.io/json) {error['title']}: {error['message'].replace('  ',' ')} Define environment variable $IPINFO_API_KEY to specify an api key.")
			else:
				return r3sponse.error(f"(https://ipinfo.io/json) {error['title']}: {error['message'].replace('  ',' ')}")
		except KeyError: a=1

		# set.
		try: 
			x = info["ip"]
			del(info["ip"])
			info["public_ip"] = x
		except KeyError: 
			return r3sponse.error("Unable to fetch netork info.")
		try: info["private_ip"] = self.__get_private_ip__()
		except: info["private_ip"] = "unkown"
		try: info["hostname"] = socket.gethostname()
		except: info["hostname"] = "unkown"

		# success.
		return r3sponse.success(f"Successfully retrieved the network information.", info)

		#
	def convert_dns(self, dns, timeout=3):
		response = self.ping(dns, timeout=timeout)
		if response["error"] != None: return response
		if response["ip"] == None: 
			return r3sponse.error(f"Failed to convert dns [{dns}].")
		return r3sponse.success(f"Successfully converted dns [{dns}].", {
			"ip":response["ip"]
		})
	def ping(self, ip, timeout=3):

		# set info.
		info = {
			"ip":None,
			"up":False,
		}

		# execute.
		output = utils.__execute__(["ping", ip], timeout=timeout, return_format="string")

		# handle.
		info["dns"] = ip
		try: info["ip"] = output.split(f"PING {ip} (")[1].split("):")[0]
		except: info["ip"] = None
		if "Request timeout for" in output:
			info["up"] = False
		elif " bytes from " in output:
			info["up"] = True
		else:
			info["up"] = None

		# success.
		return r3sponse.success(f"Successfully pinged [{ip}].", info)

		#
	# system functions.
	def __get_private_ip__(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		try:
			# doesn't even have to be reachable
			s.connect(('10.255.255.255', 1))
			ip = s.getsockname()[0]
		except Exception:
			ip = '127.0.0.1'
		finally:
			s.close()
		return ip
		#
	# port in use
	def port_in_use(self, port, host="127.0.0.1"):
		a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		location = (host, port)
		result_of_check = a_socket.connect_ex(location)
		if result_of_check == 0: in_use = True
		else: in_use = False
		a_socket.close()
		return in_use
		#
	# find free port.
	def free_port(self, start=6080):
		for i in range(10000):
			port = start + i
			if not self.port_in_use(port):
				return r3sponse.success(f"Successfully found a free port.", {
					"port":port,
				})
		return r3sponse.error(f"Unable to find a free port.")
		#

# initialized classes.
network = Network()

"""

# get network info.
response = network.info("vandenberghinc.com")

# ping an ip.
response = network.ping("192.168.1.200")

# convert a dns.
response = network.convert_dns("vandenberghinc.com")

"""
