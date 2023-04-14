# -*- coding: utf-8 -*-
"""



"""
import psycopg2 as psyg
from psycopg2 import OperationalError
import xml.etree.ElementTree as et
import os
import datetime
import locale
locale.setlocale(locale.LC_TIME,'')

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

    def disconnect(self):
        self.conn.close()

    def __del__(self):
        self.conn.close()

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
                        print(f"The error '{e}' occured in 'Insert_{table_name}'")
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

    def load_csv(self, filename = "pycode/data/test_DB.csv"):
        """
        insère dans la table les données de filename qui doit être placé dans le dossier data
        """

        # - - - création d'une liste de dictionnaire contenant les données à insérer dans la DB
        tablename = []
        les_dict = []
        with open(filename, 'r') as f:
            next_flag = True
            for line in f.readlines():
                if next_flag:
                    next_flag = False
                    linesplit = line.strip().split(',')
                    tablename.append(linesplit[0].strip())
                    dict = {}
                    col_name = []
                    for i, col in enumerate(linesplit[1:]):
                        if col != '':
                            col_name.append((i+1, col))
                            dict[col] = []
                else:
                    linesplit = line.strip().split(',')
                    if "next" in linesplit[0]:
                        next_flag = True
                        les_dict.append(dict)
                    else:
                        for i, col in col_name:
                            dict[col].append(linesplit[i].strip())

        # - - - Ajout de l'ensemble des dictionnaires dans la DB
        for i, dict in enumerate(les_dict):
            self.Insert(tablename[i], dict)

            
class Database_Read(Database):
    def get_current_chantiers(self, show = False):
        """
        Renvoi les chantier en cours à la date et hure d'exécution
        (nom, debut, fin, commentaire)
        """
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
                print(f"Chantier {i} : {line[0]} du {line[1].strftime('%d %b %Y à %Hh%M')} au {line[2].strftime('%d %b %Y à %Hh%M')}, {line[3]}")
        return record

    def get_futur_chantiers(self, show = False):
        """
        Renvoie les chantiers à venir
        (nom, debut, fin, commentaire)
        """
        query = """SELECT Cl.nom, Ch.debut, ch.fin, ch.commentaire
        FROM Chantier Ch
        JOIN CLient Cl ON  Ch.id_client = Cl.id
        WHERE Ch.debut >= NOW()
        ORDER BY Ch.debut;"""
        with self.conn:
            with self.conn.cursor() as curs:
                try:
                    curs.execute(query)
                    record = curs.fetchall()
                except OperationalError as e:
                    print(f"The error '{e}' occured in 'get_futur_chantier'")
                    record = None
        if show == True:
            print(f"Nombre de chantier à venir : {len(record)}")
            for i, line in enumerate(record):
                print(f"Chantier {i} : {line[0]} du {line[1].strftime('%d %b %Y à %Hh%M')} au {line[2].strftime('%d %b %Y à %Hh%M')}, {line[3]}")
        return record

    def get_EDT(self, nom, prenom, poste, pwd, show = False):
        """
        Renvoie les chantiers d'un salarié pour la semaine à venir 
        (nom, debut, fin, materiau)
        """
        Jplus7 = datetime.datetime.now() + datetime.timedelta(days = 7)
        J = datetime.datetime.now()
        query = """SELECT Ch.nom, Ord.debut, Ord.fin, Ch.materiau
FROM ordre_de_mission Ord
JOIN ouvrier Ou ON Ord.id_ouvrier = Ou.id
JOIN chantier Ch ON Ord.id_chantier = Ch.id
WHERE 
Ou.nom='{}' AND Ou.prenom='{}' AND Ou.poste='{}' AND Ou.pwd='{}' AND
Ord.debut<='{}' AND Ord.fin>='{}'
ORDER BY Ord.debut;
        """.format(nom, prenom, poste, pwd, Jplus7, J)
        with self.conn:
            with self.conn.cursor() as curs:
                try:
                    curs.execute(query)
                    record = curs.fetchall()
                except OperationalError as e:
                    print(f"The error '{e}' occured in 'get_futur_chantier'")
                    record = None
        if show == True:
            print(f"Nombre de chantier cette semaine : {len(record)}")
            for i, line in enumerate(record):
                print(f"Chantier {i} : {line[0]} du {line[1].strftime('%d %b %Y à %Hh%M')} au {line[2].strftime('%d %b %Y à %Hh%M')}, Prévoir {line[3]}")
        return record
    def availaible_vehicule(self, date, show = False):
        """
        renvoie la liste des vehicules disponible à une date donnée
         date doit être soit du type datetime soit une str de la forme "DD-MM-YYYY"
        (modele, taille, immatriculation, nom_chantier)
        """
        if type(date) == str:
            date = date + "-09-00"
            date = datetime.datetime.strptime(date, "%d-%m-%Y-%H-%M")
        query = """
        SELECT Veh.modele, Veh.taille, Veh.immatriculation
        EXCEPT(
        SELECT Veh.modele, Veh.taille, Veh.immatriculation
        FROM vehicule Veh
        JOIN reservation Res ON Res.immatriculation = Veh.immatriculation
        JOIN chantier Ch ON Ch.id = Res.id_chantier
        WHERE Res.debut<='{}' AND Res.fin>='{});
        """.format(date)
        with self.conn:
            with self.conn.cursor() as curs:
                try:
                    curs.execute(query)
                    record = curs.fetchall()
                except OperationalError as e:
                    print(f"The error '{e}' occured in 'get_futur_chantier'")
                    record = None
        if show == True:
            print(f"Nombre de véhicule disponible : {len(record)}")
            for i, line in enumerate(record):
                print(f"Chantier {i} : {line[0]} du {line[1].strftime('%d %b %Y à %Hh%M')} au {line[2].strftime('%d %b %Y à %Hh%M')}, Prévoir {line[3]}")
        return record
    
    def get_all(self, table):
        """
        renvoie la liste des noms associé à une table, ("ouvrier", "chantier" ou "client")
        (*)
        """
        query = """
        SELECT * FROM {};
        """.format(table)
        with self.conn:
            with self.conn.cursor() as curs:
                try:
                    curs.execute(query)
                    record = curs.fetchall()
                except OperationalError as e:
                    print(f"The error '{e}' occured in 'get_futur_chantier'")
                    record = None
        return record
        

if __name__ == "__main__":
    a = Database("projet", "admin", "admin","localhost","5432")
    print(a)
    print(a.table)

    i = Database_Insert("projet", "admin", "admin","localhost","5432")

    r = Database_Read("projet", "admin", "admin","localhost","5432")
    r.get_EDT("riner", "teddy", "judoka", "TR", True)
    print(r.get_nom("chantier"))




