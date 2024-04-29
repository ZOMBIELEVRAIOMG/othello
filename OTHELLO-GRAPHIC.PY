from tkinter import Tk, Canvas, Label, messagebox, Button
import random

class Pion:
    def __init__(self, nom_case: str, couleur: str, cercle):
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
    def __init__(self, init_game=True):
        """
        Initialise un objet Plateau.
        """
        self.fenetre = Tk()
        self.fenetre.resizable(width=True, height=True)
        self.canvas = Canvas(self.fenetre, width=600, height=600, bg="#058a47")
        self.canvas.pack()
        self.cases_libres = {}
        self.cases_occupees = {}
        self.nombre_coups = 0
        self.joueur_actuel = 'black'
        self.valeurs_cases = {}
        self.mode_auto = True
        self.nombre_pions_label = Label(self.fenetre, text="", fg="black")
        self.assigner_valeurs_cases()
        self.mode = self.choisir_mode()
        if init_game:
            self.init_game()

    def choisir_mode(self):
        """
        Choix du mode.
        """
        self.fenetre.title("Choisissez le mode de jeu")
        btn_jvj = Button(self.fenetre, text="Joueur vs Joueur", command=lambda: self.set_mode('jvj'))
        btn_jvia_facile = Button(self.fenetre, text="Joueur vs IA (Facile)", command=lambda: self.set_mode('jvia', 'facile'))
        btn_jvia_difficile = Button(self.fenetre, text="Joueur vs IA (Difficile)", command=lambda: self.set_mode('jvia', 'difficile'))
        btn_iaia = Button(self.fenetre, text="IA vs IA", command=lambda: self.set_mode('iaia'))

        btn_jvj.pack(pady=10)
        btn_jvia_facile.pack(pady=10)
        btn_jvia_difficile.pack(pady=10)
        btn_iaia.pack(pady=10)

    def set_mode(self, mode, difficulte=None):
        """
        Fixe le choix du mode et quitte l'interface de menu.
        """
        self.mode = mode
        self.difficulte = difficulte  
        self.fenetre.title("Othello")
        for widget in self.fenetre.winfo_children():
            if isinstance(widget, Button):
                widget.destroy()
        if self.mode == 'iaia':
            Button(self.fenetre, text="Automatique", command=self.enable_auto_mode).pack(side="top")
            Button(self.fenetre, text="Manuel", command=self.disable_auto_mode).pack(side="top")
            Button(self.fenetre, text="Prochain Coup", command=self.effectuer_coup_ordinateur, state="disabled").pack(side="top")

    def init_game(self):
        """
        Création de l'interface graphique et lance le jeu Othello.
        """
        self.dessiner_quadrillage()
        self.assigner_noms_cases()
        self.joueur_actuel = "black"
        self.canvas.bind("<Button-1>", self.jouer_un_pion)
        self.nombre_pions_label = Label(self.fenetre, text="", fg="black")
        self.nombre_pions_label.pack(side="top")
        self.coups_label = Label(self.fenetre, text="", fg="white")
        self.coups_label.pack(side="top")
        self.valeurs_cases = {}
        self.assigner_valeurs_cases()
        self.nombre_coups = 0
        self.mise_a_jour_nombre_pions()
        self.initialiser_pions()
        self.fenetre.mainloop()
        
    def dessiner_quadrillage(self):
        """
        Dessine le quadrillage du plateau de jeu.
        """
        for i in range(8):
            for j in range(8):
                x, y = 75 * j, 75 * i
                self.canvas.create_line(x, 0, x, 600, fill="black", width=4)
                self.canvas.create_line(0, y, 600, y, fill="black", width=4)

    def assigner_noms_cases(self):
        """
        Assigner des noms aux cases du plateau et initialiser la variable qui gère les cases libres.
        """
        lettres = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        for i in range(8):
            for j in range(8):
                nom_case = lettres[j] + str(i + 1)
                self.cases_libres[nom_case] = Label(self.fenetre, text=nom_case, bg="#058a47", fg="white")
                self.cases_libres[nom_case].place(x=j * 75 + 37.5, y=i * 75 + 37.5)

    def initialiser_pions(self):
        """
        Positionne les 4 pions de départ.
        """
        positions_initiales = {'D4': 'white', 'D5': 'black', 'E4': 'black', 'E5': 'white'}
        for pos, couleur in positions_initiales.items():
            self.creer_pion(pos, couleur)
        self.qui_doit_jouer = Label(self.fenetre, text="Tour du joueur : Noir", fg="black")
        self.qui_doit_jouer.pack(side="bottom")
        self.mise_a_jour_apres_coup()

    def assigner_valeurs_cases(self):
        """
        Définie des poids aux cases.
        """
        valeurs = [
            [500, -150, 30, 10, 10, 30, -150, 500],
            [-150, -250, 0, 0, 0, 0, -250, -150],
            [30, 0, 1, 2, 2, 1, 0, 30],
            [10, 0, 2, 16, 16, 2, 0, 10],
            [10, 0, 2, 16, 16, 2, 0, 10],
            [30, 0, 1, 2, 2, 1, 0, 30],
            [-150, -250, 0, 0, 0, 0, -250, -150],
            [500, -150, 30, 10, 10, 30, -150, 500]
        ]
        for i, row in enumerate("ABCDEFGH"):
            for j, col in enumerate(range(1, 9)):
                self.valeurs_cases[row + str(col)] = valeurs[i][j]

    def ligne(self, nom_case: str) -> int:
        """
        Renvoie le numéro de ligne correspondant au nom de la case.
        """
        return int(nom_case[1])

    def colonne(self, nom_case: str) -> int:
        """
        Renvoie le numéro de colonne correspondant au nom de la case.
        """
        return ord(nom_case[0]) - 64

    def creer_pion(self, nom_case: str, couleur: str):
        """
        Crée un pion sur la case spécifiée.
        """
        if nom_case in self.cases_libres:
            self.cases_libres[nom_case].destroy()
            del self.cases_libres[nom_case]
        x, y = (self.colonne(nom_case) - 1) * 75, (self.ligne(nom_case) - 1) * 75
        cercle = self.canvas.create_oval(x + 10, y + 10, x + 65, y + 65, fill=couleur, outline=couleur)
        self.cases_occupees[nom_case] = Pion(nom_case, couleur, cercle)

    # Logique du jeu 
    def jouer_un_pion(self, event):
        if (self.mode == 'jvj') or (self.mode == 'jvia' and self.joueur_actuel == 'black'):
            colonne = event.x // 75
            ligne = event.y // 75
            nom_case = chr(colonne + 65) + str(ligne + 1)
            if self.appliquer_coup(nom_case, self.joueur_actuel):
                self.mise_a_jour_apres_coup()
                if self.mode == 'jvia' and not self.partie_terminee():
                    self.fenetre.after(2000, self.effectuer_coup_ordinateur)            
                
    def appliquer_coup(self, nom_case, joueur):
        if self.peut_jouer(nom_case, True):
            self.creer_pion(nom_case, joueur)
            self.changer_joueur()
            return True
        return False

    def peut_jouer(self, nom_case, jouer_coup):
        if nom_case in self.cases_occupees:
            return False
        pions_a_retourner = self.trouver_pions_a_retourner(nom_case)
        if pions_a_retourner:
            if jouer_coup:
                self.retourner_pions(pions_a_retourner)
            return True
        return False


    def trouver_pions_a_retourner(self, nom_case: str) -> list:
        ligne = self.ligne(nom_case) - 1
        colonne = self.colonne(nom_case) - 1
        couleur_adverse = "white" if self.joueur_actuel == "black" else "black"
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]
        pions_a_retourner = []

        for dir_ligne, dir_colonne in directions:
            pions_potentiels = []
            i = 1
            while True:
                ligne_temp = ligne + dir_ligne * i
                colonne_temp = colonne + dir_colonne * i
                if not (0 <= ligne_temp < 8 and 0 <= colonne_temp < 8):
                    break
                case_temp = chr(colonne_temp + 65) + str(ligne_temp + 1)
                if case_temp not in self.cases_occupees:
                    break
                pion_temp = self.cases_occupees[case_temp]
                if pion_temp.couleur == couleur_adverse:
                    pions_potentiels.append(pion_temp)
                elif pions_potentiels and pion_temp.couleur == self.joueur_actuel:
                    pions_a_retourner.extend(pions_potentiels)
                    break
                else:
                    break
                i += 1
        return pions_a_retourner
                
    def retourner_pions(self, pions_a_retourner: list):
        for pion in pions_a_retourner:
            pion.couleur = self.joueur_actuel
            self.canvas.itemconfig(pion.cercle, fill=self.joueur_actuel, outline=self.joueur_actuel)
            
    def partie_terminee(self) -> bool:
        if not self.generer_coups_possibles("black") and not self.generer_coups_possibles("white"):
            return True
        return False
    
    def annoncer_gagnant(self):
        nombres_pions = self.compter_pions()
        pions_noirs = nombres_pions['black']
        pions_blancs = nombres_pions['white']
        if pions_noirs > pions_blancs:
            gagnant = "Noir"
        elif pions_blancs > pions_noirs:
            gagnant = "Blanc"
        else:
            gagnant = "Match Nul"
        messagebox.showinfo("Fin de la partie", f"La partie est terminée. Le gagnant est le joueur {gagnant}")
        
    # Gestion de l'IA
    def minimax(self, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or self.partie_terminee():
            return None, self.evaluer()
        best_move = None
        if maximizingPlayer:
            maxEval = float('-inf')
            for move in self.generer_coups_possibles(self.joueur_actuel):
                _, eval = self.minimax(depth - 1, alpha, beta, False)
                if eval > maxEval:
                    maxEval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return best_move, maxEval
        else:
            minEval = float('inf')
            for move in self.generer_coups_possibles(self.joueur_actuel):
                _, eval = self.minimax(depth - 1, alpha, beta, True)
                if eval < minEval:
                    minEval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return best_move, minEval
        
    def generer_coups_possibles(self, joueur: str) -> list:
        return [nom_case for nom_case in self.cases_libres if self.peut_jouer(nom_case, False) and self.joueur_actuel == joueur]

    def evaluer(self) -> float:
        phase = self.determiner_phase()
        poids = self.determiner_poids(phase)
        score_mobilité = self.analyser_mobilité()[self.joueur_actuel]
        score_position = self.evaluer_force_position(self.joueur_actuel)
        score_pions = self.compter_pions()[self.joueur_actuel]
        score_total = (poids['mobilité'] * score_mobilité +
                    poids['position'] * score_position +
                    poids['pions'] * score_pions)
        return score_total
    
    def determiner_phase(self) -> str:
        if self.nombre_coups <= 12:
            return 'ouverture'
        elif self.nombre_coups <= 48:
            return 'milieu'
        else:
            return 'fin'
        
    def determiner_poids(self, phase: str) -> dict:
        if phase == 'ouverture':
            return {'mobilité': 0.4, 'position': 0.4, 'pions': 0.2}
        elif phase == 'milieu':
            return {'mobilité': 0.3, 'position': 0.3, 'pions': 0.4}
        else:
            return {'mobilité': 0.2, 'position': 0.2, 'pions': 0.6}

    def analyser_mobilité(self) -> dict:
        mobilite_noirs = 0
        mobilite_blancs = 0
        for nom_case in self.cases_libres:
            if self.peut_jouer(nom_case, False):
                if self.joueur_actuel == "black":
                    mobilite_noirs += 1
                else:
                    mobilite_blancs += 1
        return {"black": mobilite_noirs, "white": mobilite_blancs}

    def evaluer_force_position(self, couleur: str) -> int:
        force_position = sum(self.valeurs_cases[pion.nom_case] for pion in self.cases_occupees.values() if pion.couleur == couleur)
        return force_position

    def compter_pions(self) -> dict:
        pions_noirs = sum(1 for pion in self.cases_occupees.values() if pion.couleur == "black")
        pions_blancs = sum(1 for pion in self.cases_occupees.values() if pion.couleur == "white")
        return {"black": pions_noirs, "white": pions_blancs}

    # Faire jouer l'IA
    def effectuer_coup_ordinateur(self):
        if not self.partie_terminee():
            coup_choisi = None

            if self.mode == 'iaia':
                coup_choisi, _ = self.minimax(5, float('-inf'), float('inf'), self.joueur_actuel == 'black')
            
            elif self.mode == 'jvia':
                if self.difficulte == 'facile':
                    coups_possibles = self.generer_coups_possibles(self.joueur_actuel)
                    coup_choisi = random.choice(coups_possibles) if coups_possibles else None
                elif self.difficulte == 'difficile':
                    coup_choisi, _ = self.minimax(5, float('-inf'), float('inf'), self.joueur_actuel == 'black')

            if coup_choisi:
                self.appliquer_coup(coup_choisi, self.joueur_actuel)
                self.mise_a_jour_apres_coup()
            else:
                self.changer_joueur()

            if not self.partie_terminee():
                if self.mode == 'iaia' and self.mode_auto:
                    self.fenetre.after(1000, self.effectuer_coup_ordinateur)
                elif self.mode == 'jvia' and self.joueur_actuel == 'white':
                    self.fenetre.after(1000, self.effectuer_coup_ordinateur)


    # Gestion des tours
    def changer_joueur(self):
        self.joueur_actuel = 'white' if self.joueur_actuel == 'black' else 'black'
        couleur = 'Noir' if self.joueur_actuel == 'black' else 'Blanc'
        self.qui_doit_jouer.config(text=f"Tour du joueur : {couleur}")
    
    # Gestion du mode iaia
    def enable_auto_mode(self):
        self.mode_auto = True
        self.effectuer_coup_ordinateur()
    
    def disable_auto_mode(self):
        self.mode_auto = False
        for widget in self.fenetre.winfo_children():
            if isinstance(widget, Button) and widget.cget("text") == "Prochain Coup":
                widget.config(state="normal")

    # Mise à jour de l'affichage 
    def mise_a_jour_apres_coup(self):
        self.mise_a_jour_nombre_pions()
        if self.partie_terminee():
            self.annoncer_gagnant()
            
    def mise_a_jour_nombre_pions(self):
        nombre_de_pions = self.compter_pions()
        self.nombre_pions_label.config(text=f"Pions noirs : {nombre_de_pions['black']}, Pions blancs : {nombre_de_pions['white']}")

if __name__ == "__main__":
    jeu = Plateau()