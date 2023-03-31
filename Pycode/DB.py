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
        self.connect()
        self.table = self.find_DB_table()

    def __repr__(self):
        txt = ""
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
        return txt
    
    def connect(self):
        try:
            self.conn = psyg.connect(dbname = self.dbname, user = self.user, password = self.pwd,  \
                                 host = self.host, port = self.port)
            print(f"Connection à la database '{self.dbname}' réussie")
        except OperationalError as e:
            print(f"The error '{e}' occured")
            self.conn = None
        
    def find_DB_table(self):
        dict = {}
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
        for table in record:
            columns = self.__find_table_column(table[0])
            dict[table[0]] = columns
        return dict
    
    def __find_table_column(self, table_name):
        columns = []
        query = """SELECT column_name FROM information_schema.columns
    WHERE table_name = '{}'""".format(table_name)
        with self.conn:
            with self.conn.cursor() as curs:
                try:
                    curs.execute(query)
                    record = curs.fetchall()
                except OperationalError as e:
                    print(f"The error '{e}' occured in '__repr__'")
                    record = None
        for col in record:
            columns.append(col[0])
        return columns

class Database_Insert(Database):
    def import_test_data(self, path = "data_pour_test/data.xml"):
        
        return None

    def Insert_client(self, noms, show = False):
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

    def Insert(self, table_name, data):
        """
        Ajoute des donnée dans la table demandé
        INPUT :
            - table_name : nom de la table 
            - data : dictionnaire avec pour clefs le nom des colonnes de la table
                     et en valeur une liste des données à ajouter, il faut que toutes
                     les listes soit de la même taille
        OUTPUT None, ajoute dans la table spécifié les données de data.
        """
        test = True
        n = 1
        if(type(next(iter(data.values()))) == list):
        #on vérifie si les listes sont de la même taille
            
            n = len(next(iter(data.values())))
            for val in data.values():
                if len(val) != n : test = False
        if not test : print("Les données de data ne font pas la même taille, rien n'a été ajouté")
        else :
            query = self.query_insert(table_name, data, n)
            with self.conn:
                with self.conn.cursor() as curs:
                    try:
                        curs.execute(query)
                    except OperationalError as e:
                        print(f"The error '{e}' occured in 'Insert_client''")
            self.conn.commit()
        return None
    
    def query_insert(self, table_name, data, n):
        """
        créé la query 'INSERT INTO' à partir d'un nom de table et d'un dictionnaire de données
        """
        query = "INSERT INTO {}(".format(table_name)
        for i, key in enumerate(data.keys()):
            if i != 0 : query += ", " + key
            else : query += key
        query += ") VALUES"
        liste = []
        for value in data.values():
            liste.append(value)
        print(liste)
        if n == 1:
            query += " ('" + str(liste[0]) + "'"
            for elt in liste[1:]:
                query += ", '" + elt + "'"
            query += ");"
        else:
                query += " ('" + str(liste[0][0]) + "'"
                for j in range(1, len(liste)):
                    query += ", '" + str(liste[j][0]) + "'"
                for i in range(1,n):
                    query += "), ('" + str(liste[0][i]) + "'"
                    for j in range(1, len(liste)):
                        query += ", '" + str(liste[j][i]) + "'"
                query += ");"
        return query

    def load_csv(self, filename):
        """
        insère dans la table les données de filename qui doit être placé dans le dossier data
        """
        tablename = []
        les_dict = []
        with open("data/{}".format(filename), 'r') as f:
            next_flag = True
            for line in f.readlines():
                if next_flag:
                    next_flag = False
                    linesplit = line.strip().split()
                    tablename .append(linesplit[0])
                    dict = {}
                    col_name = []
                    for i, col in enumerate(linesplit[1:]):
                        if col != '':
                            col_name.append(col)
                else:
                    linesplit = line.strip().split()
                    if linesplit[0] == "next":
                        next_flag = True
// - - - - - - - - -  - - - - - - - - à finir

            
class Database_Read(Database):
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
                    print(f"The error '{e}' occured in 'get_current_chantier'")
                    record = None
        if show == True:
            print(f"Nombre de chantier en cours : {len(record)}")
            for i, line in enumerate(record):
                print(f"Chantier {i} : {line[0]} de {line[1]} à {line[2]}, {line[3]}")
        return record



a = Database("projet", "admin", "admin","localhost","5432")

print(a)

data = {"nom" : ["amazon", "fnac", "mcdo"]}

i = Database_Insert("projet", "admin", "admin","localhost","5432")

i.Insert("client", data)
