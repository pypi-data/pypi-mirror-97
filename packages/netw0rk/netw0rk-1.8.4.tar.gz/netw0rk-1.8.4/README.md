# Netw0rk
Author(s):  Daan van den Bergh<br>
Copyright:  © 2020 Daan van den Bergh All Rights Reserved<br>
<br>
<br>
<p align="center">
  <img src="https://raw.githubusercontent.com/vandenberghinc/public-storage/master/vandenberghinc/icon/icon.png" alt="Bergh-Encryption" width="50"/>
</p>

## Installation
	pip3 install netw0rk --upgrade && python3 -c "import netw0rk" --create-alias

## CLI:
The netw0rk cli tool.

	Usage: netw0rk <mode> <options> 
	Modes:
	    --network : Access the network.
	        --info : Retrieve the current firewall information.
	    --firewall : Access the firewall (Linux only).
	        --disable : Disable the firewall.
	        --enable : Enable the firewall.
	        --set-default false : Set the default firewall behaviour (deny/allow).
	        --allow 22 : Allow a port in the firewall settings.
	        --deny 22 : Deny a port in the firewall settings.
	    -h / --help : Show the documentation.
	Options:
	    -c : Do not clear the logs.
	Author: Daan van den Bergh. 
	Copyright: © Daan van den Bergh 2020. All rights reserved.

## Python Examples.

### The FireWall object class
The FireWall() object class.
```python

# import the package.
import netw0rk

# retrieve the firewall information.
response = netw0rk.firewall.info()

# disable the firewall.
response = netw0rk.firewall.disable()

# enable the firewall.
response = netw0rk.firewall.enable()

# set the default port action.
response = netw0rk.firewall.set_default(deny=True)

# allow a port.
response = netw0rk.firewall.allow(2200)

# deny a port.
response = netw0rk.firewall.deny(2200)

```

### The Network object class
The Network() object class.
```python

# import the package.
import netw0rk

# get network info.
response = netw0rk.network.info()

# ping an ip.
response = netw0rk.network.ping("192.168.1.200")

# convert a dns.
response = netw0rk.network.convert_dns("vandenberghinc.com")

```

### Response Object.
When a function completed successfully, the "success" variable will be "True". When an error has occured the "error" variable will not be "None". The function returnables will also be included in the response.

	{
		"success":False,
		"message":None,
		"error":None,
		"...":"...",
	}