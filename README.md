# OTHELLO

## Présentation
Notre projet consiste à implémenter le jeu de plateau Othello afin qu'il puisse être joué contre une IA.
Réalisé en python et à l'aide du module d'interface graphique tkinter, il peut être joué en 3 modes :
deux joueurs jouant à tour de rôle, un joueur jouant contre une IA, et deux IA jouant l'une contre l'autre.

### Pré-requis
Nécessite une version récente de python pour que tkinter fonctionne.
Vous trouverez 3 fichiers ; 
- OTHELLO-GRAPHIC.PY le fichier contenant le code du jeu
- Makefile le fichier makefile pour lancer le code avec la commande make
- README.md

### Démarage
Dans le terminal, une fois dans le répertoire courant, taper la ligne de commande ```make```

### Description du code
Le code est organisé en deux classes que sont la classe Pion qui définit ce qu'est un pion et la classe Plateau qui initialise un plateau
et permet de lancer le jeu de différentes manières.

La classe Pion est défini par :
- ```self.nom_case``` le nom de la case où se trouve le pion
- ```self.couleur``` la couleur du pion
- ```self.cercle``` la représentation graphique du pion

La classe Plateau est défini par :
- ```self.fenetre``` crée une fenêtre tkinter
- ```self.canvas``` crée un canva
- ```self.cases_libres``` un dictionnaire pour les casses libres où l'on peut placer des pions
- ```self.cases_occupees``` un dictionnaire pour les casses occupées où un pion existe déjà
- ```self.nombre_coups``` compte le nombre de coup afin de permettre à l'IA de choisir le chemin le plus optimal pour elle
- ```self.joueur_actuel`` gère quel joueur doit jouer, les premiers à jouer étant les pions noir, joueur_actuel est noir au début
- ```self.valeurs_cases``` assigne des poids aux cases nécessaire à l'implémenttion de l'IA
- ```self.mode_auto``` permet de savoir si le mode ia vs ia se lance en mode automatique ou manuel
- ```self.nombre_pions_label``` nombre de pions présents sur le plateau au fur et à mesure que le jeu avance
- ```self.mode``` un choix possible entre 3 modes : 2 joueurs, 1 joueur et une ia, 2 ia, le jeu du joueur contre l'IA peut être en mode facile ou difficile
- ```self.init_game``` initialise le jeu

## Auteurs
Mohammed Chakroun

Clément Lukacs

Pierre-Emmanuel Screve

Nora Moreau