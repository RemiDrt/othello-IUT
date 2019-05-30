#! /bin/usr/env python
# coding: utf-8
from json import dumps, loads
import os
from partie2 import *

def effacer_terminal():
    """ Efface le terminal. """
    #os.system('clear') #pour linux
    os.system('cls') #pour Windows

def creer_partie(n):
    """ Crée une partie. Une partie est un dictionnaire contenant :
    - le joueur dont c'est le tour (clé joueur) initialisé à 1,
    - le plateau (clé plateau).
    :Exemple:
    creer_partie(4) retourne un dictionnaire contenant les entrées
    (couples clés/valeurs) :
    - joueur : 1
    - plateau : {
    - n : 4,
    - cases : [0, 0, 0, 0, 0, 2, 1, 0, 0, 1, 2, 0, 0, 0, 0, 0]
    }
    """
    partie = { "joueur" : 1 , "plateau" : creer_plateau(n) }
    return partie


def saisie_valide(partie, s):
    """ Retourne True si la chaîne s correspond à un mouvement valide pour le joueur
    et False sinon.
    La chaîne s est valide si :
    - s est égal à la lettre M ou
    - s correspond à une case (de la forme a1 pour la case (0,0), ..., h8 pour la cas
    où le joueur courant peut poser son pion.
    :Exemple:
    p = creer_partie(4)
    saisie_valide(p, "M") # retourne True
    saisie_valide(p, "b1") # retourne True
    saisie_valide(p, "b4") # return False
    """
    if s == "M" :
        return True
    #ord('a') = 97 donc pour associer la lettre a la valeur il faut enlever 97
    #on regarde si avec i = ord(s[0]) - 97 et j = int(s[1]) on a un mvt valide
    #si le joueur a mal saisi la fct mouvement_valide va retourner false
    if len(s) != 2 :
        return False
    if ord(s[1]) > 57 or ord(s[1]) < 48 :
        #ce n'est pas un chiffre donc retourne false cf table ascii
        #on fait ce test pour eviter erreur quand on converti en int
        return False
    i = ord(s[0]) - ord("a")
    j = int(s[1]) - 1
    return mouvement_valide(partie["plateau"], i, j, partie["joueur"] )

def tour_jeu(partie):
    """ Effectue un tour de jeu :
    - efface le terminal,
    - affiche le plateau,
    - si le joueur courant peut jouer, effectue la saisie d'un mouvement valide
    (saisie contrôlée),
    - Effectue le mouvement sur le plateau de jeu,
    - Retourne True si le joueur courant a joué ou False s'il souhaite accéder
    au menu principal.
    :Exemple:
    p = creer_partie(4)
    tour_jeu(p)
    #Si l'utilisateur a saisi b1, alors p vaut :
    {
    "joueur" : 1,
    "plateau" : {
    "n" : 4,
    "cases" : [0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 2, 0, 0, 0, 0, 0]
    }
    }
    """
    effacer_terminal()
    afficher_plateau(partie["plateau"])
    #ici : cas ou le joueur ne peut pas jouer (on lui laisse quand même le choix de retourner au menu)
    #s'il veut continuer la partie on retourne True sans rien faire
    if not joueur_peut_jouer(partie["plateau"], partie["joueur"]) :
        print("joueur " + str(partie["joueur"]) + " ne peut pas joueur, saisir M pour revenir au menu ou n'importe quoi pour passer votre tour")
        saisi = input()
        if saisi == "M" :
            return False
        else :
            return True
    #cas ou le joueur peut jouer on retourne false s'il veut retourner au menu et true s'il a saisi un bon mouvement (apres avoir effectué le mouvement)
    else :
        saisi = "11"
        #on initialise saisi sur une mauvaise valeur pour rentrer dans la boucle de verification automatiquement
        while not saisie_valide(partie, saisi) :
            print("joueur " + str(partie["joueur"]) + " : \n\t-saisir M pour retourner au menu \n\t-saisir un mouvement valide : letrre correspondant à la ligne et chiffre correspondant à la colonne (ex : b2)")
            saisi = input()
        if saisi == "M" :
            return False
        else :
            mouvement(partie["plateau"], ord(saisi[0]) - ord("a"), int(saisi[1]) - 1, partie["joueur"] )
            effacer_terminal()
            afficher_plateau(partie["plateau"])
            return True
def saisir_action(partie):
    """ Retourne le choix du joueur pour menu (saisie contrôlée):
    - 0 pour terminer le jeu,
    - 1 pour commencer une nouvelle partie,
    - 2 pour charger une partie,
    - 3 pour sauvegarder une partie (si une partie est en cours),
    - 4 pour reprendre la partie (si une partie est en cours).
    :Exemple:
    n = saisir_action(None)
    n est un entier compris entre 0 et 2 inclus.
    """
    #on laisse tout en chaine de caractere jusquau retourne pour eviter les erreur de conversion
    saisi = ""
    if partie is None :
        while saisi != "0" and saisi != "1" and saisi != "2" :
            print("saisir une action :\n\t- 0 pour terminer le jeu,\n\t- 1 pour commencer une nouvelle partie\n\t- 2 pour charger une partie")
            saisi = input()
        return int(saisi)
    else :
        while saisi != "0" and saisi != "1" and saisi != "2" and saisi != "3" and saisi != "4" :
            print("saisir une action :\n\t- 0 pour terminer le jeu,\n\t- 1 pour commencer une nouvelle partie\n\t- 2 pour charger une partie\n\t- 3 pour sauvegarder une partie\n\t- 4 pour reprendre la partie.")
            saisi = input()
        return int(saisi)

def jouer(partie) :
    """ Permet de jouer à la partie en cours (passée en paramètre).
    Retourne True si la partie est terminée, False sinon.
    :Exemple:
    p = creer_partie(4)
    res = jouer(p)
    Si res vaut True, alors les deux joueurs ont fait une partie entière d'Othello
    sur une grille 4 * 4.
    """
    #une partie continue tant qu'elle n'est pas fini ou que la fct tour_jeu revoit false (retourner au menu)
    #on utilise une variable continuer initialisé a True pour rentrer dans la boucle et qui sera ensuite equivalent tour_jeu
    continuer = True
    while not fin_de_partie(partie["plateau"]) and continuer :
        #on fait un tour
        continuer = tour_jeu(partie)
        #on augmenter change de joueur
        partie["joueur"] += 1
        #quand on depasse 2 on revient a 1
        if partie["joueur"] > 2 :
            partie["joueur"] = 1
    #en sortant de la boucle soit la partie est fini (retourner true) soit le joueur revient au menu (retourner False)
    return fin_de_partie(partie["plateau"])

def saisir_taille_plateau():
    """ Fait saisir un nombre parmi 4,6 ou 8 (saisie contrôlée).
    :Exemple:
    n = saisir_taille_plateau()
    n est un entier égal à 4, 6 ou 8.
    """
    taille = 0
    while taille != 4 and taille != 6 and taille != 8 :
        print("Saisir la taille du plateau : 4, 6 ou 8")
        taille = int(input())
    return taille

def sauvegarder_partie(partie):
    """ Sauvegarde la partie passée en paramètre au format json
    dans le fichier sauvegarde_partie.json
    :Exemple:
    p = creer_partie(4)
    sauvegarder_partie(p)
    Le fichier sauvegarde_partie.json doit contenir :
    {"joueur": 1, "plateau": {"n": 4, "cases": [0, 0, 0, 0, 0, 2, 1, 0, 0, 1, 2, 0,
    0, 0, 0, 0]}}
    """
    fichier = dumps(partie)
    f = open("sauvegarde_partie.json", "w")
    f.write(fichier)
    f.close()

def charger_partie():
    """ Crée la partie à partir des données du fichier sauvegarde_partie.json
    ou crée une nouvelle partie 4*4.
    Retourne la partie créée.
    :Exemple:
    p = charger_partie()
    Si le fichier sauvegarde_partie.json contient :
    {"joueur": 1, "plateau": {"n": 4, "cases": [0, 0, 0, 0, 0, 2, 1, 0, 0, 1, 2, 0,
    0, 0, 0, 0]}}
    alors p correspond à une nouvelle partie
    """
    if os.path.exists("sauvegarde_partie.json"):
        print("Le fichier sauvegarde_partie.json existe.")
        fichier = open("sauvegarde_partie.json", "r")
        chaine = fichier.read()
        fichier.close()
        partie = loads(chaine)
        return partie
    else:
        print("Le fichier sauvegarde_partie.json n'existe pas.")
        return creer_partie(4)

def othello():
    """ Fonction permettant de jouer à Othello. On peut enchaîner, sauvegarder,
    charger et recommencer des parties d'Othello.
    :Exemple:
    othello()
    """
    p = None
    action = saisir_action(p)
    #on joue au jeux tant qu'on a pas saisi 0 (pour terminer)
    while action != 0 :
        if action == 1 :
            #on crée une partie p
            n = saisir_taille_plateau()
            p = creer_partie(n)
            #on joue
            res = jouer(p)
            #si la partie se fini p devient none pour la saisi de l'action
            if res :
                if gagnant(p["plateau"]) == 0 :
                    print("égalité")
                else :
                    print("joueur " + str(gagnant(p["plateau"])) + " a gagné la partie")
                p = None
        elif action == 2 :
            #on charge une partie
            p = charger_partie()
            #on joue
            res = jouer(p)
            #si la partie se fini p devient none pour la saisi de l'action
            if res :
                if gagnant(p["plateau"]) == 0 :
                    print("égalité")
                else :
                    print("joueur " + str(gagnant(p["plateau"])) + " a gagné la partie")
                p = None
        elif action == 3 :
            #on sauvegarde la partie
            sauvegarder_partie(p)
        elif action == 4 :
            #on reprend la partie en cours
            res = jouer(p)
            if res :
                if gagnant(p["plateau"]) == 0 :
                    print("égalité")
                else :
                    print("joueur " + str(gagnant(p["plateau"])) + " a gagné la partie")
                p = None
        action = saisir_action(p)



if __name__ == '__main__':
    print("phase de test : verifier les saisies controlées")
    assert creer_partie(4)["plateau"]["n"] == 4
    assert not creer_partie(4)["plateau"]["n"] == 6
    assert creer_partie(8)["plateau"]["n"] == 8
    assert creer_partie(8)["joueur"] == 1
    assert not creer_partie(8)["joueur"] == 2

    p = creer_partie(4)
    tour_jeu(p)
    effacer_terminal()
    p = creer_partie(4)
    assert saisie_valide(p, "M")
    assert not saisie_valide(p, "m")
    assert not saisie_valide(p,"b2")
    assert not saisie_valide(p,"1a")
    assert saisie_valide(p, "b1")

    saisir_action(p)
    p = None
    saisir_action(p)
    p = charger_partie()
    set_case(p["plateau"], 3, 3, 2)
    sauvegarder_partie(p)
    p = charger_partie()
    assert get_case(p["plateau"], 3, 3) == 2
    saisir_taille_plateau()
    print("vous avez tout testé sans erreur")
