
class Matrix: pass

class Matrix:
    """
    Objet qui représente une matrice de taille (p, q) donnée à l'initialisation

    Opérateurs implémentés : 
    -------------
        - l'addition par une matrice de même taille (respectivement la soustraction)
        - la multiplication (à droite) : 
                - par un scalaire (respectivement la division)
                - par une matrice de taille (q, r)
    
    Opérations élémentaires :
    -------------
        - Transposée : self.transpose() (retourne une nouvelle matrice)
        - Permutation : self.permute(j, k) (en place)
        - Dilatation : self.dilate(i, d) (en place)
        - Transvection : self.transvect(i, j, t) (en place)
    """
    def __init__(self, size: tuple[int, int], name: str) -> None:
        self.name = name
        self.__content = []
        self.__set_size(size)
    
    @property
    def content(self) -> list[list]:
        return self.__content
    
    @property
    def size(self) -> tuple[int, int]:
        return (self.size_l, self.size_c)

    @property
    def transposition(self) -> Matrix:
        mat = [
            [
                self.get_coef(i, j) for i in range(1, self.size_l+1)
            ] 
            for j in range(1, self.size_c+1)
        ]
        t_mat = Matrix((self.size_c, self.size_l), '{}t'.format(self.name))
        t_mat.set_as_mat(mat)
        return t_mat

    def get_coef(self, i: int, j: int):
        assert 0 < i <= self.size_l and 0 < j <= self.size_c, "get_coef : given coordinates are out of bounds"
        return self.__content[i-1][j-1]
    
    def __set_size(self, size: tuple[int, int]) -> None:
        (self.size_l, self.size_c) = size
    
    def set_as_mat(self, mat: list[list]) -> None:
        assert len(mat) == self.size_l, "dimension lignes incompatible"
        assert len(mat[0]) == self.size_c, "dimension colonnes incompatible"
        self.__content = mat
    
    def set_identity(self) -> None:
        assert self.size_l == self.size_c
        mat = [
            [1 if i == j else 0 
                for j in range(self.size_c)
            ] 
            for i in range(self.size_l)
        ]
        self.set_as_mat(mat)
    
    def set_zero(self) -> None:
        mat = [
            [
                0 for j in range(self.size_c)
            ] 
            for i in range(self.size_l)
        ]
        self.set_as_mat(mat)
    
    def set_elementary(self, i: int, j: int) -> None:
        assert 0 < i <= self.size_l and 0 < j <= self.size_c, "set_elementary : given coordinates are out of bounds"
        self.set_zero()
        self.__content[i][j] = 1
    
    def __conv_res(self, mat: list[list], op: str, size: tuple[int, int]) -> Matrix:
        ret_mat = Matrix(size, name="{}{}".format(self.name, op))
        ret_mat.set_as_mat(mat)
        return ret_mat

    def permute(self, j: int, k: int) -> None:
        """échange les lignes d'indice j et k (en place)"""
        assert 0 < j <= self.size_l and 0 < k <= self.size_l, "transvect : line does not exist"
        self.__content[j-1], self.__content[k-1] = self.__content[k-1], self.__content[j-1]
    
    def dilate(self, i: int, d: int) -> None:
        """multiplie la ligne i par le facteur d (en place)"""
        assert 0 < i <= self.size_l, "dilate : line does not exist"
        for j in range(self.size_c):
            self.__content[i-1][j] *= d
    
    def transvect(self, i: int, j: int, t: int) -> None:
        """ajoute à la ligne i la ligne j multipliée par le facteur t (en place)"""
        assert 0 < i <= self.size_l and 0 < j <= self.size_l, "transvect : line does not exist"
        for c in range(self.size_c):
            self.__content[i-1][c] += self.__content[j-1][c] * t

    def __str__(self) -> str:
        s = "Matrice {} : \n".format(self.name)
        for i in range(self.size_l):
            for j in range(self.size_c):
                s += '{}  '.format(self.__content[i][j])
            if i < self.size_l - 1: s += '\n'
        return s
    
    def __add__(self, addvalue) -> Matrix:
        assert addvalue.size_l == self.size_l, "addition : dimension lignes incompatible"
        assert addvalue.size_c == self.size_c, "addition : dimension colonnes incompatible"
        mat_res = [
            [self.get_coef(i, j) + addvalue.get_coef(i, j)
                for j in range(1, self.size_c+1)
            ] 
            for i in range(1, self.size_l+1)
        ]
        return self.__conv_res(mat_res, '+{}'.format(addvalue.name), self.size)
    
    def __mul__(self, mulvalue) -> Matrix:
        if type(mulvalue) == Matrix: 
            assert self.size_c == mulvalue.size_l, "number of columns on the left does not match with number of lines on the right"
            mat_res = [
                [sum([self.get_coef(i, k) * mulvalue.get_coef(k, j) for k in range(1, self.size_c+1)]) # TODO : pose probleme si self[i, k] est une constante mais pas mulvalue[k, j]
                    for j in range(1, mulvalue.size_c+1)
                ]
                for i in range(1, self.size_l+1)
            ]
            size = (self.size_l, mulvalue.size_c)
            name = mulvalue.name
        else: # multiplication par un scalaire
            mat_res = [
                [self.get_coef(i, j) * mulvalue
                    for j in range(1, self.size_c+1)
                ] 
                for i in range(1, self.size_l+1)
            ]
            size = self.size
            name = "*{}".format(mulvalue) if mulvalue >= 1 else "/{}".format(1/mulvalue)
            
        return self.__conv_res(mat_res, name, size)

    def __sub__(self, subvalue) -> Matrix:
        return self + (subvalue * -1)
    
    def __truediv__(self, divvalue) -> Matrix:
        if type(divvalue) == Matrix: 
            pass # inversion de matrice ? TODO
        else: # division par un scalaire
            return (self * (1/divvalue))

if __name__ == '__main__':
    print("Matrices d'exemple : ")
    # exemple matrice A de taille (2, 3)
    mat_A = Matrix((2, 3), "A")
    mat_A.set_as_mat([
        [2, 3, 7],
        [1, 4, 6]
    ])
    print(mat_A)
    # exemple matrice B de taille (3,2)
    mat_B = Matrix((3, 2), "B")
    mat_B.set_as_mat([
        [4, 5],
        [0, 1],
        [3, 2]
    ])
    print(mat_B)
    mat_C = Matrix((3, 3), "C")
    mat_C.set_as_mat([
        [1, 2, -3],
        [2, -1, 4],
        [4, 3, -2]
    ])
    print(mat_C)
    # ---------------------
    # opérateurs 
    print("Utilisation des opérateurs : ")
    # addition :
    addition = mat_A + mat_A
    print(addition)
    # multiplication :
    #   - par une autre matrice
    multi = mat_A * mat_B
    print(multi)
    #   - par un scalaire 3
    multi_sca = mat_A * 3
    print(multi_sca)
    # division :
    #   - par un scalaire 2
    div_sca = mat_A / 2
    print(div_sca)
    # ----------------------
    # Opérations élémentaires sur les matrices
    print("Opération sur les matrices : ")
    # transposition
    mat_At = mat_A.transposition
    print(mat_At)
    # permutation
    j = 1; k = 3
    mat_C.permute(j, k)
    print("P({},{}) :\n".format(j, k), mat_C, sep='')
    mat_C.permute(j, k) # inverse
    # dilatation
    d = 4; i = 2
    mat_C.dilate(i, d)
    print("D{}({}) :\n".format(i, d), mat_C, sep='')
    mat_C.dilate(i, 1/d) # inverse 
    # transvection
    t = 2; i = 2; j = 1
    mat_C.transvect(i, j, t)
    print("T{}{}({})\n".format(i, j, t), mat_C, sep='')
    mat_C.transvect(i, j, -t) # inverse
    
