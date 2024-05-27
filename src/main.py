from src.state import *


def get_obj() -> Action:
    rep = input("""
    quel objet avez vous ?
    a) telephone    e) clope    i) menotte
    b) pilule       f) biere    j) none
    c) voleur       g) loupe
    d) inverseur    h) scie
    """)
    return {
        "a": Telephone(), "e": Clope(), "i": Menotte(),
        "b": Pilule(),    "f": Biere(), "j": None,
        "c": Voleur(),    "g": Loupe(),
        "d": Inverseur(), "h": Scie(),
    }[rep]


def get_objs() -> [Action]:
    result = []
    # = tant qu'on a pas none
    while v := get_obj():
        result.append(v)


def get_obj_donneur() -> Action:
    rep = input("""
    quel objet le donneur à ?
    a) telephone    e) clope    i) menotte
    b) pilule       f) biere    j) none
    c) voleur       g) loupe
    d) inverseur    h) scie
    """)
    return {
        "a": Telephone(), "e": Clope(), "i": Menotte(),
        "b": Pilule(),    "f": Biere(), "j": None,
        "c": Voleur(),    "g": Loupe(),
        "d": Inverseur(), "h": Scie(),
    }[rep]


def get_objs_donneur() -> [Action]:
    result = []
    # = tant qu'on a pas none
    while v := get_obj_donneur():
        result.append(v)


def run_with_objet():
    nbr_plein1 = input("nbr plein:")
    nbr_vide1 = input("nbr vide:")
    objets = get_objs()
    objets_donneur = get_objs_donneur()
    vie = int(input("combien de vie possédez-vous ?"))
    vie_donneur = int(input("combien de vie le donneur possède ?"))

    state = State(nbr_plein1, nbr_vide1, objets, objets_donneur, vie, vie_donneur)

    print("chemin avec le plus de chance de gagner:")
    print(state.roll())
