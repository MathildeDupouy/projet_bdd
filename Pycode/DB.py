# -*- coding: utf-8 -*-
"""



"""
import psycopg2 as psyg
from psycopg2 import OperationalError
import xml.etree.ElementTree as et
import datetime

class Database():
    def __init__(self, dbname, user, pwd, host, port):
        self.dbname = dbname
        self.user = user
        self.pwd = pwd
        self.host = host
        self.port = port
        self.conn = None

    def __repr__(self):
        self.connect()
        txt = ""
        if self.conn:
            query = """SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'public'"""
            with self.conn:
                with self.conn.cursor() as curs:
                    try:
                        curs.execute(query)
                        record = curs.fetchall()
                    except OperationalError as e:
                        print(f"The error '{e}' occured in '__repr__'")
                        record = None
            txt +=  "              List of relations\n"
            txt += "Schema |        Name        | Type  |  Owner\n"
            txt += "-------+--------------------+-------+----------\n"
            for name in record:
                txt += "public | {:^19}| table | {}\n".format(name[0], self.user)
        self.conn.close()
        return txt
    
    def connect(self):
        try:
            self.conn = psyg.connect(dbname = self.dbname, user = self.user, password = self.pwd,  \
                                 host = self.host, port = self.port)
            print(f"Connection à la database '{self.dbname}' réussie")
        except OperationalError as e:
            print(f"The error '{e}' occured")
            self.conn = None


class Database_Insert(Database):
    def import_test_data(self, path = "data_pour_test/data.xml"):
        
        return None

    def Insert_client(self, noms, show = False):
        self.connect()
        if self.conn:
            if (type(noms) == list):
                query = """INSERT INTO client(nom)
                    VALUES ('{}')""".format(noms[0])
                for nom in noms[1:]:
                    query += ", ('{}')".format(nom)
                query+=";"
            else:
                query = """INSERT INTO client(nom)
                    VALUES ('{}');""".format(noms)
            with self.conn:
                with self.conn.cursor() as curs:
                    try:
                        curs.execute(query)
                    except OperationalError as e:
                        print(f"The error '{e}' occured in 'Insert_client''")
        self.conn.commit()
        self.conn.close()

    def Insert_chantier(self, debut, fin, commentaire, materiau, clientname, facture, idclient = None):
        return None


class Database_Read(Database):
    def get_current_chantiers(self, show = False):
        self.connect()
        if self.conn:
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
                        print(f"The error '{e}' occured in 'get_current_chantier'")
                        record = None
            if show == True:
                print(f"Nombre de chantier en cours : {len(record)}")
                for i, line in enumerate(record):
                    print(f"Chantier {i} : {line[0]} de {line[1]} à {line[2]}, {line[3]}")
        self.conn.close()
        return record



a = Database("postgres", "postgres", "admin","localhost","5432")

print(a)




