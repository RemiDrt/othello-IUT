#! /bin/usr/env python
# coding: utf-8
from termcolor.termcolor import *
from colorama.colorama import init #windows
init()#windows
def indice_valide(plateau, indice):
    """ Retourne True si indice est un indice valide de case pour le plateau
    (entre 0 et n-1)
    :Exemple:
    p = creer_plateau(8)
    indice_valide(p,0) # retourne True
    indice_valide(p, 18) # retourne False
    """
    #un plateau de taille n donne un tableau de taille n²
    #un bon indice est dans l'intervalle [0;n-1] car tableau commence a 0
    #n est donné dans avec la clé "n" du dictionnaire représentant le tableau
    if indice < plateau["n"] and indice >= 0 :
        return True
    else:
        return False

def case_valide(plateau, i, j):
    """ Retourne True si (i,j) est une case du plateau (i et j sont des indices
    valides)
    :Exemple:
    p = creer_plateau(8)
    case_valide(p,3,3) # retourne True
    case_valide(p,18,3) # retourne False
    """
    #une case valide a 2 indices valides
    if indice_valide(plateau, i) and indice_valide(plateau, j) :
        return True
    else :
        return False

def get_case(plateau, i, j):
    """ Retourne la valeur de la case (i,j). Erreur si (i,j) n'est pas valide.
    :Exemple:
    p = creer_plateau(4)
    get_case(p,0,0) # retourne 0/2/1 (la case est vide/pion blanc/pion noir)
    get_case(p,1,1) # retourne 0/2/1 (la case est vide/pion blanc/pion noir)
    get_case(p,1,2) # retourne 0/2/1 (la case est vide/pion blanc/pion noir)
    get_case(p,18,3) # lève une erreur
    """
    assert case_valide(plateau, i, j),"coordonées de la case inexistantes"
    #n (obtenue avec le dictionnaire) le format du plateau (8 6 4)
    #l'indice dans le tableau c'est (n (format du plateau) * ligne) + colonne
    #les numeros de cases d'une ligne i sont dans [n*i ; n*i + (n-1)]
    indice_case = (plateau["n"] * i) + j
    return plateau["cases"][indice_case]

def set_case(plateau, i, j, val):
    """ Affecte la valeur val dans la case (i,j). Erreur si (i,j) n'est pas une case
    ou si val n'est pas entre 0 et 2.
    Met aussi à jour le nombre de cases libres (sans pion).
    :Exemple:
    p = creer_plateau(4)
    set_case(p,0,0,1) # met un pion noir (i.e., met la valeur 1) dans la case (0,0)
    set_case(p,1,2,0) # enlève le pion (i.e., met la valeur 0) dans la case (1,2)
    set_case(p,18,3,1) # lève une erreur
    set_case(p,2,3,6) # lève une erreur
    """
    assert case_valide(plateau, i, j) and (val == 2 or val == 1 or val == 0),"coordonées inexistantes ou valeur inexistante"
    indice_case = (plateau["n"] * i) + j
    plateau["cases"][indice_case] = val

def creer_plateau(n):
    """Retourne une nouvelle partie. Lève une erreur si n est différent de 4, 6 ou 8.
    Une partie est un dictionnaire contenant :
    - n : valeur passée en paramètre
    - cases : tableau de n*n cases initialisées
    :Exemple:
    creer_plateau(4) retourne un dictionnaire contenant les entrées (couples clés/val
    - n : 4
    - cases : [0, 0, 0, 0, 0, 2, 1, 0, 0, 1, 2, 0, 0, 0, 0, 0]
    """

    assert n == 4 or n == 6 or n == 8,"dimensions disponibles : 4x4 6x6 8x8"
    i=0
    cases=[]
    while i < n ** 2 :
        cases.append(0)
        i = i + 1
    plateau = {"n" : n, "cases" : cases}
    #les 4 cases a remplir aux debut sont les combinaisons des indices n/2 et (n/2)-1
    #on fait les divisions d'entiers pour pas avoir de float dans les indices
    set_case(plateau, n//2, n//2, 2)
    set_case(plateau, (n//2)-1, (n//2)-1, 2)
    set_case(plateau, n//2, (n//2)-1, 1)
    set_case(plateau, (n//2)-1, n//2, 1)
    return plateau


def afficher_plateau(plateau) :
	"""Affiche le plateau à l'écran"""

	#constru ligne des vals colonne
	i = 0
	ligne = "   "
	while i < plateau["n"] :
		ligne += "   " + str(i + 1) + "   "
		i += 1
	print(ligne)
	#constru ligne_val + ligne_space
	i = 0
	color_equipe = 'white'

	while i < plateau["n"] :

		j = 0
		ligne_val = " " + chr(97+i) + " " #chr pour afficher les coordonnées avec lettre
		ligne_transi = "   "#il y a 3 "places" avant d'avoir le plateau
		while j < plateau["n"] :
			val = "   " #on initialise la valeur d'une case a 3 espaces de base (=0)
			if get_case(plateau, i, j) == 1 :
				color_equipe = 'grey' #les noirs sont affichés en gris
				val = "###"#la valeur pour 2 ou 1 est ###
			elif get_case(plateau, i, j) == 2 :
				color_equipe = 'white'#les blancs sont couleur blanche
				val = "###"
			if (i + j) % 2 == 1 : #indice impaire (pour alternance couleur)
				chaine_space = colored("       ", 'cyan', 'on_cyan')
				chaine_val = colored("  " + val + "  ", color_equipe, 'on_cyan')

			else :
				chaine_space = colored("       ", 'magenta', 'on_magenta')
				chaine_val = colored("  " + val + "  ", color_equipe, 'on_magenta')
			#chaine = une case (1/3 de hauteur)
			#une ligne = toutes les cases
			ligne_transi += chaine_space
			ligne_val += chaine_val

			j = j + 1
		#ici on combine chaque tiers pour avoir un ligne de case complete
		print(ligne_transi)
		print(ligne_val)
		print(ligne_transi)
		i = i + 1

if __name__ == '__main__':
	p = creer_plateau(8)
	#test indice_valide pour 8x8
	i = -2
	while i < 10 :
		if i >= 0 and i < 8 :
				assert indice_valide(p, i)
		else :
				assert not indice_valide(p, i)
		i += 1
	print("arriver ici sans error = passer les test indice d'un plateau 8x8")
	#test case_valide pour 8x8
	assert case_valide(p, 5, 5) #2 bien vers milieu i=j
	assert case_valide(p, 0, 0) #2 bien vers bas lim i=j
	assert not case_valide(p, -1, -3) #2 pas bien trop petit

	print("arriver ici sans error = passer les test case d'un plateau 8x8")
	#la fct get_case contient un assert verifiant la validité  de la case fct qui fonctionne 	d'apres les test précédents donc ici on test les valeurs retrounés et pas les indices entrés
	assert get_case(p , 0, 0) == p["cases"][0] == 0#la premiere
	assert get_case(p , 7, 7) == p["cases"][63] == 0#la dernière
	assert not get_case(p ,5 ,6 ) == 3 #un mauvaise valeur
	assert not get_case(p ,1 ,0 ) == -3 #un mauvaise valeur
	assert get_case(p ,4 ,4 ) == 2 #la bon setup de départ
	print("arriver ici sans error = passer les test get_case d'un plateau 8x8")
	#la fct set_case contient un assert verifiant la validité  de la valeur donné donc ici on 	test les valeurs le bon changement de valeur des cases par la validité de la valeur ni la 	validité des indices verifiés au dessus
	set_case(p, 0, 0, 1)
	assert get_case(p, 0, 0) == 1
	set_case(p, 7, 7, 2)
	assert get_case(p, 7, 7) == 2
	print("arriver ici sans error = passer les test set_case d'un plateau 8x8")

	assert p["n"] == 8
	assert len(p["cases"]) == 8*8
	assert get_case(p ,4 ,4 ) == 2 #la bon setup de départ
	assert get_case(p ,3 ,3 ) == 2 #la bon setup de départ
	assert get_case(p ,4 ,3 ) == 1 #la bon setup de départ
	assert get_case(p ,3 ,4 ) == 1 #la bon setup de départ
	print("arriver ici sans error = passer les test creer_plateau d'un plateau 8x8")
	set_case(p ,0 ,0 ,1)
	set_case(p ,7 ,7 ,2)
	afficher_plateau(p)
	print("si affichage bon + valeur setup + 1ere case=noir et derniere=blanche : 	afficher_plateau est bon pour un 8x8")
