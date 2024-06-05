from copy import deepcopy

from src.tree import Tree

# todo gerer mieux le telephone et les probas individuel
"""
cartouche: [1,0]
objet [biere]
action [biere, assassinat, suicide]
                      proba
                        |
            +- [a] -> (0.5) donneur perds une vie --+-- [s] -> (1) enleve une vide
            |      -> (0.5) donneur perds rien      +-- [b] -> (1) enleve une vide
            |                   |                   +-- [a] -> (1) donneur ne perds rien
            |                   |
            |                   +---[changement]----+-- [s] -> (1) donneur perds une vie
            |                                       +-- [a] -> (1) joueur perds une vie
    root ---+- [s] -> (0.5) perds une vie 
            |      -> (0.5) enleve une pleine
            |
            +- [b] -> (0.5) enleve une pleine
                   -> (0.5) enleve une vide
"""


class Player:
    def __init__(self, objets, vie_gagne, vie_perdu, is_opponent_chained, is_silled):
        self.objets = objets
        self.vie_gagne = vie_gagne
        self.vie_perdu = vie_perdu
        self.is_opponent_chained = is_opponent_chained
        self.is_silled = is_silled
        self.revealed_ball = {}

        self.objets.append(Assassiner())
        self.objets.append(Suicider())

    def as_lost(self, vie_max):
        return self.vie_gagne + self.vie_perdu + vie_max <= 0


class State:
    """
    Represent l'état du jeu
    """

    def __init__(self, nbr_plein, nbr_vide, vie_max, dealer: Player, player: Player, name="root", proba=1):
        self.nbr_plein = nbr_plein
        self.nbr_vide = nbr_vide
        self.vie_max = vie_max
        self.dealer = dealer
        self.player = player
        self.playerActu = player
        self.name = name
        self.proba = proba

    def change_role(self):
        if self.playerActu == self.player:
            self.playerActu = self.dealer
        else:
            self.playerActu = self.player

    def opponent(self) -> Player:
        if self.playerActu == self.player:
            return self.dealer
        else:
            return self.player

    def nbr_cartouche(self):
        return self.nbr_vide + self.nbr_plein

    def proba_plein_global(self):
        return self.nbr_plein / self.nbr_cartouche()

    def roll(self) -> (Tree | None):
        """
        Genere l'arbre des possibilitées avec toutes les combinaisons d'objet possible
        :return: Tree
        """
        # le tour est finis, il n'y a plus de strategies à appliquer
        if self.nbr_cartouche() <= 0 \
                or (self.player.as_lost(self.vie_max)) \
                or (self.dealer.as_lost(self.vie_max)) \
                or self.proba <= 0:
            return None

        result = Tree(self, [])

        for objet in self.playerActu.objets:
            if objet.is_needed(self):
                # on doit controller l'évolution de l'objet state,
                # c'est donc mieux de copier l'objet
                result.childs.extend(objet.construire_proba_graph(deepcopy(self)).childs)

        return result

    def find_best_solution(self, tree: Tree) -> []:
        """
        c'est quoi le meilleur chemin ?
        un chemin ou on est le plus sur ?
        ou un chemin ou on gagne le plus ?

        :param tree:
        :return:
        """
        pass


class Action:
    """
    Represente un choix possible
    """

    def is_needed(self, state: State) -> bool:
        """
        règles de gestion:
            c'est ici qu'on viendra optimiser et appliquer les strategies
        """
        return True

    def construire_proba_graph(self, state: State) -> Tree:
        """
        pour cette action quel sont les possibilité derriere ?
        :param state:
        :return:
        """
        raise "unimplemented"


class Assassiner(Action):
    def construire_proba_graph(self, state) -> Tree:
        state.name = "Assassiner"
        state.proba = 1

        next_state_true = deepcopy(state)
        next_state_true.name = "tué marche"
        next_state_true.proba = state.playerActu.revealed_ball.get(state.nbr_cartouche() - 1,
                                                                   state.proba_plein_global())
        next_state_true.nbr_plein -= 1

        if next_state_true.playerActu.is_silled:
            next_state_true.opponent().vie_perdu += 2
            next_state_true.playerActu.is_silled = False
        else:
            next_state_true.opponent().vie_perdu += 1

        if not next_state_true.playerActu.is_opponent_chained:
            next_state_true.change_role()
        else:
            next_state_true.playerActu.is_opponent_chained = False

        # --------------------------------------------------------

        next_state_false = deepcopy(state)
        next_state_false.name = "tué marche pas"
        next_state_false.proba = 1 - state.playerActu.revealed_ball.get(state.nbr_cartouche() - 1,
                                                                        state.proba_plein_global())
        next_state_false.nbr_vide -= 1

        if next_state_false.playerActu.is_silled:
            next_state_false.playerActu.is_silled = False

        if not next_state_false.playerActu.is_opponent_chained:
            next_state_false.change_role()
        else:
            next_state_false.playerActu.is_opponent_chained = False
        # --------------------------------------------------------

        return Tree(state, [
            Tree(next_state_true, [next_state_true.roll()]),
            Tree(next_state_false, [next_state_false.roll()]),
        ])


class Suicider(Action):
    def construire_proba_graph(self, state) -> Tree:
        state.name = "Suicider"
        state.proba = 1

        next_state_true = deepcopy(state)
        next_state_true.name = "Suicide marche"
        next_state_true.proba = state.playerActu.revealed_ball.get(state.nbr_cartouche() - 1,
                                                                   state.proba_plein_global())
        next_state_true.nbr_vide -= 1

        if next_state_true.playerActu.is_silled:
            next_state_true.playerActu.is_silled = False

        # --------------------------------------------------------

        next_state_false = deepcopy(state)
        next_state_false.name = "Suicide marche pas"
        next_state_false.proba = 1 - state.playerActu.revealed_ball.get(state.nbr_cartouche() - 1,
                                                                        state.proba_plein_global())
        next_state_false.playerActu.vie_perdu += 2 if next_state_false.playerActu.is_silled else 1
        next_state_false.nbr_plein -= 1

        if next_state_false.playerActu.is_silled:
            next_state_false.playerActu.vie_perdu += 2
            next_state_false.playerActu.is_silled = False
        else:
            next_state_false.playerActu.vie_perdu += 1

        if not next_state_false.playerActu.is_opponent_chained:
            next_state_false.change_role()
        else:
            next_state_false.playerActu.is_opponent_chained = False

        # --------------------------------------------------------

        return Tree(state, [
            Tree(next_state_true, [next_state_true.roll()]),
            Tree(next_state_false, [next_state_false.roll()]),
        ])


class Telephone(Action):
    def construire_proba_graph(self, state) -> Tree:
        state.playerActu.objets.remove(self)
        state.name = "Telephone"
        state.proba = 1

        result = []

        for i in range(state.nbr_cartouche()):
            next_state_true = deepcopy(state)
            next_state_true.name = "Telephone[" + i.__str__() + ", true]"
            next_state_true.playerActu.revealed_ball[i] = 1

            next_state_false = deepcopy(state)
            next_state_false.name = "Telephone[" + i.__str__() + ", false]"
            next_state_false.playerActu.revealed_ball[i] = 0

            result.append(Tree(next_state_true, [next_state_true.roll()]))
            result.append(Tree(next_state_false, [next_state_false.roll()]))

        return Tree(State, result)


class Pilule(Action):
    def construire_proba_graph(self, state) -> Tree:
        state.playerActu.objets.remove(self)
        state.name = "Pilule"
        state.proba = 1

        next_state_true = deepcopy(state)
        next_state_true.name = "Pilule marche"
        next_state_true.proba = 0.5
        next_state_true.playerActu.vie_gagne += 1 if next_state_true.playerActu.vie_gagne+next_state_true.playerActu.vie_perdu < state.vie_max else 0

        next_state_false = deepcopy(state)
        next_state_false.name = "Pilule marche pas"
        next_state_false.proba = 0.5
        next_state_false.playerActu.vie_perdu = 1

        return Tree(state, [
            Tree(next_state_true, [next_state_true.roll()]),
            Tree(next_state_false, [next_state_false.roll()]),
        ])


class Voleur(Action):
    def construire_proba_graph(self, state) -> Tree:
        state.playerActu.objets.remove(self)
        state.name = "Voleur"
        state.proba = 1

        result = []

        for oo in state.opponent().objets:
            if oo is Voleur:
                cpy = deepcopy(state)
                # on enleve mécaniquement car sur un joueurs différent que celui en court
                cpy.opponent().objets.remove(oo)
                result.append(oo.construire_proba_graph(self, cpy))

        return Tree(state, result)


class Inverseur(Action):
    def construire_proba_graph(self, state) -> Tree:
        state.playerActu.objets.remove(self)
        state.name = "Inverseur"
        state.proba = 1

        index_last = state.nbr_cartouche() - 1
        proba = state.playerActu.revealed_ball.get(index_last, state.proba_plein_global())
        state.playerActu.revealed_ball[index_last] = 1 - proba

        return Tree(state, [state.roll()])


class Clope(Action):
    def construire_proba_graph(self, state) -> Tree:
        state.playerActu.objets.remove(self)
        state.name = "Clope"
        state.proba = 1

        state.playerActu.vie_gagne += 1 if state.playerActu.vie_gagne+state.playerActu.vie_perdu < state.vie_max else 0

        return Tree(state, [state.roll()])


class Biere(Action):
    def is_needed(self, state: State) -> bool:
        return state.proba_plein_global() == 0.5

    def construire_proba_graph(self, state) -> Tree:
        state.playerActu.objets.remove(self)
        state.name = "Biere"
        state.proba = 1

        next_state_plein = deepcopy(state)
        next_state_plein.name = "Cartouche pleine enlevée"
        next_state_plein.proba = state.playerActu.revealed_ball.get(state.nbr_cartouche() - 1,
                                                                    state.proba_plein_global())
        next_state_plein.nbr_plein -= 1

        next_state_vide = deepcopy(state)
        next_state_vide.name = "Cartouche pleine enlevée"
        next_state_vide.proba = 1 - state.playerActu.revealed_ball.get(state.nbr_cartouche() - 1,
                                                                       state.proba_plein_global())
        next_state_vide.nbr_vide -= 1

        return Tree(state, [
            Tree(next_state_plein, [next_state_plein.roll()]),
            Tree(next_state_vide, [next_state_vide.roll()]),
        ])


class Loupe(Action):
    def construire_proba_graph(self, state) -> Tree:
        state.playerActu.objets.remove(self)
        state.name = "Loupe"
        state.proba = 1

        next_state_plein = deepcopy(state)
        next_state_plein.name = "pleine vue"
        next_state_plein.proba = state.playerActu.revealed_ball.get(state.nbr_cartouche() - 1,
                                                                    state.proba_plein_global())
        next_state_plein.playerActu.revealed_ball[state.nbr_cartouche() - 1] = 1

        next_state_vide = deepcopy(state)
        next_state_vide.name = "Vide vue"
        next_state_vide.proba = 1 - state.playerActu.revealed_ball.get(state.nbr_cartouche() - 1,
                                                                       state.proba_plein_global())
        next_state_vide.playerActu.revealed_ball[state.nbr_cartouche() - 1] = 0

        return Tree(state, [
            Tree(next_state_plein, [next_state_plein.roll()]),
            Tree(next_state_vide, [next_state_vide.roll()]),
        ])


class Scie(Action):
    def construire_proba_graph(self, state) -> Tree:
        state.playerActu.objets.remove(self)
        state.name = "Scie"
        state.proba = 1

        state.playerActu.is_silled = True

        return Tree(state, [state.roll()])


class Menotte(Action):
    def construire_proba_graph(self, state) -> Tree:
        state.playerActu.objets.remove(self)
        state.name = "Menotte"
        state.proba = 1

        state.playerActu.is_opponent_chained = True

        return Tree(state, [state.roll()])
