from partie1 import*
def pion_adverse(joueur):
    """ Retourne l'entier correspondant à l'adversaire :
    - retourne 2 si joueur vaut 1,
    - retourne 1 si joueur vaut 2.
    Lève une erreur si joueur est différent de 1 et 2.
    """
    assert joueur == 1 or joueur == 2 , "mauvaise valeur de joueur"
    if joueur == 1 :
        return 2
    else :
        return 1

def prise_possible_direction(p, i, j, vertical, horizontal, joueur):
    """ Retourne True si le joueur peut retourner un pion adverse
    dans la direction (vertical,horizontal) en posant un pion dans la case (i,j),
    False sinon.
    :Exemple:
    p = creer_plateau(4)
    prise_possible_direction(p,1,3,0,-1,2) # retourne True
    prise_possible_direction(p,1,3,0,-1,1) # retourne False
    prise_possible_direction(p,1,3,-1,-1,2) # retourne False
    prise_possible_direction(p,1,0,0,1,1) # retourne True
    """
    #on peut prendre toute une ligne de pion adverse si on l'encadre et
    #qu'il n'y a pas de vide (dans la direction)
    #on verifie dans un boucle que la case de la direction est valide et
    #la case n'est pas vide (obligé pour eviter l'erreur de l'assert)
    #et que c'est un pion adverse
    if not case_valide(p, i + vertical, j + horizontal) :
        return False
    if get_case(p, i + vertical, j + horizontal) != pion_adverse(joueur) :
        return False
    while case_valide(p, i + vertical, j + horizontal) and \
    get_case(p, i + vertical, j + horizontal) == pion_adverse(joueur) :
        i += vertical
        j += horizontal
    #sorti de la boucle on regarde la valeur de la case ou on est arrivé
    #vide ou case non valide la prise n'est pas possible
    #sinon c'est un allié on
    if not case_valide(p, i + vertical, j + horizontal) or get_case(p, i + vertical, j + horizontal) == 0 :
        return False
    if get_case(p, i + vertical, j + horizontal) == joueur:
        return True
def mouvement_valide(plateau, i, j, joueur):
    """Retourne True si le joueur peut poser un pion à la case (i,j), False sinon.
    :Exemple:
    p = creer_plateau(4)
    mouvement_valide(p,1,3,2) # retourne True
    mouvement_valide(p,0,0,1) # retourne False
    """
    #un mvt est valide si on pose a une case adjacente ET
    #si on entoure un pion (donc utiliser prise_possible_direction)
    # ET si la case est vide ( = 0 )
    #on regarde ici si la case et valide et si elle est vide
    if not case_valide(plateau, i, j) :
        return False
    if get_case(plateau, i, j) != 0 :
        return False
    #ci-dessous toutes les possibilités de prise_possible_direction
    #si une des direction est possible pour prendre (or) on retourne True
    if not prise_possible_direction(plateau, i, j, 0, 1, joueur) and \
     not prise_possible_direction(plateau, i, j, 0, -1, joueur) and \
     not prise_possible_direction(plateau, i, j, 1, 0, joueur) and \
     not prise_possible_direction(plateau, i, j, 1, 1, joueur) and \
     not prise_possible_direction(plateau, i, j, 1, -1, joueur) and \
     not prise_possible_direction(plateau, i, j, -1, 0, joueur) and \
     not prise_possible_direction(plateau, i, j, -1, 1, joueur) and \
     not prise_possible_direction(plateau, i, j, -1, -1, joueur) :
        return  False
    return True

def mouvement_direction(plateau, i, j, vertical, horizontal, joueur):
    """ Joue le pion du joueur à la case (i,j) si c'est possible.
    :Exemple:
    p = creer_plateau(4)
    mouvement_direction(p,0,3,-1,1,2) # ne modifie rien
    mouvement_direction(p,1,3,0,-1,2) # met la valeur 2 dans la case (1,2)
    """
    #on met a jour le damier si dans la direction donnée on peut prendre un ou des pions
    #on ne test pas la validité du mouvement que cette fct est utilisée dans une autre qui fera le test avant

    if prise_possible_direction(plateau, i, j, vertical, horizontal, joueur) :
        while get_case(plateau, i + vertical, j + horizontal) == pion_adverse(joueur) :
            set_case(plateau, i + vertical, j + horizontal, joueur)
            i += vertical
            j += horizontal

def mouvement(plateau, i, j, joueur):
    """ Ajoute le pion du joueur à la case (i,j) et met à jour le plateau.
    :Exemple:
    p = creer_plateau(4)
    mouvement(p,0,3,2) # ne modifie rien
    mouvement(p,1,3,2) # met la valeur 2 dans les cases (1,2) et (1,3)
    """
    #si le mouvement est possible on pose le pion et ensuite on regarde toutes les direction de prise
    if mouvement_valide(plateau, i, j, joueur) :
        set_case(plateau, i, j, joueur)
        mouvement_direction(plateau, i, j, 0, 1, joueur)
        mouvement_direction(plateau, i, j, 0, -1, joueur)
        mouvement_direction(plateau, i, j, 1, 0, joueur)
        mouvement_direction(plateau, i, j, 1, 1, joueur)
        mouvement_direction(plateau, i, j, 1, -1, joueur)
        mouvement_direction(plateau, i, j, -1, 0, joueur)
        mouvement_direction(plateau, i, j, -1, 1, joueur)
        mouvement_direction(plateau, i, j, -1, -1, joueur)

def joueur_peut_jouer(plateau, joueur):
    """ Retourne True s'il existe une case sur laquelle le joueur peut jouer,
    False sinon.
    :Exemple:
    p = creer_plateau(4)
    joueur_peut_jouer(p,1) # retourne True
    # On remplace les pions du joueur 2 par des pions du joueur 1
    set_case(p,1,1,1)
    set_case(p,2,2,1)
    joueur_peut_jouer(p,1) # retourne False
    """
    jouer = False
    case = 0
    #on va regarder toutes les cases du tableaux
    #si y en a une où on peut jouer on retourne true sinon false
    while case < len(plateau["cases"]) and not jouer:
        #on cherche a retrouver i et j en fct de la case du plateau
        #i (les lignes) c'est le resultat de la dvision entière de la case par la dimension (8, 6, 4)
        #j (les colonnes) c'est le resultat du reste de la meme division entière
        i = case // plateau["n"]
        j = case % plateau["n"]
        if mouvement_valide(plateau, i, j, joueur) :
            jouer = True
            #on pourrait retourner True ici mais ca va interrompre la boucle et dans mes souvenirs c'etait pas forcément bon pour le processur
        case += 1
    return jouer

def fin_de_partie(plateau):
    """ Retourne True si la partie est finie, False sinon.
    :Exemple:
    p = creer_plateau(4)
    fin_de_partie(p) # retourne False
    # On remplace les pions du joueur 2 par des pions du joueur 1
    set_case(p,1,1,1)
    set_case(p,2,2,1)
    fin_de_partie(p) # retourne True
    """
    #la partie est fini quand aucun des joueur ne peut jouer
    return not joueur_peut_jouer(plateau, 1) and not joueur_peut_jouer(plateau, 2)

def gagnant(plateau):
    """ Retourne :
    - 2 si le joueur 2 a plus de pions que le joueur 1,
    - 1 si le joueur 1 a plus de pions que le joueur 2,
    - 0 si égalité.
    :Exemple:
    p = creer_plateau(4)
    # On remplace les pions du joueur 2 par des pions du joueur 1
    set_case(p,1,1,1)
    set_case(p,2,2,1)
    gagnant(p) # retourne 1
    """
    #on va parcourir le plateau et compter les pions
    compteur_noir = 0
    compteur_blanc = 0
    i = 0
    while i < len(plateau["cases"]) :
        if plateau["cases"][i] == 1 :
            compteur_noir += 1
        elif plateau["cases"][i] == 2 :
            compteur_blanc += 1
        i += 1
    if compteur_noir < compteur_blanc : #plus de blanc victoire blanc
        return 2
    elif compteur_blanc < compteur_noir : #plus de noir victoire noir
        return 1
    else : #égalité
         return 0

if __name__ == '__main__':

    p = creer_plateau(4)#on fait pour un petit plateau car c'est plus simple pour les tests

    assert pion_adverse(get_case(p, 2, 1)) == 2 #ici pion noir donc adverse = 2
    assert pion_adverse(get_case(p, 2, 2)) == 1 #ici pion noir donc adverse = 1
    assert not pion_adverse(get_case(p, 1, 2)) == 1 #ici pion noir donc adverse != 1
    assert not pion_adverse(get_case(p, 1, 1)) == 2 #ici pion blanc donc adverse != 2

    assert prise_possible_direction(p, 0, 2, 1, 0, 2)
    assert prise_possible_direction(p, 2, 3, 0, -1, 1)
    assert not prise_possible_direction(p, 3, 3, 1, 1, 1)#mauvaise direction
    assert not prise_possible_direction(p, 0, 3, 1, -1, 2)#pas possible de prendre
    set_case(p, 3, 0, 2)
    assert prise_possible_direction(p, 0, 3, 1, -1, 2)#possible de prendre
    set_case(p, 3, 0, 0)


    assert not mouvement_valide(p, 1, 2, 1)#position deja occupé
    assert not mouvement_valide(p, 3, 3, 2)#pas de prise possible
    assert mouvement_valide(p, 0, 2, 2)#le blanc ici peut retourner un noirs
    assert mouvement_valide(p, 2, 3, 1)#le noir peut prendre un blanc ici

    mouvement_direction(p, 0, 0, 1, 1, 1)#mouvement pas possible donc verifier que rien a changé
    assert get_case(p, 1, 1) == 2 #en 1;1 ca doit etre un blanc (2)
    mouvement_direction(p, 1, 3, 0, -1, 1)#pas possible pour le noir : verif rien a changer
    assert get_case(p, 1, 2) == 1 #en 1;2 ca doit encore etre un noir (1)
    mouvement_direction(p, 1, 0, 0, 1, 1)#mouvement possible donc verifier que case = 1 (noir)
    assert get_case(p, 1, 1) == 1
    mouvement_direction(p, 2, 0, 0, 1, 2)#mouvement possible donc verifier que case = 2 (blanc)
    assert get_case(p, 2, 1) == 2

    p = creer_plateau(4)

    mouvement(p, 0, 0, 1)#pas possible verif que ca a pas changé
    assert get_case(p, 1, 1) == 2
    assert get_case(p, 0, 0) == 0
    mouvement(p, 1, 0, 1)#possible verifier que la case a changé et le pion de la direction possible aussi
    assert get_case(p, 1, 0) == 1
    assert get_case(p, 1, 1) == 1

    assert joueur_peut_jouer(p, 2)
    assert joueur_peut_jouer(p, 1)
    mouvement(p, 3, 2, 1)#on met un noir pour que tous les pions = noirs
    assert not joueur_peut_jouer(p, 1)
    assert not joueur_peut_jouer(p, 2)

    assert fin_de_partie(p) #on peut plus jouer donc c'est fini

    assert gagnant(p) == 1 #y a que des noir donc noir gagnant
    assert not gagnant(p) == 2
    assert not gagnant(p) == 0
    p = creer_plateau(4)
    assert gagnant(p) == 0 #il y a autant donc egalité
    assert not fin_de_partie(p) #on a recréer une partie donc on peut jouer
    set_case(p, 3, 0, 2)
    mouvement(p, 0, 3, 2)
    afficher_plateau(p)
    print("verifier que tout est et qu'il y a a;4 et d;1")
