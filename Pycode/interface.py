# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 09:16:51 2023

@author: mathi
"""

from DB import Database, Database_Insert, Database_Read

TABLES = ["client", "ouvrier", "vehicule", "chantier"]
TABLES_COL = [
    ["nom"],
    ["nom", "prenom", "poste", "pwd"],
    ["immatriculation", "taille", "modele"],
    ["nom", "debut", "fin", "commentaire", "materiau", "id_client", "facture"]]

class Interface() :
    def __init__(self) :
        self.cases = ["insert", " "]
        self.description = ["insérer un nouvel élément dans la database", \
                            "quitter"]

    def connection_db(self) : 
        dbname = input("nom de la database ? (ex: projet, postgres...)")
        user = input("nom de l'utilisateur ? (ex: admin, postgres...)")
        pwd = input("mot de passe ? (ex: admin...)")
        host = "localhost"
        port = "5432"
        self.database = Database(dbname, user, pwd, host, port)
        self.database_insert = Database_Insert(dbname, user, pwd, host, port)
        self.database_read = Database_Read(dbname, user, pwd, host, port)

    def quit(self) :
        self.database.disconnect()
        self.database_insert.disconnect()
        self.database_read.disconnect()

    def run(self):
        entree = ""
        while entree != " " :
            entree = input("Que voulez-vous faire ?\n\
                           insert pour insérer un nouvel élément dans la database,\n\
                               SPACE pour quitter.\n\
                        """)

            if entree == "insert" :
                self.insert_data()
            elif entree == " " :
                print(self.database_read.get_all("ouvrier"))
                self.quit()
            else :
                print("Entrée non valide.")
   
    def insert_data(self) :
        table_id = int(input("Dans quelle table souhaitez-vous insérer ?\n \
                        0 : {},\n\
                        1 : {},\n\
                        2 : {},\n\
                        3 : {},\n\
                        4 : quitter.\
                        ".format(TABLES[0], TABLES[1], TABLES[2], TABLES[3])))
        if table_id == 4 :
            self.quit()
        elif TABLES[table_id] == "chantier" :
            data = {}
            data["nom"] = input("Entrez  le nom du chantier : ")
            data["debut"] = input("Quand débutera le chantier ? (format JJ/MM/AAAA HH:mm) ")
            data["fin"] = input("Quand terminera le chantier ? (format JJ/MM/AAAA HH:mm) ")
            data["commentaire"] = input("Un commentaire ? ")
            data["facture"] = input("Quel est le numéro de facture ? ")
            # Client
            clients = self.read
        else :
            data = {}
            for col_name in TABLES_COL[table_id] :
                data_col = input("Entrez une valeur pour {} : ".format(col_name))
                data[col_name] = data_col
            self.database_insert.Insert(TABLES[table_id], data)
            print("L'entrée de {} a bien été insérée.".format(TABLES[table_id]))
            