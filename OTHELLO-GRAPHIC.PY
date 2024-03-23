from tkinter import *

class Pion:
    def __init__(self, nom_case, couleur, cercle):
        self.nom_case = nom_case
        self.couleur = couleur
        self.cercle = cercle

class Plateau:
    def __init__(self):
        self.fenetre = Tk()
        self.fenetre.resizable(width=False, height=False)
        self.canvas = Canvas(self.fenetre, width=600, height=600, background = "green")
        self.canvas.pack()

        self.dessiner_quadrillage()
        self.assigner_noms_cases()
        self.joueur_actuel = "black"
        self.canvas.bind("<Button-1>", self.jouer_un_pion)#<Button-1> = clique souris bouton gauche 
        #Après le clique l'événement self.jouer_un_pion est déclenché est le clique est l'argument de la fonction

        self.fenetre.mainloop()


############# INTERFACE VISUELLE ##########
    def dessiner_quadrillage(self):
        i = 1
        while i < 8:
            self.canvas.create_line(75*i, 0, 75*i, 600, fill="white")
            self.canvas.create_line(0, 75*i, 600, 75*i, fill="white")
            i += 1

    def assigner_noms_cases(self):
        lettres = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.cases_libres = {}
        self.cases_occupees = {}

        #L'axe x en haut, le point (0, 0) est donc en haut à gauche
        #On utilise label pour écrire sur le canvas
        for ligne in range(8):
            for colonne in range(8):
                nom_case = lettres[colonne] + str(ligne + 1)
                self.cases_libres[nom_case] = Label(self.fenetre, text = nom_case, bg = "green", fg = "white")
                self.cases_libres[nom_case].place(x = colonne * 75 + 37.5, y = ligne * 75 + 37.5)

        self.creer_pion("D4", "white")
        self.creer_pion("D5", "black")
        self.creer_pion("E4", "black")
        self.creer_pion("E5", "white")

        self.qui_doit_jouer = Label(self.fenetre, text="Tour du joueur : Noir", fg="green")
        self.qui_doit_jouer.pack(side="bottom")

    #Permet de récupérer la ligne où se trouve une case
    def ligne(self, nom_case):
        return int(nom_case[1]) #transforme le char en int

    #Permet de récupérer la colonne où se trouve une case
    def colonne(self, nom_case):
        return ord(nom_case[0]) - 64 #recupe le numéro alphabétique de la lettre A=1 B=2 etc
    
    def creer_pion(self, nom_case, couleur):
        #Si le pion est dans cases_libres alors il n'existe pas, le joueur veut placer un nouveau pion, on crée le pion et la case n'est plus libre
        #Si le pion n'est pas dans cases libre, alors le pion existe déjà et on veut changer sa couleur = créer un nouveau pion avec la couleur inverse
        if nom_case in self.cases_libres :
            self.cases_libres[nom_case].destroy()
            del self.cases_libres[nom_case]

        i = self.ligne(nom_case) - 1
        j = self.colonne(nom_case) - 1
        cercle = self.canvas.create_oval(j * 75 + 10, i * 75 + 10,   j * 75 + 65, i * 75 + 65,   fill = couleur)
        pion = Pion(nom_case, couleur, cercle)
        self.cases_occupees[nom_case] = pion





############# LE JOUEUR VEUT JOUER UNE CASE ##########
    #On verifie que les regles soient respectées
    #Si tout est bon, on crée le pion voulu par le joueur
    def jouer_un_pion(self, clique):
        #On vérifie qu'il existe des cases libres, s'il n'y a plus de cases libres le jeu est terminé
        if not self.cases_libres:
            self.qui_doit_jouer.config(text="Le jeu est terminé")
            return

        #Reconnaissance de la case où l'on a cliqué
        colonne = clique.x // 75 #division entière pour savoir dans quelle case se trouve le clique de la souris
        ligne = clique.y // 75 #division entière pour savoir dans quelle case se trouve le clique de la souris
        nom_case = chr(colonne + 65) + str(ligne + 1)

        ######## REGLES ########
        #CASE DEJA OCCUPEE
        if nom_case in self.cases_occupees : #regarder si la case est dans le dictionnaire cases_occupee, si elle ne l'est pas alors on peut placer un pion dessus
            couleur = "Noir" if self.joueur_actuel == "black" else "Blanc" 
            self.qui_doit_jouer.config(text="La case est déjà occupée !\nTour du joueur : " + couleur)
            return
        #PION DOIT ENCADRER UN AUTRE PION
        pions_encadres = self.cherche_pions_voisins(nom_case)
        if pions_encadres == 0:
            couleur = "Noir" if self.joueur_actuel == "black" else "Blanc" 
            self.qui_doit_jouer.config(text="Cette case ne peut pas être jouée. Le pion doit encadrer un ou plusieurs pions adverses.\nTour du joueur : " + couleur)
            return
        ######## REGLES ########
        
        self.creer_pion(nom_case, self.joueur_actuel)
        self.joueur_actuel = "white" if self.joueur_actuel == "black" else "black" #change la couleur avec laquelle on joue après chaque pion posé
        
        couleur = "Noir" if self.joueur_actuel == "black" else "Blanc" 
        self.qui_doit_jouer.config(text="Tour du joueur : " + couleur) #Annonce à qui c'est le tour de jouer



############################ Dans cette fonction on regarde si le pion voisin est un pion adverse ###########################
#################### Si oui, on appelle la fonction cherche_pions_encadrés qui regarde si son voisin à lui ##################
#################### est de la couleur du joueur, si oui on peut l'encadrer, si non on continue de chercher  ################
####################### jusqu'à tomber sur une case vide ou un pion d'une même couleur que le joueur ########################
    def cherche_pions_voisins(self, nom_case):
        #On regarde les 8 cases autours de notre pion

        #LIGNE AU-DESSUS de notre case
        i = self.ligne(nom_case) - 1
        j = self.colonne(nom_case) - 1
        nom_pion =  chr(j + 64) + str(i)
        if nom_pion in self.cases_occupees and 0 < i < 9 and 0 < j < 9 : #Est-ce qu'il y a un pion sur cette case ?
            pion = self.cases_occupees.get(nom_pion) #Oui il y a un pion donc on le récupère
            i = i - 1 #on prépare i et j pour regarder le voisin de ce pion
            j = j - 1
            if pion.couleur != self.joueur_actuel and 0 < i < 9 and 0 < j < 9 : #Est-ce que c'est un pion adverse
                liste_pions_adverses = [] #Oui, donc on récupère les pions de couleur différente dans la liste pour pouvoir les encadrer si possible
                liste_pions_adverses.append(pion)
                nom_pion =  chr(j + 64) + str(i)
                pion = self.cases_occupees.get(nom_pion) #On récupère aussi le voisin du pion adverse pour regarder 
                if pion is not None :                    #si c'est aussi un pion adverse, un pion du joeur, ou une case vide
                    #Ce n'est pas une case vide, donc peut-être que c'est un pion adverse ou un pion du joeur, on regarde ça avec cette fonction
                    return self.cherche_pions_encadres(pion.couleur, "diagonale haute gauche", i, j, liste_pions_adverses)
                else :
                    return 0

        i = self.ligne(nom_case) - 1
        j = self.colonne(nom_case)
        nom_pion =  chr(j + 64) + str(i)
        if nom_pion in self.cases_occupees and 0 < i < 9 and 0 < j < 9 :
            pion = self.cases_occupees.get(nom_pion)
            i = i - 1
            if pion.couleur != self.joueur_actuel and 0 < i < 9 and 0 < j < 9 :
                liste_pions_adverses = [] #On récupère dedans tous les pions de couleur différente que l'on encadrera
                liste_pions_adverses.append(pion)
                nom_pion =  chr(j + 64) + str(i)
                pion = self.cases_occupees.get(nom_pion)
                if pion is not None :
                    return self.cherche_pions_encadres(pion.couleur, "au-dessus", i, j, liste_pions_adverses)
                else :
                    return 0

        i = self.ligne(nom_case) - 1
        j = self.colonne(nom_case) + 1
        nom_pion =  chr(j + 64) + str(i)
        if nom_pion in self.cases_occupees and 0 < i < 9 and 0 < j < 9 :
            pion = self.cases_occupees.get(nom_pion)
            i = i - 1
            j = j + 1
            if pion.couleur != self.joueur_actuel and 0 < i < 9 and 0 < j < 9 :
                liste_pions_adverses = [] #On récupère dedans tous les pions de couleur différente que l'on encadrera
                liste_pions_adverses.append(pion)
                nom_pion =  chr(j + 64) + str(i)
                pion = self.cases_occupees.get(nom_pion)
                if pion is not None :
                    return self.cherche_pions_encadres(pion.couleur, "diagonale haute droite", i, j, liste_pions_adverses)
                else :
                    return 0

        #LIGNE OU SE TROUVE notre case
        i = self.ligne(nom_case)
        j = self.colonne(nom_case) - 1
        nom_pion =  chr(j + 64) + str(i)
        if nom_pion in self.cases_occupees and 0 < i < 9 and 0 < j < 9 :
            pion = self.cases_occupees.get(nom_pion)
            j = j - 1
            if pion.couleur != self.joueur_actuel and 0 < i < 9 and 0 < j < 9 :
                liste_pions_adverses = [] #On récupère dedans tous les pions de couleur différente que l'on encadrera
                liste_pions_adverses.append(pion)
                nom_pion =  chr(j + 64) + str(i)
                pion = self.cases_occupees.get(nom_pion)
                if pion is not None :
                    return self.cherche_pions_encadres(pion.couleur, "gauche", i, j, liste_pions_adverses)
                else :
                    return 0

        i = self.ligne(nom_case)
        j = self.colonne(nom_case) + 1
        nom_pion =  chr(j + 64) + str(i)
        if nom_pion in self.cases_occupees and 0 < i < 9 and 0 < j < 9 :
            pion = self.cases_occupees.get(nom_pion)
            j = j - 1
            if pion.couleur != self.joueur_actuel and 0 < i < 9 and 0 < j < 9 :
                liste_pions_adverses = [] #On récupère dedans tous les pions de couleur différente que l'on encadrera
                liste_pions_adverses.append(pion)
                nom_pion =  chr(j + 64) + str(i)
                pion = self.cases_occupees.get(nom_pion)
                if pion is not None :
                    return self.cherche_pions_encadres(pion.couleur, "droite", i, j, liste_pions_adverses)
                else :
                    return 0

        #LIGNE EN-DESSOUS de notre case
        i = self.ligne(nom_case) + 1
        j = self.colonne(nom_case) - 1
        nom_pion =  chr(j + 64) + str(i)
        if nom_pion in self.cases_occupees and 0 < i < 9 and 0 < j < 9 :
            pion = self.cases_occupees.get(nom_pion)
            i = i + 1
            j = j - 1
            if pion.couleur != self.joueur_actuel and 0 < i < 9 and 0 < j < 9 :
                liste_pions_adverses = [] #On récupère dedans tous les pions de couleur différente que l'on encadrera
                liste_pions_adverses.append(pion)
                nom_pion =  chr(j + 64) + str(i)
                pion = self.cases_occupees.get(nom_pion)
                if pion is not None :
                    return self.cherche_pions_encadres(pion.couleur, "diagonale basse gauche", i, j, liste_pions_adverses)
                else :
                    return 0

        i = self.ligne(nom_case) + 1
        j = self.colonne(nom_case)
        nom_pion =  chr(j + 64) + str(i)
        if nom_pion in self.cases_occupees and 0 < i < 9 and 0 < j < 9 :
            pion = self.cases_occupees.get(nom_pion)
            i = i + 1
            if pion.couleur != self.joueur_actuel and 0 < i < 9 and 0 < j < 9 :
                liste_pions_adverses = [] #On récupère dedans tous les pions de couleur différente que l'on encadrera
                liste_pions_adverses.append(pion)
                nom_pion =  chr(j + 64) + str(i)
                pion = self.cases_occupees.get(nom_pion)
                if pion is not None :
                    return self.cherche_pions_encadres(pion.couleur, "en-dessous", i, j, liste_pions_adverses)
                else :
                    return 0

        i = self.ligne(nom_case) + 1
        j = self.colonne(nom_case) + 1
        nom_pion =  chr(j + 64) + str(i)
        if nom_pion in self.cases_occupees and 0 < i < 9 and 0 < j < 9 :
            pion = self.cases_occupees.get(nom_pion)
            i = i + 1
            j = j + 1
            if pion.couleur != self.joueur_actuel and 0 < i < 9 and 0 < j < 9 :
                liste_pions_adverses = [] #On récupère dedans tous les pions de couleur différente que l'on encadrera
                liste_pions_adverses.append(pion)
                nom_pion =  chr(j + 64) + str(i)
                pion = self.cases_occupees.get(nom_pion)
                if pion is not None :
                    return self.cherche_pions_encadres(pion.couleur, "diagonale basse droite", i, j, liste_pions_adverses)
                else :
                    return 0

        return 0


################# On cherche les pions adverses que l'on encadre ##############
    def cherche_pions_encadres(self, couleur, direction, i, j, liste_pions_adverses):
        #Si on tombe sur un pion de la même couleur alors on a encadré un ou des pions !
        #On change la couleur des pions encadrés que l'on avait récupéré dans la liste, et on renvoie le nombre de pions encadrés
        if couleur == self.joueur_actuel:
            for pion in liste_pions_adverses:
                if pion.couleur == "white":
                    self.creer_pion(pion.nom_case, "black")
                elif pion.couleur == "black":
                    self.creer_pion(pion.nom_case, "white")
            return len(liste_pions_adverses)

        #On parcourt tous les pions que l'on pourrait encadrer jusqu'à soit tomber sur un case vide, soit un pion du joeur
        #Si le pion qu'on nous a envoyé était sur la diagonale en haut à gauche, alors il ne faut regarder que les pions 
        #dans cette direction, car ce sont les seuls pions qu'on pourrait encadrer
        #LIGNE AU-DESSUS de notre case
        if direction == "diagonale haute gauche" :
            i = i - 1
            j = j - 1
            nom_pion =  chr(j + 64) + str(i)
            pion = self.cases_occupees.get(nom_pion)
            if pion is not None :
                liste_pions_adverses.append(pion)
                self.cherche_pions_encadres(pion.couleur, "diagonale haute gauche", i, j, liste_pions_adverses)
            else :
                return 0

        if direction == "au-dessus" :
            i = i - 1
            nom_pion =  chr(j + 64) + str(i)
            pion = self.cases_occupees.get(nom_pion)
            if pion is not None :
                liste_pions_adverses.append(pion)
                self.cherche_pions_encadres(pion.couleur, "au-dessus", i, j, liste_pions_adverses)
            else :
                return 0

        if direction == "diagonale haute droite" :
            i = i - 1
            j = j + 1
            nom_pion =  chr(j + 64) + str(i)
            pion = self.cases_occupees.get(nom_pion)
            if pion is not None :
                liste_pions_adverses.append(pion)
                self.cherche_pions_encadres(pion.couleur, "diagonale haute droite", i, j, liste_pions_adverses)
            else :
                return 0

            #LIGNE OU SE TROUVE notre case
        if direction == "gauche" :
            j = j - 1
            nom_pion =  chr(j + 64) + str(i)
            pion = self.cases_occupees.get(nom_pion)
            if pion is not None :
                liste_pions_adverses.append(pion)
                self.cherche_pions_encadres(pion.couleur, "gauche", i, j, liste_pions_adverses)
            else :
                return 0

        if direction == "droite" :
            j = j + 1
            nom_pion =  chr(j + 64) + str(i)
            pion = self.cases_occupees.get(nom_pion)
            if pion is not None :
                liste_pions_adverses.append(pion)
                self.cherche_pions_encadres(pion.couleur, "droite", i, j, liste_pions_adverses)
            else :
                return 0

        #LIGNE EN-DESSOUS de notre case
        if direction == "diagonale basse gauche" :
            i = i + 1
            j = j - 1
            nom_pion =  chr(j + 64) + str(i)
            pion = self.cases_occupees.get(nom_pion)
            if pion is not None :
                liste_pions_adverses.append(pion)
                self.cherche_pions_encadres(pion.couleur, "diagonale basse gauche", i, j, liste_pions_adverses)
            else :
                return 0

        if direction == "en-dessous" :
            i = i + 1
            nom_pion =  chr(j + 64) + str(i)
            pion = self.cases_occupees.get(nom_pion)
            if pion is not None :
                liste_pions_adverses.append(pion)
                self.cherche_pions_encadres(pion.couleur, "en-dessous", i, j, liste_pions_adverses)
            else :
                return 0

        if direction == "diagonale basse droite" :
            i = i + 1
            j = j + 1
            nom_pion =  chr(j + 64) + str(i)
            pion = self.cases_occupees.get(nom_pion)
            if pion is not None :
                liste_pions_adverses.append(pion)
                self.cherche_pions_encadres(pion.couleur, "diagonale basse droite", i, j, liste_pions_adverses)
            else :
                return 0


lancer_une_partie = Plateau()