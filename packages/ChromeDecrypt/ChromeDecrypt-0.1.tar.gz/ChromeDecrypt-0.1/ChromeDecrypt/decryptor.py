#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author github.com/L1ghtM4n

__all__ = ["DecryptPassword"]

# Import modules
from base64 import b64decode
from Crypto.Cipher import AES
from json import load as json_load
from DPAPI import CryptUnprotectData

""" Decrypt chrome password """
def DecryptPassword(buffer: bytes, aes_key: bytes):
    assert len(aes_key) == 32, "Invalid encryption key"
    assert len(buffer) > 15, "Invalid buffer"
    cipher = AES.new(aes_key, AES.MODE_GCM, buffer[3:15])
    return cipher.decrypt(buffer[15:])[:-16].decode(errors="ignore")

""" Read master key from Local State file """
def DecryptMasterKey(LocalStateFile: str) -> bytes:
    with open(LocalStateFile, 'r') as LocalState:
        encrypted_key = json_load(LocalState)["os_crypt"]["encrypted_key"]
        decoded_key = b64decode(encrypted_key)[5:]
        decrypted_key = CryptUnprotectData(decoded_key)
        assert len(decrypted_key) == 32, "Invalid encryption key"
        return decrypted_key
