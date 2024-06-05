class Tree:
    """
    classe représentant un arbre multiple simple
    """
    def __init__(self, element, childs: list):
        self.element = element
        self.childs = childs

    def depth_foreach(self, f):
        f(self)
        for n in self.childs:
            n.depth_foreach(n, f)

    def width_foreach(self, f):
        """
        la fonction va s'appliquer sur tout les éléments d'un niveau avant de passer au suivant
        """
        elements_at_level = [self]

        while elements_at_level:
            for element in elements_at_level:
                f(element)
            list_of_lists = [element.childs for element in elements_at_level]
            elements_at_level = flatten(list_of_lists)

    def __str__(self):
        return "..."


def flatten(lists_of_lists) -> list:
    """
    transforme une liste de liste en liste
    :param lists_of_lists:
    :return:
    """
    result = []
    for liste in lists_of_lists:
        result.extend(liste)

    return result
