import numpy

class Pion:
    def __init__(self, nom, couleur = '-'):
        self.nom = nom
        self.couleur = couleur
        
class Othello:
    def __init__(self, plateau = [] ):
        self.listelettre =  ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.listechiffre = ['1', '2', '3', '4', '5', '6', '7', '8']
        self.plateau = plateau
        self.tour = 'Noir'
        self.skippedturn = 0 ###################################################################################################################################
        self.creerPlateau()
        while True:
            print("\n \n")
            if self.skippedturn == 2:
                self.partieFinit()
            self.dicojouable = self.RecupCase()
            self.affichePlateau()
            print(self.dicojouable)
            print("C'est au", self.tour)
            x = self.joue()
            self.coupJoue(x)
        
    
    def creerPlateau(self):
        """initialise le plateau"""
        
        board = [
          ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1'],
          ['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2'],
          ['A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3'],
          ['A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4'],
          ['A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5'],
          ['A6', 'B6', 'C6', 'D6', 'E6', 'F6', 'G6', 'H6'],
          ['A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7'],
          ['A8', 'B8', 'C8', 'D8', 'E8', 'F8', 'G8', 'H8'],
          ]
        
        i = -1
        for ligne in board:
            i += 1
            self.plateau.append([])
            for case in ligne:
                    self.plateau[i].append(Pion(case))
                    
        self.modifPlateau(self.lettreChiffre('D4'), 'B')
        self.modifPlateau(self.lettreChiffre('D5'), 'N')
        self.modifPlateau(self.lettreChiffre('E4'), 'N')
        self.modifPlateau(self.lettreChiffre('E5'), 'B')
              

    def affichePlateau(self):
        """affiche le plateau"""
        listeaffichage = []
        i = -1
        for ligne in self.plateau:
            i += 1
            listeaffichage.append([])
            for pion in ligne:
                listeaffichage[i].append(pion.couleur)
                
                
           
        listeaffichage.insert(0, ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'])   #Pour afficher les ABCD / 1234 sur les côtés
        listeaffichage.insert(9, ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'])
        for i in range(10):
            if i in [0, 9]:
                listeaffichage[i].insert(0, '/')
                listeaffichage[i].insert(9, '/')
                
            elif i in [1, 2, 3, 4, 5, 6, 7, 8]:
                listeaffichage[i].insert(0, i)
                listeaffichage[i].insert(9, i)                               #
            
        print(numpy.matrix(listeaffichage))
        
    def lettreChiffre(self, input):
        """permet de dire A1 au lieu de faire [0][0] pour acceder à une case du plateau"""
        return [self.listechiffre.index(input[1]),self.listelettre.index(input[0])]
            
    
    def modifPlateau(self, input, couleur):
        """modifier une couleur du plateau"""
        self.plateau[input[0]][input[1]].couleur = couleur
        
        
    def RecupCase(self):
        listecase = []
        listeblanc = []
        listenoir = []
        listevide = []
        dicojouable = {}
        for lettre in self.listelettre:
            for chiffre in self.listechiffre:
                case = self.lettreChiffre(lettre + chiffre)
                if self.plateau[case[0]][case[1]].couleur == 'B':
                    listecase.append(self.plateau[case[0]][case[1]].nom)
                    listeblanc.append(self.plateau[case[0]][case[1]].nom)
                if self.plateau[case[0]][case[1]].couleur == 'N':
                    listecase.append(self.plateau[case[0]][case[1]].nom)
                    listenoir.append(self.plateau[case[0]][case[1]].nom)            
        if self.tour == 'Noir':
            for case in listeblanc:
                #print(case,"gd")
                #print(self.listelettre.index(case[0]),self.listechiffre.index(case[1]), 'édz')
                for i in range(3):
                    #print(i, "i::")
                    if self.listechiffre.index(case[1]) - 1 + i < 0:
                        continue
                    if self.listechiffre.index(case[1]) - 1 + i > 7:
                        break
                    for j in range(3):                   #PEUT ETRE A MODIFIER
                        
                        if self.listelettre.index(case[0]) - 1 + j < 0:
                            continue
                        if self.listelettre.index(case[0]) - 1 + j > 7:
                            break
                        
                        #print(self.plateau[self.listechiffre.index(case[1])-1+i][self.listelettre.index(case[0])-1+j].nom, i, j, case,"/")
                        if self.plateau[self.listechiffre.index(case[1])-1+i][self.listelettre.index(case[0])-1+j].couleur == '-' and self.plateau[self.listechiffre.index(case[1])-1+i][self.listelettre.index(case[0])+j-1].nom not in listevide:
                            listevide.append(self.plateau[self.listechiffre.index(case[1])-1+i][self.listelettre.index(case[0])+j-1].nom)
                            #print(listevide)
        else:
            for case in listenoir:
                #print(case,"gd")
                #print(self.listelettre.index(case[0]),self.listechiffre.index(case[1]), 'édz')
                for i in range(3):
                    #print(i, "i::")
                    if self.listechiffre.index(case[1]) - 1 + i < 0:
                        continue
                    if self.listechiffre.index(case[1]) - 1 + i > 7:
                        break
                    for j in range(3):
                        
                        if self.listelettre.index(case[0]) - 1 + j < 0:
                            continue
                        if self.listelettre.index(case[0]) - 1 + j > 7:
                            break
                        if self.plateau[self.listechiffre.index(case[1])-1+i][self.listelettre.index(case[0])-1+j].couleur == '-' and self.plateau[self.listechiffre.index(case[1])-1+i][self.listelettre.index(case[0])+j-1].nom not in listevide:
                            listevide.append(self.plateau[self.listechiffre.index(case[1])-1+i][self.listelettre.index(case[0])+j-1].nom)
        #print(listevide)
        listevide.sort()
        listefiltre2 = []
        print(listevide,'listevide')
        for case in listevide:
            #print(case,'case::')
            dicojouable[case] = []
            dicojouable[case].append(self.enBas(case))
            dicojouable[case].append(self.enHaut(case))
            dicojouable[case].append(self.aGauche(case))
            dicojouable[case].append(self.aDroite(case))
            dicojouable[case].append(self.hautGauche(case))
            dicojouable[case].append(self.hautDroite(case))
            dicojouable[case].append(self.basGauche(case))
            dicojouable[case].append(self.basDroite(case))
            
        for cle, listevaleur in dicojouable.items():
            listefiltre = []
            for valeur in listevaleur:
                if valeur is not None and valeur != []:
                    listefiltre.append(valeur)
            dicojouable[cle] = listefiltre
            if listefiltre == []:
                listefiltre2.append(cle)

        for cle in listefiltre2:
            del dicojouable[cle]
        
        return(dicojouable)                   
        
    def enBas(self, case):
        if self.listechiffre.index(case[1]) == 7:
            return
        listecase = []
        i = 1
        if self.tour =='Noir':
            while self.plateau[self.listechiffre.index(case[1])+i][self.listelettre.index(case[0])].couleur != '-' :
                if self.plateau[self.listechiffre.index(case[1])+i][self.listelettre.index(case[0])].couleur == 'N':
                    return listecase
                listecase.append(self.plateau[self.listechiffre.index(case[1])+i][self.listelettre.index(case[0])].nom)
                if self.listechiffre.index(case[1]) + i == 7:
                    return
                i += 1
        else:
            while self.plateau[self.listechiffre.index(case[1])+i][self.listelettre.index(case[0])].couleur != '-' :
                if self.plateau[self.listechiffre.index(case[1])+i][self.listelettre.index(case[0])].couleur == 'B':
                    return listecase
                listecase.append(self.plateau[self.listechiffre.index(case[1])+i][self.listelettre.index(case[0])].nom)
                if self.listechiffre.index(case[1]) + i == 7:
                    return 
                i += 1
                
    def enHaut(self, case):
        if self.listechiffre.index(case[1]) == 0:
            return
        listecase = []
        i = 1
        if self.tour =='Noir':
            while self.plateau[self.listechiffre.index(case[1])-i][self.listelettre.index(case[0])].couleur != '-' :
                if self.plateau[self.listechiffre.index(case[1])-i][self.listelettre.index(case[0])].couleur == 'N':
                    return listecase
                listecase.append(self.plateau[self.listechiffre.index(case[1])-i][self.listelettre.index(case[0])].nom)
                if self.listechiffre.index(case[1]) - i == 0:
                    return 
                i += 1
        else:
            while self.plateau[self.listechiffre.index(case[1])-i][self.listelettre.index(case[0])].couleur != '-' :
                if self.plateau[self.listechiffre.index(case[1])-i][self.listelettre.index(case[0])].couleur == 'B':
                    return listecase
                listecase.append(self.plateau[self.listechiffre.index(case[1])-i][self.listelettre.index(case[0])].nom)
                if self.listechiffre.index(case[1]) - i == 0:
                    return 
                i += 1
            
    def aGauche(self, case):
        if self.listelettre.index(case[0]) == 0:
            return
        listecase = []
        i = 1
        if self.tour =='Noir':
            while self.plateau[self.listechiffre.index(case[1])][self.listelettre.index(case[0])-i].couleur != '-' :
                #print('tournoir', case)
                if self.plateau[self.listechiffre.index(case[1])][self.listelettre.index(case[0])-i].couleur == 'N':
                    return listecase
                listecase.append(self.plateau[self.listechiffre.index(case[1])][self.listelettre.index(case[0])-i].nom)
                if self.listelettre.index(case[0]) - i == 0:
                    #print('yo')
                    return 
                i += 1
        else:
            #print('tourblanc', case)
            while self.plateau[self.listechiffre.index(case[1])][self.listelettre.index(case[0])-i].couleur != '-' :
                if self.plateau[self.listechiffre.index(case[1])][self.listelettre.index(case[0])-i].couleur == 'B':
                    return listecase
                listecase.append(self.plateau[self.listechiffre.index(case[1])][self.listelettre.index(case[0])-i].nom)
                if self.listelettre.index(case[0]) - i == 0:
                    return 
                i += 1
                
    def aDroite(self, case):
        if self.listelettre.index(case[0]) == 7:
            return
        listecase = []
        i = 1
        #print('a droite', case)
        if self.tour =='Noir':
            while self.plateau[self.listechiffre.index(case[1])][self.listelettre.index(case[0])+i].couleur != '-' :
                if self.plateau[self.listechiffre.index(case[1])][self.listelettre.index(case[0])+i].couleur == 'N':
                    return listecase
                listecase.append(self.plateau[self.listechiffre.index(case[1])][self.listelettre.index(case[0])+i].nom)
                if self.listelettre.index(case[0]) + i == 7:
                    return 
                i += 1
        else:
            #print('tour blanc&&',listecase, case)
            while self.plateau[self.listechiffre.index(case[1])][self.listelettre.index(case[0])+i].couleur != '-' :
                #print('tour blanc',listecase, case)
                if self.plateau[self.listechiffre.index(case[1])][self.listelettre.index(case[0])+i].couleur == 'B':
                    #print('tour blancDD&&',listecase, case)
                    return listecase
                listecase.append(self.plateau[self.listechiffre.index(case[1])][self.listelettre.index(case[0])+i].nom)
                if self.listelettre.index(case[0]) + i == 7:
                    #print('tour blancZZDD&&',listecase, case)
                    return 
                i += 1
                
    def hautGauche(self, case):
        if self.listechiffre.index(case[1]) == 0 or self.listelettre.index(case[0]) == 0:
            return
        listecase = []
        i = 1
        if self.tour =='Noir':
            while self.plateau[self.listechiffre.index(case[1])-i][self.listelettre.index(case[0])-i].couleur != '-' :
                if self.plateau[self.listechiffre.index(case[1])-i][self.listelettre.index(case[0])-i].couleur == 'N':
                    return listecase
                listecase.append(self.plateau[self.listechiffre.index(case[1])-i][self.listelettre.index(case[0])-i].nom)
                if self.listechiffre.index(case[1])-i == 0 or self.listelettre.index(case[0])-i == 0:
                    return 
                i += 1
        else:
            while self.plateau[self.listechiffre.index(case[1])-i][self.listelettre.index(case[0])-i].couleur != '-' :
                if self.plateau[self.listechiffre.index(case[1])-i][self.listelettre.index(case[0])-i].couleur == 'B':
                    return listecase
                listecase.append(self.plateau[self.listechiffre.index(case[1])-i][self.listelettre.index(case[0])-i].nom)
                if self.listechiffre.index(case[1])-i == 0 or self.listelettre.index(case[0])-i == 0:
                    return 
                i += 1
                
    def hautDroite(self, case):
        if self.listechiffre.index(case[1]) == 0 or self.listelettre.index(case[0]) == 7:
            return
        listecase = []
        i = 1
        if self.tour =='Noir':
            while self.plateau[self.listechiffre.index(case[1])-i][self.listelettre.index(case[0])+i].couleur != '-' :
                if self.plateau[self.listechiffre.index(case[1])-i][self.listelettre.index(case[0])+i].couleur == 'N':
                    return listecase
                listecase.append(self.plateau[self.listechiffre.index(case[1])-i][self.listelettre.index(case[0])+i].nom)
                if self.listechiffre.index(case[1])-i == 0 or self.listelettre.index(case[0])+i == 7:
                    return 
                i += 1
        else:
            while self.plateau[self.listechiffre.index(case[1])-i][self.listelettre.index(case[0])+i].couleur != '-' :
                if self.plateau[self.listechiffre.index(case[1])-i][self.listelettre.index(case[0])+i].couleur == 'B':
                    return listecase
                listecase.append(self.plateau[self.listechiffre.index(case[1])-i][self.listelettre.index(case[0])+i].nom)
                if self.listechiffre.index(case[1])-i == 0 or self.listelettre.index(case[0])+i == 7:
                    return 
                i += 1
                
    def basGauche(self, case):
        if self.listechiffre.index(case[1]) == 7 or self.listelettre.index(case[0]) == 0:
            return
        listecase = []
        i = 1
        if self.tour =='Noir':
            while self.plateau[self.listechiffre.index(case[1])+i][self.listelettre.index(case[0])-i].couleur != '-' :
                if self.plateau[self.listechiffre.index(case[1])+i][self.listelettre.index(case[0])-i].couleur == 'N':
                    return listecase
                listecase.append(self.plateau[self.listechiffre.index(case[1])+i][self.listelettre.index(case[0])-i].nom)
                if self.listechiffre.index(case[1])+i == 7 or self.listelettre.index(case[0])-i == 0:
                    return 
                i += 1
        else:
            while self.plateau[self.listechiffre.index(case[1])+i][self.listelettre.index(case[0])-i].couleur != '-' :
                if self.plateau[self.listechiffre.index(case[1])+i][self.listelettre.index(case[0])-i].couleur == 'B':
                    return listecase
                listecase.append(self.plateau[self.listechiffre.index(case[1])+i][self.listelettre.index(case[0])-i].nom)
                if self.listechiffre.index(case[1])+i == 7 or self.listelettre.index(case[0])-i == 0:
                    return  #pas sur ces returns la a voir
                i += 1
                
                
    def basDroite(self, case):
        if self.listechiffre.index(case[1]) == 7 or self.listelettre.index(case[0]) == 7:
            return
        listecase = []
        i = 1
        if self.tour =='Noir':
            while self.plateau[self.listechiffre.index(case[1])+i][self.listelettre.index(case[0])+i].couleur != '-' :
                if self.plateau[self.listechiffre.index(case[1])+i][self.listelettre.index(case[0])+i].couleur == 'N':
                    return listecase
                listecase.append(self.plateau[self.listechiffre.index(case[1])+i][self.listelettre.index(case[0])+i].nom)
                if self.listechiffre.index(case[1])+i == 7 or self.listelettre.index(case[0])+i == 7:
                    return 
                i += 1
        else:
            while self.plateau[self.listechiffre.index(case[1])+i][self.listelettre.index(case[0])+i].couleur != '-' :
                if self.plateau[self.listechiffre.index(case[1])+i][self.listelettre.index(case[0])+i].couleur == 'B':
                    return listecase
                listecase.append(self.plateau[self.listechiffre.index(case[1])+i][self.listelettre.index(case[0])+i].nom)
                if self.listechiffre.index(case[1])+i == 7 or self.listelettre.index(case[0])+i == 7:
                    return 
                i += 1
    
    def joue(self):
        x = None
        if len(self.dicojouable) == 0:
            print('aucun coup jouable pour', self.tour)
            self.skippedturn += 1
            if self.tour =='Noir':
                self.tour ='Blanc'
                return
            else: 
                self.tour = 'Noir'
                return
        self.skippedturn = 0
        while x not in self.dicojouable.keys():
            x = input('Entrez un coup valide: ')
        return x
    
    def coupJoue(self, input):
        if input == None:
            return
        if self.tour =='Noir':
            self.tour ='Blanc'
            self.plateau[self.listechiffre.index(input[1])][self.listelettre.index(input[0])].couleur = 'N'
            for listevaleur in self.dicojouable[input]:
                for valeur in listevaleur:
                    self.plateau[self.listechiffre.index(valeur[1])][self.listelettre.index(valeur[0])].couleur = 'N'
        else:
            self.tour ='Noir'
            self.plateau[self.listechiffre.index(input[1])][self.listelettre.index(input[0])].couleur = 'B'
            for listevaleur in self.dicojouable[input]:
                for valeur in listevaleur:
                    self.plateau[self.listechiffre.index(valeur[1])][self.listelettre.index(valeur[0])].couleur = 'B'
        
                            
    def partieFinit(self):
        compteurblanc = 0
        compteurnoir = 0
        for ligne in self.plateau:
            for case in ligne:
                if self.plateau[case].couleur == 'B':
                    compteurblanc += 1
                elif self.plateau[case].couleur == 'N':
                    compteurnoir += 1
        print('compteur blanc: ', compteurblanc,'\ncompteur noir:', compteurnoir)
        

Jeu = Othello()

         
                