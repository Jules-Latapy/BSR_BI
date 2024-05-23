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


class AvecObjet:
    class State:
        def __init__(self, nbr_plein, nbr_vide, objets, objets_donneur, vie, vie_donneur):
            self.nbr_plein = nbr_plein
            self.nbr_vide = nbr_vide
            self.objets_donneur = objets_donneur
            self.objets = objets
            self.vie = vie
            self.vie_donneur = vie_donneur

        def proba_plein_global(self):
            return self.nbr_plein / (self.nbr_vide + self.nbr_plein)

        def doit_suicider(self):
            return self.proba_plein_global() < 50

        def doit_tirer(self):
            return self.proba_plein_global() >= 50

        def roll(self):
            for o in self.objets:
                o.utilise(self)

    class Objet:
        def utilise(state):
            raise "unimplemented"

    class Telephone(Objet):
        def utilise(state):
            pass

    class Pilule(Objet):
        def utilise(state):
            pass

    class Voleur(Objet):
        def utilise(state):
            pass

    class Inverseur(Objet):
        def utilise(state):
            pass

    class Clope(Objet):
        def utilise(state):
            pass

    class Biere(Objet):
        def utilise(state):
            pass

    class Loupe(Objet):
        def utilise(state):
            pass

    class Scie(Objet):
        def utilise(state):
            pass

    class Menotte(Objet):
        def utilise(state):
            pass
