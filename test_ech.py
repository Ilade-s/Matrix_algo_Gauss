"""test échellonage"""
from Matrix_class import *

class Systeme(Matrix):
    """Représente un système linéaire
    \nSubclass de Matrix"""
    def __init__(self, mat: list[list] | Matrix, name: str) -> None:
        super().__init__(0, name)
        self.set_as_mat(mat, strict=False)
        self.__rang = -1
    
    @property
    def equations(self):
        return self[:, :-1]
    
    @property
    def results(self):
        return self[:, -1]
    
    @property
    def rang(self):
        assert self.__rang >= 0, "La matrice n'a pas été échellonnée"
        return self.__rang
    
    def first_non_zero(self, l: int):
        """retourne la colonne du 1er coef de la ligne l qui est non nul (i.e. coef evalué à vrai)"""
        c = 1
        while not self.equations[l, c]:
            c += 1
            if c > self.equations.size_c: return 0
        return c 
    
    def ech(self, n_pivot=1):
        """échellonne la matrice (en place)
        \nn_pivots à 1 signifie qu'on effectue l'échellonnage total du système (recommandé/par défaut)"""
        if n_pivot > self.equations.size_c or not self.first_non_zero(n_pivot): # on est n dehors de la matrice, ou la ligne étudiée est totalement nulle
            self.__rang = n_pivot - 1
        else: # l'échellonnage n'est pas terminé
            # choisi, et si nécessaire replace, le 1er pivot
            if self.first_non_zero(n_pivot) > n_pivot:
                nl = n_pivot + 1
                while self.first_non_zero(nl) > n_pivot:
                    nl += 1
                self.permute(n_pivot, nl)
            # met à 0 les coefs de la même colonne, en dessous du pivot (self[n_pivot:, n_pivot])
            for l in range(n_pivot + 1, len(self) + 1):
                t = - self[l, n_pivot] / self[n_pivot, n_pivot]
                print('T{}{}({})'.format(l, n_pivot, t))
                self.transvect(l, n_pivot, t)
            
            print(self)

            self.ech(n_pivot+1)
    
    def reduce(self, offset=0):
        """reduit la matrice à une matrice triangulaire supérieure (voire diagonale)
        \tLa matrice doit avoir été préalablement échellonnée (self.ech())"""
        l = len(self) - offset
        if l == 0:
            pass
        else:
            c = self.first_non_zero(l)
            if c: # si la ligne n'est pas nulle (pivot présent), on peut la réduire
                self.dilate(l, 1 / self[l, c]) # on met le pivot à 1
                # on met à zéro les coefs de la colonne au dessus du pivot
                for i in range(1, l):
                    t = - self[i, c] / self[l, c]
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

    sys = Systeme(mat, 'S')

    print(sys)

    #print(sys.equations)
    #print(sys.results)

    sys.ech()
    sys.reduce()
