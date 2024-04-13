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
        self.nombre_pions_label = Label(self.fenetre, text="", fg="white")
        self.nombre_pions_label.pack(side="top")
        self.mise_a_jour_nombre_pions()
        self.coups_label = Label(self.fenetre, text="", fg="white")
        self.coups_label.pack(side="top")
        self.mise_a_jour_coups_possibles()
        self.valeurs_cases = {}  # Dictionnaire pour stocker les valeurs des cases
        self.assigner_valeurs_cases()  # Appel de la méthode pour assigner les valeurs
        self.nombre_coups = 0
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
        for ligne in range(8):
            for colonne in range(8):
                nom_case = lettres[colonne] + str(ligne + 1)
                self.cases_libres[nom_case] = Label(self.fenetre, text = nom_case, bg = "#{:02x}{:02x}{:02x}".format(5,138,71), fg = "white")
                self.cases_libres[nom_case].place(x = colonne * 75 + 37.5, y = ligne * 75 + 37.5)
        self.creer_pion("D4", "white")
        self.creer_pion("D5", "black")
        self.creer_pion("E4", "black")
        self.creer_pion("E5", "white")
        self.qui_doit_jouer = Label(self.fenetre, text="Tour du joueur : Noir", fg="white")
        self.qui_doit_jouer.pack(side="bottom")

    def assigner_valeurs_cases(self):
        """
        Assigner des valeurs aux cases du plateau.
        """
        valeurs = [
            [500,  -150,   30, 10, 10, 30, -150,  500],
            [-150, -250,    0,  0,  0,  0, -250, -150],
            [30,      0,    1,  2,  2,  1,    0,   30],
            [10,      0,    2, 16, 16,  2,    0,   10],
            [10,      0,    2, 16, 16,  2,    0,   10],
            [30,      0,    1,  2,  2,  1,    0,   30],
            [-150, -250,    0,  0,  0,  0, -250, -150],
            [500,  -150,   30, 10, 10, 30, -150,  500]
        ]
        for i, ligne in enumerate("ABCDEFGH"):
            for j, colonne in enumerate(range(1, 9)):
                nom_case = ligne + str(colonne)
                self.valeurs_cases[nom_case] = valeurs[i][j]
    
    def ligne(self, nom_case):
        """
        Renvoie le numéro de ligne correspondant au nom de la case.
        Args:
            nom_case (str): Le nom de la case.
        Returns:
            int: Le numéro de ligne.
        """
        return int(nom_case[1])

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
        self.nombre_coups += 1
        # Met à jour le nombre de pions
        self.mise_a_jour_nombre_pions()
        self.mise_a_jour_coups_possibles()
        score_evaluation = self.evaluer()
        print("Score de l'évaluation :", score_evaluation)
        
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
    
    def peut_jouerbis(self, nom_case):
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
            # Le pion peut être placé
            return True
        # Aucun pion encadré n'a changé de couleur
        return False  
    
    def compter_pions(self):
        """
        Compte le nombre de pions de chaque joueur sur le plateau.
        Returns:
            dict: Un dictionnaire contenant le nombre de pions pour chaque joueur.
        """
        # Initialiser les compteurs
        pions_noirs = 0
        pions_blancs = 0
        # Parcourir les pions sur le plateau
        for case, pion in self.cases_occupees.items():
            if pion.couleur == "black":
                pions_noirs += 1
            elif pion.couleur == "white":
                pions_blancs += 1
        # Retourner le nombre de pions pour chaque joueur
        return {"black": pions_noirs, "white": pions_blancs}

    def mise_a_jour_nombre_pions(self):
        """
        Met à jour l'affichage du nombre de pions de chaque joueur.
        """
        nombre_de_pions = self.compter_pions()
        self.nombre_pions_label.config(text=f"Pions noirs : {nombre_de_pions['black']}, Pions blancs : {nombre_de_pions['white']}")
        
    def analyser_mobilité(self):
        """
        Analyse la mobilité en comptant le nombre de coups légaux possibles pour chaque joueur.
        Returns:
            dict: Un dictionnaire contenant le nombre de coups légaux pour chaque joueur.
        """
        # Initialiser les compteurs
        mobilite_noirs = 0
        mobilite_blanc = 0
        for nom_case in self.cases_libres:
            if self.peut_jouerbis(nom_case):
                if self.joueur_actuel == "black":
                    mobilite_noirs += 1
                else: 
                    mobilite_blanc += 1
        return {"black": mobilite_noirs, "white": mobilite_blanc}

    def evaluer_force_position(self, couleur):
        """
        Évalue la force d'une position en fonction de la somme des valeurs des cases occupées par la couleur donnée.
        Args:
            couleur (str): La couleur des pions à évaluer ('black' ou 'white').
        Returns:
            int: La force de la position pour la couleur donnée.
        """
        force_position = 0
        for case, pion in self.cases_occupees.items():
            if pion.couleur == couleur:
                force_position += self.valeurs_cases[case]
        return force_position
    
    def evaluer(self):
        """
        Évalue la qualité d'une position dans le jeu Othello en prenant en compte 
        le nombre de pions et la mobilité de chaque joueur.
        Returns:
            float: Le score de l'évaluation de la position, 
                   où un score positif indique un avantage pour les noirs et un score négatif indique un avantage pour les blancs.
        """
        # Déterminer la phase de la partie en fonction du nombre de coups
        if self.nombre_coups <= 12:
            # Phase d'ouverture
            poids_mobilité = 0.4
            poids_position = 0.4
            poids_pions = 0.2
        elif self.nombre_coups <= 48:
            # Milieu de partie
            poids_mobilité = 0.3
            poids_position = 0.3
            poids_pions = 0.4
        else:
            # Fin de partie
            poids_mobilité = 0.2
            poids_position = 0.2
            poids_pions = 0.6
        # Calculer les scores de chaque critère
        score_mobilité = self.analyser_mobilité()[self.joueur_actuel]
        score_position = self.evaluer_force_position(self.joueur_actuel)
        score_pions = self.compter_pions()[self.joueur_actuel]
        # Calculer le score total en combinant les scores pondérés
        score_total = (poids_mobilité * score_mobilité +
                       poids_position * score_position +
                       poids_pions * score_pions)
        # Retourner le score total
        return score_total
        
    def generer_coups_possibles(self, joueur):
        """
        Génère la liste des coups possibles pour le joueur donné dans l'état actuel du plateau.
        Args:
            joueur (str): Le joueur dont on veut générer les coups ("black" ou "white").
        Returns:
            list: La liste des noms de cases où le joueur peut jouer.
        """
        coups_possibles = []
        for nom_case in self.cases_libres:
            if self.peut_jouerbis(nom_case):
                if joueur == "black" and self.joueur_actuel == "black":
                    coups_possibles.append(nom_case)
                elif joueur == "white" and self.joueur_actuel == "white":
                    coups_possibles.append(nom_case)
        return coups_possibles
    
    def mise_a_jour_coups_possibles(self):
        """
        Met à jour l'affichage du nombre de pions de chaque joueur.
        """
        joueur = self.joueur_actuel
        coups = self.generer_coups_possibles(joueur)
        self.coups_label.config(text=f"Coups possibles : {coups}")
    
lancer = Plateau()