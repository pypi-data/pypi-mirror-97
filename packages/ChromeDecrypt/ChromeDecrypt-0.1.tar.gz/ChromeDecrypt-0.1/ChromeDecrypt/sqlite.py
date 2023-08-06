#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author github.com/L1ghtM4n

__all__ = ["DatabaseConnection"]

# Import modules
from os import remove
from io import BufferedReader
from tempfile import NamedTemporaryFile
from sqlite3 import connect as sqlite_connect

""" DataBase connection object with auto cleanup """
class DatabaseConnection(object):
    def __init__(self, db: BufferedReader, name="DataBase"):
        assert db is not None, "No buffer"
        assert "b" in db.mode, "Required 'rb' mode"
        self.tmp = NamedTemporaryFile(
            prefix=name + "_", 
            suffix=".tdb", 
            delete=False
        )
        db.seek(0)
        self.tmp.write(db.read())
        self.tmp.close()
        self.connection = sqlite_connect(self.tmp.name)
        self.cursor = self.connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
        remove(self.tmp.name)
