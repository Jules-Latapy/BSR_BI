
class SansObjet:
    class State:
        def __init__(self, nbr_plein, nbr_vide):
            self.nbr_plein = nbr_plein
            self.nbr_vide = nbr_vide

        def proba_plein_global(self):
            return self.nbr_plein / (self.nbr_vide + self.nbr_plein)

        def doit_suicider(self):
            return self.proba_plein_global() < 0.50

        def doit_tirer(self):
            return self.proba_plein_global() >= 0.50


def run_without_objet():
    nbr_plein1 = input("nbr plein:")
    nbr_vide1 = input("nbr vide:")
    state = SansObjet.State(nbr_plein1, nbr_vide1)

    while state.nbr_plein + state.nbr_vide > 1:
        ds = state.doit_suicider()
        if ds:
            print("suicidez-vous")
            result = bool(input("c'était une cartouche pleine ? [true/false]"))
            if result:
                state.nbr_plein = state.nbr_plein - 1
            else:
                state.nbr_vide = state.nbr_vide - 1

        else:
            print("tuez-le")
            result = bool(input("c'était une cartouche pleine ? [true/false]"))
            if result:
                state.nbr_plein = state.nbr_plein - 1
            else:
                state.nbr_vide = state.nbr_vide - 1
            nbVideJouer = input("le donneur joue, entré le nbr de cartouche vide joué:")
            state.nbr_vide = state.nbr_vide - int(nbVideJouer)
            state.nbr_plein = state.nbr_plein - 1