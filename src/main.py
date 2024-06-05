import src.state
from src.state import *


def get_obj() -> Action:
    rep = input("""
    quel objet avez vous ?
    a) telephone    e) clope    i) menotte
    b) pilule       f) biere    j) plus rien
    c) voleur       g) loupe
    d) inverseur    h) scie
    """)
    return {
        "a": Telephone(), "e": Clope(), "i": Menotte(),
        "b": Pilule(), "f": Biere(), "j": None,
        "c": Voleur(), "g": Loupe(),
        "d": Inverseur(), "h": Scie(),
    }[rep]


def get_objs() -> [Action]:
    result = []
    # = tant qu'on a pas none
    while v := get_obj():
        result.append(v)
    return result


def get_obj_donneur() -> Action:
    rep = input("""
    quel objet le donneur à ?
    a) telephone    e) clope    i) menotte
    b) pilule       f) biere    j) plus rien
    c) voleur       g) loupe
    d) inverseur    h) scie
    """)
    return {
        "a": Telephone(), "e": Clope(), "i": Menotte(),
        "b": Pilule(), "f": Biere(), "j": None,
        "c": Voleur(), "g": Loupe(),
        "d": Inverseur(), "h": Scie(),
    }[rep]


def get_objs_donneur() -> [Action]:
    result = []
    # = tant qu'on a pas none
    while v := get_obj_donneur():
        result.append(v)

    return result


def run_with_objet():
    nbr_plein1 = int(input("nbr plein:"))
    nbr_vide1 = int(input("nbr vide:"))
    objets = get_objs()
    objets_donneur = get_objs_donneur()
    vie_max = int(input("vie maximum ?"))
    vie_joueur = int(input("combien de vie possédez-vous ?"))
    vie_donneur = int(input("combien de vie le donneur possède ?"))

    joueur = src.state.Player(objets, 0, vie_max-vie_joueur, False, False)
    donneur = src.state.Player(objets_donneur, 0, vie_max-vie_donneur, False, False)

    state = State(nbr_plein1, nbr_vide1, vie_max, donneur, joueur)

    print("chemin avec le plus de chance de gagner:")
    print(state.roll())


if __name__ == '__main__':
    run_with_objet()
