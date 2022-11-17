class Pile:
    """
    Une pile de maillons.

    Implémente les primitives d'une pile en POO.
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

    def est_vide(self):
        return self.taille == 0

    def empiler(self, e):
        self.tete = Maillon(e, self.tete)
        self.inc_taille()

    def depiler(self):
        if not self.est_vide():
            tete = self.tete
            self.tete = tete.suivant
            self.dec_taille()
            return tete

    def longueur(self):
        return self.taille

    def set_taille(self, v):
        self.taille = v

    def inc_taille(self):
        self.set_taille(self.longueur() + 1)

    def dec_taille(self):
        self.set_taille(self.longueur() - 1)

    def sommet(self):
        return self.tete

    def copier(self):
        p2 = Pile()
        p3 = Pile()
        while not self.est_vide():
            p2.empiler(self.depiler().valeur)
        while not p2.est_vide():
            e = p2.depiler().valeur
            p.empiler(e)
            p3.empiler(e)
        return p3

class Maillon:
    def __init__(self, valeur, suivant = None):
        self.valeur = valeur
        self.suivant = suivant

class Jeu:
    """
    Classe à un instance unique.
    Concrétise l'espace de jeu, avec trois piles.
    Permet de déplacer un élément d'une pile à l'autre.
    """
    # init
    hauteur = 4
    gauche = Pile()
    milieu = Pile()
    droite = Pile()
    for i in range(hauteur, 0, -1):
        gauche.empiler(i)

    def __str__(cls):
        line = ""
        piles = [cls.gauche, cls.milieu, cls.droite]
        for h in range(cls.hauteur, 0, -1):
            for p in piles:
                line = line + "  "
                taille = p.longueur()
                if p.est_vide() or taille < h:
                    line = line + "   "
                else:
                    e = p.sommet()
                    for i in range(h, taille):
                        e = e.suivant
                    line = line + f"[{e.valeur}]"
                line = line + "  "
            line = line + "\n"
        for _ in piles:
            line = line + "-=====-"
        return line

    # __setitem__ et __getitem__ peuvent simplifier l'écriture qui suit :
    def deplacer_gauche_vers_milieu(cls):
        if (not cls.milieu.sommet()
            or cls.gauche.sommet().valeur < cls.milieu.sommet().valeur
        ):
            cls.milieu.empiler(cls.gauche.depiler().valeur)

    def deplacer_gauche_vers_droite(cls):
        if (not cls.droite.sommet()
            or cls.gauche.sommet().valeur < cls.droite.sommet().valeur
        ):
            cls.droite.empiler(cls.gauche.depiler().valeur)

if __name__ == "__main__":
    p = Pile()
    p.empiler(1)
    assert p.longueur() == 1, "Erreur de taille"
    for i in range(2):
        p.empiler(i)
    assert p.longueur() == 3, "Erreur de taille"
    p2 = p.copier()
    assert p2.longueur() == 3, "Erreur de taille"
    assert p2.longueur() == p.longueur(), "Erreur de taille_copier"

    assert p2 != p, "Les deux piles ont la même adresse"
    assert p.sommet().valeur == p2.sommet().valeur, "Erreur de copie ?"
    assert p.sommet() != p2.sommet(), "Erreur de copie ?"

    Jeu().deplacer_gauche_vers_milieu()
    Jeu().deplacer_gauche_vers_droite()
    print(Jeu())