"""test échelonnage"""
from Matrix_class import *

class Systeme(Matrix):
    """Représente un système linéaire
    \nSubclass de Matrix"""
    def __init__(self, mat: list[list] | Matrix, name: str) -> None:
        super().__init__(0, name)
        self.set_as_mat(mat, strict=False)
        self.__rang = 0
    
    @property
    def equations(self):
        return self[:, :-1]
    
    @property
    def results(self):
        return self[:, -1]
    
    @property
    def rang(self):
        return self.__rang
    
    def first_non_zero(self, l: int):
        """retourne la colonne du 1er coef de la ligne l qui est non nul (i.e. coef evalué à vrai)"""
        c = 1
        while not self.equations[l, c]:
            c += 1
            if c > self.equations.size_c: return 0
        return c 
    
    def col_is_empty(self, c: int, l=1) -> bool:
        """retourne vrai si la colonne est vide à partir de la ligne l (à partir de la 1ere ligne par défaut), faux sinon"""
        tr = self.equations.transposition
        while not tr[c, l]:
            l += 1
            if l > tr.size_c: return True
        return False
    
    def ech(self, n_pivot=1):
        """échelonne la matrice (en place)
        \nn_pivots à 1 signifie qu'on effectue l'échelonnage total du système (recommandé/par défaut)"""
        if n_pivot > len(self): # on est en dehors de la matrice, ou la ligne étudiée est totalement nulle
            return self.rang
        elif not self.first_non_zero(n_pivot) and n_pivot < len(self): # ligne nulle, qui n'est pas la dernière ligne : on l'échange avec la prochaine
            self.permute(n_pivot, n_pivot + 1)
            self.ech(n_pivot) # on reprend à la ligne permutée
        elif self.col_is_empty(n_pivot, n_pivot): # par de coef non nul dans cette colonne à partir de la ligne n_pivots : pas de pivot possible
            self.ech(n_pivot + 1)
        else: # l'échelonnage n'est pas terminé
            # choisi, et si nécessaire replace, le 1er pivot
            if self.first_non_zero(n_pivot) > n_pivot:
                nl = n_pivot + 1
                while self.first_non_zero(nl) > n_pivot:
                    nl += 1
                self.permute(n_pivot, nl)
            # met à 0 les coefs de la même colonne, en dessous du pivot (self[n_pivot:, n_pivot])
            for l in range(n_pivot + 1, len(self) + 1):
                if self[l, n_pivot]:
                    t = (-1) * self[l, n_pivot] / self[n_pivot, n_pivot]
                    print('T{}{}({})'.format(l, n_pivot, t))
                    self.transvect(l, n_pivot, t)
                    print(self)
            self.__rang += 1
            self.ech(n_pivot + 1)
    
    def reduce(self, offset=0):
        """reduit la matrice à une matrice triangulaire supérieure (voire diagonale). 
        \nLa matrice doit avoir été préalablement échelonnée (self.ech())"""
        l = len(self) - offset
        if l:
            c = self.first_non_zero(l)
            if c: # si la ligne n'est pas nulle (pivot présent), on peut la réduire
                print("D{}({})".format(l, 1 / self[l, c]))
                self.dilate(l, 1 / self[l, c]) # on met le pivot à 1
                # on met à zéro les coefs de la colonne au dessus du pivot
                for i in range(1, l):
                    if self[i, c]:    
                        t = (-1) * self[i, c] / self[l, c]
                        print('T{}{}({})'.format(i, l, t))
                        self.transvect(i, l, t)
            print(self)        
            # on appelle reduce sur la colonne au dessus
            self.reduce(offset + 1)


if __name__ == '__main__':
    mat = Matrix((3, 4), "C")
    mat.set_as_mat([
        [1, 2, -3, 6],
        [2, -1, 4, 2],
        [4, 3, -2, 14]
    ])
    #a = Variable('a', 1)
    #b = Variable('b', 1)
    #c = Variable('c', 1)
    #d = Variable('d', 1)
    #mat = Matrix((3, 4), "C")
    #mat.set_as_mat([
    #    [1, 1, 1, 1],
    #    [a, b, c, d],
    #    [a**2, b**2, c**2, d**2]
    #])

    sys = Systeme(mat, 'S')

    print(sys)

    sys.ech()
    print("Rang du système : ", sys.rang)
    print("Réduction")
    sys.reduce()
