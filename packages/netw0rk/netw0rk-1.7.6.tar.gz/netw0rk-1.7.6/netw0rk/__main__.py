#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# insert the package for universal imports.
import os, sys, syst3m

# settings.
SOURCE_NAME = "netw0rk"
SOURCE_PATH = syst3m.defaults.source_path(__file__, back=1)
BASE = syst3m.defaults.source_path(SOURCE_PATH, back=1)
sys.path.insert(1, BASE)

# imports.
import netw0rk
from netw0rk.classes.config import *

# the cli object class.
class CLI(cl1.CLI):
	def __init__(self):
		
		# defaults.
		cl1.CLI.__init__(self,
			modes={
				"--network":"Access the network.",
				"    --info":"Retrieve the current network information.",
				"--firewall":"Access the firewall (Linux only).",
				"    --info":"Retrieve the current firewall information.",
				"    --disable":"Disable the firewall.",
				"    --enable":"Enable the firewall.",
				"    --set-default false":"Set the default firewall behaviour (deny/allow).",
				"    --allow 22":"Allow a port in the firewall settings.",
				"    --deny 22":"Deny a port in the firewall settings.",
				"-h / --help":"Show the documentation.",
			},
			options={
				"-c":"Do not clear the logs.",
			},
			alias=ALIAS,
			executable=__file__,
		)

		#
	def start(self):
		self.arguments.check()
		
		# clear logs.
		if not self.arguments.present(['-c']):
			os.system("clear")

		# help.
		if self.arguments.present(['-h', '--help']):
			print(self.documentation)

		# network.
		elif self.arguments.present(['--network']):

			# info.
			if self.arguments.present(['--info']):
				response = netw0rk.network.info()
				r3sponse.log(response=response)
				if response.success: 
					del response["message"] ; del response["error"] ; del response["success"]
					print("Network info:")
					print(response.json(indent=3)[:-2].replace('",',"").replace('"',"").replace('\n  ',"\n * ")[2:])


			# invalid.
			else:  self.invalid()

		# firewall.
		elif self.arguments.present(['--firewall']):

			# check os.
			syst3m.defaults.operating_system(supported=["linux"])

			# retrieve the firewall information.
			if self.arguments.present(['--info']):
				response = netw0rk.firewall.info()
				r3sponse.log(response=response)
				if response.success: 
					del response["message"] ; del response["error"] ; del response["success"]
					print(response.json(indent=3).replace("{\n","").replace("\n}","").replace('",',"").replace('"',"").replace('\n  ',"\n * "))

			# disable the firewall.
			elif self.arguments.present(['--disable']):
				response = netw0rk.firewall.disable()
				r3sponse.log(response=response)

			# enable the firewall.
			elif self.arguments.present(['--enable']):
				response = netw0rk.firewall.enable()
				r3sponse.log(response=response)

			# set the default port action.
			elif self.arguments.present(['--set-default']):
				deny = self.arguments.get("--set-default")
				if deny in ["True", "true", True]: deny = True
				else: deny = False
				response = netw0rk.firewall.set_default(deny=deny)
				r3sponse.log(response=response)

			# allow a port.
			elif self.arguments.present(['--allow']):
				port = int(self.arguments.get("--allow"))
				response = netw0rk.firewall.allow(port)
				r3sponse.log(response=response)

			# deny a port.
			elif self.arguments.present(['--deny']):
				port = int(self.arguments.get("--deny"))
				response = netw0rk.firewall.deny(port)
				r3sponse.log(response=response)


			# invalid.
			else:  self.invalid()

		# invalid.
		else:  self.invalid()

		#
	
# main.
if __name__ == "__main__":
	cli = CLI()
	if "--developer" in sys.argv:
		cli.start()
	else:
		try:
			cli.start()
		except KeyboardInterrupt:
			print("Aborted: KeyboardInterrupt")

