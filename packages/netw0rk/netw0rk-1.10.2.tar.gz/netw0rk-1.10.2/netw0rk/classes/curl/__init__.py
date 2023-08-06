#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from netw0rk.classes.config import *
from netw0rk.classes import utils

# the curl object class.
class Curl(object):
	def __init__(self, 
		base_url=None,
		headers={},
	):

		#	-	init:
		if base_url[len(base_url)-1] != '/': base_url += '/'
		self.base_url = base_url
		self.headers = headers
	def download_img(self, url, img):
		url = self.base_url+url.replace('//','/')
		os.system('curl -s -o {url} "{img}"')
		if Files.exists(img_path): return True
		else: return False
	def get(self, url, data=None):
		url = self.base_url+url.replace('//','/')
		if data == None: return requests.get(url, headers=self.headers).json()
		else: return requests.get(url, data=data, headers=self.headers).json()
	def post(self, url, data=None):
		url = self.base_url+url.replace('//','/')
		if data == None: return requests.post(url, headers=self.headers).json()
		else: return requests.post(url, json=data, headers=self.headers).json()
	def delete(self, url, data=None):
		url = self.base_url+url.replace('//','/')
		if data == None:  return requests.delete(url, headers=self.headers)
		else: return requests.delete(url, json=data, headers=self.headers)
