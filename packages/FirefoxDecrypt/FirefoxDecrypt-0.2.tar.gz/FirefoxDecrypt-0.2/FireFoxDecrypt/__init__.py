#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Author : github.com/L1ghtM4n
# Thanks : github.com/lclevy/firepwd

__all__ = ["DecryptLogins"]

# Import modules
from os import path
# Import packages
from .decryptor import getKey, getLoginData, CKA_ID, url_clean, decrypt3DES

# import FireFoxDecrypt as ff
# ff.DecryptLogins('logins.json', 'key4.db')
def DecryptLogins(loginsFile: str, keydbFile: str, masterPassword="") -> list:
	credentials = []
	if type(loginsFile) == str and not path.exists(loginsFile):
		raise FileNotFoundError("logins.json file not exists!")
	if type(keydbFile) == str and not path.exists(keydbFile):
		raise FileNotFoundError("key4.db file not exists!")
	key, algo = getKey(masterPassword.encode(), keydbFile)
	if key == None:
		raise Exception("Unable to retrieve key")
	logins = getLoginData(loginsFile)
	if algo == '1.2.840.113549.1.12.5.1.3' or algo == '1.2.840.113549.1.5.13':	
		for i in logins:
			assert i[0][0] == CKA_ID
			hostname=url_clean.sub('', i[2]).strip().strip('/')
			username=decrypt3DES(i[0][2], key, i[0][1])
			password=decrypt3DES(i[1][2], key, i[1][1])
			credentials.append({
				"hostname": hostname,
				"username": username,
				"password": password
			})
	return credentials

