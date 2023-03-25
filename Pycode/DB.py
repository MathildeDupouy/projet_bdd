# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import psycopg2 as psyg
from psycopg2 import OperationalError
import datetime

class Database():
    def __init__(self, dbname, user, pwd, host, port):
        self.dbname = dbname;
        self.user = user;
        self.pwd = pwd;
        self.host = host;
        self.port = port;
        try:
            self.conn = psyg.connect(dbname = self.dbname, user = self.user, password = self.pwd,  \
                                 host = self.host, port = self.port)
            print(f"Connection à la database '{dbname}' réussie")
        except OperationalError as e:
            print(f"The error '{e}' occured")
    
    def get_current_chantiers(self, show = False):
        query = """SELECT Cl.nom, Ch.debut, ch.fin, ch.commentaire
        FROM Chantier Ch
        JOIN CLient Cl ON  Ch.id_client = Cl.id
        WHERE Ch.debut < NOW() AND Ch.fin > NOW();"""
        with self.conn:
            with self.conn.cursor() as curs:
                try:
                    curs.execute(query)
                    record = curs.fetchall()
                except OperationalError as e:
                    print(f"The error '{e}' occured dans 'get_current_chantier'")
                    record = None
        if show == True:
            print(f"Nombre de chantier en cours : {len(record)}")
            for i, line in enumerate(record):
                print(f"Chantier {i} : {line[0]} de {line[1]} à {line[2]}, {line[3]}")


a = Database("name", "ben", "eee","localhost","5432")

print("fin test")
