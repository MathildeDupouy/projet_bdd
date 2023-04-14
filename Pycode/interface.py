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
            entree = input("""
Que voulez-vous faire ?
insert pour insérer un nouvel élément dans la database,
SPACE pour quitter.""")

            if entree == "insert" :
                self.insert_data()
            elif entree == " " :
                self.quit()
                return
            else :
                print("Entrée non valide.")
   
    def insert_data(self) :
        table_id = int(input("Dans quelle table souhaitez-vous insérer ?\n\
                        0 : {},\n\
                        1 : {},\n\
                        2 : {},\n\
                        3 : {},\n\
                        4 : quitter.\
                        ".format(TABLES[0], TABLES[1], TABLES[2], TABLES[3])))
        if table_id == 4 :
            self.quit()
            return
        ## Entrer un chantier
        elif TABLES[table_id] == "chantier" :
            data = {}
            data["nom"] = input("Entrez le nom du chantier : ")
            data["debut"] = input("Quand débutera le chantier ? (format JJ/MM/AAAA HH:mm) ")
            data["fin"] = input("Quand terminera le chantier ? (format JJ/MM/AAAA HH:mm) ")
            data["commentaire"] = input("Un commentaire ? ")
            data["facture"] = input("Quel est le numéro de facture ? ")
            data["materiau"] = input("Quel est le materiau concerné (PVC ou CAOUTCHOUC ? ")
            # Client
            self.print_clients()
            data["id_client"] = input("Quel est le client du chantier ?")
            # Insertion chantier
            res_insert = self.database_insert.Insert("chantier", data)
            id_chantier = res_insert[0]
            # Ouvriers
            self.print_ouvriers()
            n = 0
            ouvriers = []
            debuts = []
            fins = []
            entree = input("Missionnez un ouvrier sur le chantier : ")
            # TODO controler date ?
            while entree != " " :
                ouvriers.append(entree)
                entree = input("Quelle date commence-t-il ? (DD/MM/AAAA HH:mm) ")
                debuts.append(entree)
                entree = input("Quelle date finit-il ? (DD/MM/AAAA HH:mm) ")
                fins.append(entree)
                n += 1
                print("Si vous voulez missionner un autre ouvrier, entrez son numéro, sinon tapez espace.")
                entree = input("")
            if(n == 1) :
                self.database_insert.Insert("ordre_de_mission", \
                                            {"id_chantier" : id_chantier,\
                                              "id_ouvrier" : ouvriers[0],\
                                              "debut" : debuts[0], "fin" : fins[0]})
            else :
                self.database_insert.Insert("ordre_de_mission", \
                                            {"id_chantier" : [id_chantier] * n,\
                                              "id_ouvrier" : ouvriers,\
                                              "debut" : debuts, "fin" : fins})

            # Vehicule
            self.print_vehicules()
            n = 0
            vehicules = []
            debuts = []
            fins = []
            entree = input("Réservez un véhicule pour le chantier : ")
            # TODO controler date ?
            while entree != " " :
                vehicules.append(entree)
                entree = input("Quelle date de début ? (DD/MM/AAAA HH:mm) ")
                debuts.append(entree)
                entree = input("Quelle date de fin ? (DD/MM/AAAA HH:mm) ")
                fins.append(entree)
                n += 1
                print("Si vous voulez réserver un autre véhicule, entrez son numéro, sinon tapez espace.")
                entree = input("")
            if (n == 1) :
                self.database_insert.Insert("reservation", \
                                {"id_chantier" : id_chantier,\
                                  "immatriculation" : vehicules[0],\
                                      "debut" : debuts[0], "fin" : fins[0]})
            else :
                self.database_insert.Insert("reservation", \
                            {"id_chantier" : [id_chantier] * n,\
                              "immatriculation" : vehicules[0],\
                                  "debut" : debuts[0], "fin" : fins[0]})

        ## Entrer dans client, ouvrier ou vehicule
        else :
            data = {}
            for col_name in TABLES_COL[table_id] :
                data_col = input("Entrez une valeur pour {} : ".format(col_name))
                data[col_name] = data_col
            self.database_insert.Insert(TABLES[table_id], data)
            print("L'entrée de {} a bien été insérée.".format(TABLES[table_id]))

    def print_ouvriers(self) :
        ouvriers = [(client[0], client[1], client[2]) for client in self.database_read.get_all("ouvrier")]
        print("Les ouvriers sont :")
        for ouvrier in ouvriers :
            print("- {} : {} {}".format(ouvrier[0], ouvrier[1], ouvrier[2]))

    def print_clients(self) :
        clients = [(client[0], client[1]) for client in self.database_read.get_all("client")]
        print("Les clients sont :")
        for client in clients :
            print("- {} : {}".format(client[0], client[1]))

    def print_vehicules(self) :
        vehicules = [(vehicule[0], vehicule[1], vehicule[2]) for vehicule in self.database_read.get_all("vehicule")]
        print("Les véhicules sont :")
        for vehicule in vehicules :
            print("- {} : {} {}".format(vehicule[0], vehicule[2], vehicule[1]))