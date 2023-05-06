class Pile:
    """
    Une pile de maillons.

    Implémenter les primitives d'une pile en POO.
    /!\\ N'utiliser que les fonctions données !
         Attention aux inversions.

    Pile :
    - créer une pile
    - empiler
    - dépiler
    - taille
    ~ copier
    - sommet
    """

    def __init__(self):
        self.tete = None
        self.taille = 0
