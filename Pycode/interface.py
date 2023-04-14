# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 09:16:51 2023

@author: mathi
"""

from DB import Database, Database_Insert, Database_Read

class Interface() :
    def __init__(self) :
        self.database = None
        self.cases = ["insert", " "]
        self.description = ["insérer un nouvel élément dans la database", \
                            "quitter"]

    def connection_db(self) : 
        dbname = insert("nom de la database ? (ex: projet, postgres...)")
        user = insert("nom de l'utilisateur ? (ex: admin, postgres...)")
        pwd = insert("nom de l'utilisateur ? (ex: admin...)")
        host = "localhost"
        port = "5432"
        self.database = Database(dbname, user, pwd, host, port)
    
    def run(self):
        entree = ""
        while entree !== " " :
            entree = input(
                """
                Que voulez-vous faire ?
                insert pour insérer un nouvel élément dans la database, 
                SPACE pour quitter.
                """
                )

            match entree :
                case "insert" :
                    
                case " " :
                    return
                case _ :
                    print("Entrée non valide.")
            