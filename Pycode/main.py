# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 09:23:09 2023

@author: mathi
"""
from interface import Interface
from DB import Database, Database_Insert, Database_Read

#database_insert = Database_Insert("projet", "admin", "admin", "localhost", "5432")
#database_insert.load_csv("data/test_DB.csv")

interface = Interface()
interface.connection_db()
interface.run()
