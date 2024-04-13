from tkinter import *

class Pion:
    def __init__(self, nom_case, couleur, cercle):
        """
        Initialise un objet Pion.
        Args:
            nom_case (str): Le nom de la case où se trouve le pion.
            couleur (str): La couleur du pion ('black' ou 'white').
            cercle (object): L'objet cercle représentant visuellement le pion.
        """
        self.nom_case = nom_case
        self.couleur = couleur
        self.cercle = cercle

class Plateau:
    def __init__(self):
        """
        Initialise un objet Plateau et lance le jeu Othello.
        """
        self.fenetre = Tk()
        self.fenetre.resizable(width=False, height=False)
        self.canvas = Canvas(self.fenetre, width=600, height=600, bg = "#{:02x}{:02x}{:02x}".format(5,138,71))
        self.canvas.pack()
        self.dessiner_quadrillage()
        self.assigner_noms_cases()
        self.joueur_actuel = "black"
        self.canvas.bind("<Button-1>", self.jouer_un_pion)
        self.fenetre.mainloop()

    def dessiner_quadrillage(self):
        """
        Dessine le quadrillage du plateau de jeu.
        """
        for i in range(8): 
            for j in range(8):
                x = 75 * j
                y = 75 * i
                self.canvas.create_line(75*j, 0, 75*j, 600, fill="black", width=4)
                self.canvas.create_line(0, 75*i, 600, 75*i, fill="black", width=4)
                if i > 0 and j > 0:  
                    self.canvas.create_oval(x-4, y-4, x+4, y+4, fill="black", outline="black")

    def assigner_noms_cases(self):
        """
        Assigner des noms aux cases du plateau.
        """
        lettres = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.cases_libres = {}
        self.cases_occupees = {}
        # L'axe x en haut, le point (0, 0) est donc en haut à gauche
        for ligne in range(8):
            for colonne in range(8):
                nom_case = lettres[colonne] + str(ligne + 1)
                self.cases_libres[nom_case] = Label(self.fenetre, text = nom_case, bg = "#{:02x}{:02x}{:02x}".format(5,138,71), fg = "white")
                self.cases_libres[nom_case].place(x = colonne * 75 + 37.5, y = ligne * 75 + 37.5)
        self.creer_pion("D4", "white")
        self.creer_pion("D5", "black")
        self.creer_pion("E4", "black")
        self.creer_pion("E5", "white")
        self.qui_doit_jouer = Label(self.fenetre, text="Tour du joueur : Noir", fg="black")
        self.qui_doit_jouer.pack(side="bottom")

    def ligne(self, nom_case):
        """
        Renvoie le numéro de ligne correspondant au nom de la case.
        Args:
            nom_case (str): Le nom de la case.
        Returns:
            int: Le numéro de ligne.
        """
        return int(nom_case[1])

    # Permet de récupérer la colonne où se trouve une case
    def colonne(self, nom_case):
        """
        Renvoie le numéro de colonne correspondant au nom de la case.
        Args:
            nom_case (str): Le nom de la case.
        Returns:
            int: Le numéro de colonne.
        """        
        return ord(nom_case[0]) - 64
    
    def creer_pion(self, nom_case, couleur):
        """
        Crée un pion sur la case spécifiée.
        Args:
            nom_case (str): Le nom de la case où créer le pion.
            couleur (str): La couleur du pion ('black' ou 'white').
        """
        # Si le pion est dans cases_libres alors il n'existe pas, le joueur veut placer un nouveau pion, on crée le pion et la case n'est plus libre
        #Si le pion n'est pas dans cases libre, alors le pion existe déjà et on veut changer sa couleur ie créer un nouveau pion avec la couleur inverse
        if nom_case in self.cases_libres :
            self.cases_libres[nom_case].destroy()
            del self.cases_libres[nom_case]
        i = self.ligne(nom_case) - 1
        j = self.colonne(nom_case) - 1
        cercle = self.canvas.create_oval(j * 75 + 10, i * 75 + 10,   j * 75 + 65, i * 75 + 65,   fill = couleur, outline=couleur)
        pion = Pion(nom_case, couleur, cercle)
        self.cases_occupees[nom_case] = pion

    def jouer_un_pion(self, clique):
        """
        Gère le placement d'un pion lorsque l'utilisateur clique sur une case.

        Args:
            clique (object): L'événement de clic de souris.
        """
        # Fin du jeu
        if not self.cases_libres:
            self.qui_doit_jouer.config(text="Le jeu est terminé")
            return
        # Reconnaissance de la case où l'on a cliqué
        colonne = clique.x // 75 
        ligne = clique.y // 75
        nom_case = chr(colonne + 65) + str(ligne + 1)
        # Case occupée
        if nom_case in self.cases_occupees: 
            couleur = "Noir" if self.joueur_actuel == "black" else "Blanc" 
            self.qui_doit_jouer.config(text="La case est déjà occupée !\nTour du joueur : " + couleur)
            return
        # Positionner le pion et vérifier s'il encadre un pion adverse
        if self.peut_jouer(nom_case):
            self.creer_pion(nom_case, self.joueur_actuel)
            self.joueur_actuel = "white" if self.joueur_actuel == "black" else "black"
            couleur = "Noir" if self.joueur_actuel == "black" else "Blanc" 
            self.qui_doit_jouer.config(text="Tour du joueur : " + couleur) # Annonce à qui c'est le tour de jouer
        else:
            couleur = "Noir" if self.joueur_actuel == "black" else "Blanc" 
            self.qui_doit_jouer.config(text="Le coup n'est pas valide. Veuillez réessayer.\nTour du joueur : " + couleur)

    def peut_jouer(self, nom_case):
        """
        Vérifie si le pion peut être placé à la case spécifiée en respectant les règles du jeu.
        Args:
            nom_case (str): Le nom de la case où le joueur souhaite placer le pion.
        Returns:
            bool: True si le placement est valide, False sinon.
        """
        # Obtenir la ligne et la colonne de la case spécifiée
        ligne = self.ligne(nom_case)
        colonne = self.colonne(nom_case)
        # Déterminer la couleur adverse
        couleur_adverse = "white" if self.joueur_actuel == "black" else "black"
        # Liste des directions possibles pour vérifier les pions encadrés
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]
        # Liste pour stocker les pions encadrés dans toutes les directions
        pions_encadres_totale = []
        # Parcourir toutes les directions pour trouver les pions encadrés
        for direction in directions:
            dir_ligne, dir_colonne = direction
            ligne_temp, colonne_temp = ligne + dir_ligne, colonne + dir_colonne
            pions_a_retourner = []
            # Parcourir la ligne et la colonne dans cette direction
            while 1 <= ligne_temp <= 8 and 1 <= colonne_temp <= 8:
                case_temp = chr(colonne_temp + 64) + str(ligne_temp)
                if case_temp in self.cases_occupees:
                    pion_temp = self.cases_occupees[case_temp]
                    # On trouve un pion qui encadre les pions adverses,
                    # On ajoute tous les pions adverses dans la liste à retourner et on sort de la boucle
                    if pion_temp.couleur == self.joueur_actuel:
                        if pions_a_retourner:
                            pions_encadres_totale.extend(pions_a_retourner) 
                        break
                    # Tant que l'on trouve des pions adverses dans cette direction, on continue la boucle while
                    elif pion_temp.couleur == couleur_adverse:
                        pions_a_retourner.append(pion_temp)
                else:
                    break
                ligne_temp += dir_ligne
                colonne_temp += dir_colonne
        # Changer la couleur des pions encadrés dans toutes les directions
        if pions_encadres_totale:
            for pion_encadre in pions_encadres_totale:
                pion_encadre.couleur = self.joueur_actuel
                self.canvas.itemconfig(pion_encadre.cercle, fill=self.joueur_actuel, outline=self.joueur_actuel)
            # Le pion peut être placé
            return True  
        # Aucun pion encadré n'a changé de couleur
        return False  
    
lancer_une_partie = Plateau()
