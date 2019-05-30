# coding: utf-8
from termcolor.termcolor import *
def aff_simple(plateau) :
    i = 0
    while i < plateau["n"] :
        j = 0
        chaine = ""
        while j < plateau["n"] :
            if j != plateau["n"] - 1 :
                chaine += str(get_case(plateau, i, j)) + "  "
            else :
                chaine += str(get_case(plateau, i, j)) #on evite les 2 espaces pour le dernier 
            j = j + 1
        print(chaine)
        i = i +1
        
def aff_moyen(plateau):
    chaine_etoile = ""
    chaine_transi = ""
    chaine_val = ""
    k = 0
    while k < plateau["n"] :
        
        if k == plateau["n"] - 1 :
            chaine_transi += "*      *"
            chaine_etoile += "********"
        else :
            chaine_etoile += "*******"
            chaine_transi += "*      "
            
        k = k + 1
    print(chaine_etoile)
    i = 0
    while i < plateau["n"] :
        j = 0
        chaine = "*"
        while j < plateau["n"] :            
            val_case=" "
            if get_case(plateau,i,j) == 2 :
                val_case = "B"
            elif get_case(plateau,i,j) == 1 :
                val_case = "N"
            chaine += "  " + val_case + "   *"        
            j = j + 1
        print(chaine_transi)
        print(chaine)
        print(chaine_transi)
        print(chaine_etoile)
        i = i + 1
def aff_diff(plateau) :
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
		ligne_val = " " + chr(97+i) + " "
		ligne_transi = "   "
		while j < plateau["n"] :
			val = "   "
			if get_case(plateau, i, j) == 1 :
				color_equipe = 'grey'
				val = "###"
			elif get_case(plateau, i, j) == 2 :
				color_equipe = 'white'
				val = "###"
			if (i + j) % 2 == 1 : #indice impaire (pour alternance couleur)
				chaine_space = colored("       ", 'cyan', 'on_cyan')
				chaine_val = colored("  " + val + "  ", color_equipe, 'on_cyan')
			
			else :
				chaine_space = colored("       ", 'magenta', 'on_magenta') 
				chaine_val = colored("  " + val + "  ", color_equipe, 'on_magenta')
			ligne_transi += chaine_space
			ligne_val += chaine_val
			
			j = j + 1
			
		print(ligne_transi)
		print(ligne_val)
		print(ligne_transi)
		i = i + 1
