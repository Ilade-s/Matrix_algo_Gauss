from Expression_class import Expression, Variable

class Matrix: pass

class Matrix:
    """
    Objet qui représente une matrice de taille (p, q) donnée à l'initialisation.
    
    Initialisée à une matrice nulle de la bonne taille.

    Accès/modification : 
    -----------------
        - ligne (élément) : Matrix[<ligne> (, <colonne>)]

    Opérateurs/Actions implémentés : 
    -------------
        - l'addition par une matrice de même taille (respectivement la soustraction)
        - la multiplication : 
                - par un scalaire (respectivement la division)
                - par une matrice de taille compatible
        - affichage (méthode __print__ définie)
    
    Opérations élémentaires :
    -------------
        - Transposée : self.transposition (retourne une nouvelle matrice)
        - Permutation : self.permute(j, k) (en place)
        - Dilatation : self.dilate(i, d) (en place)
        - Transvection : self.transvect(i, j, t) (en place)
    """
    def __init__(self, size: tuple[int, int], name: str) -> None:
        self.name = name
        self.__set_size(size)
        self.set_zero()
    
    @property
    def content(self) -> list[list]:
        return self.__content

    @property
    def transposition(self) -> Matrix:
        mat = [
            [
                self[i, j] for i in range(1, len(self)+1)
            ] 
            for j in range(1, len(self[0])+1)
        ]
        t_mat = Matrix((len(self[0]), len(self)), '{}t'.format(self.name))
        t_mat.set_as_mat(mat)
        return t_mat
    
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
        assert 0 < i <= len(self) and 0 < j <= len(self[0]), "set_elementary : given coordinates are out of bounds"
        self.set_zero()
        self[i, j] = 1
    
    def __conv_res(self, mat: list[list], op: str, size: tuple[int, int]) -> Matrix:
        ret_mat = Matrix(size, name="{}{}".format(self.name, op))
        ret_mat.set_as_mat(mat)
        return ret_mat

    def permute(self, j: int, k: int) -> None:
        """échange les lignes d'indice j et k (en place)"""
        assert 0 < j <= len(self) and 0 < k <= len(self), "transvect : line does not exist"
        self[j], self[k] = self[k], self[j]
    
    def dilate(self, i: int, d: int) -> None:
        """multiplie la ligne i par le facteur d (en place)"""
        assert 0 < i <= len(self), "dilate : line does not exist"
        for j in range(1, len(self[0])+1):
            self[i, j] *= d
    
    def transvect(self, i: int, j: int, t: int) -> None:
        """ajoute à la ligne i la ligne j multipliée par le facteur t (en place)"""
        assert 0 < i <= len(self) and 0 < j <= len(self), "transvect : line does not exist"
        for c in range(1, len(self[0])+1):
            self[i, c] += self[j, c] * t

    def __len__(self) -> int:
        return self.size_l

    def __getitem__(self, key):
        assert isinstance(key, (tuple, int)), "key must be one or two indexes ([<line>] or [<line>, <column>])"
        if isinstance(key, tuple): # key est un couple ligne/colonne
            key_l, key_c = key
            assert (-self.size_l < key_l <= self.size_l) and (-self.size_c < key_c <= self.size_c), "item does not exist at coordinates {}, {}".format(key_l, key_c)
            item = self.__content[key_l-1][key_c-1]
        else: # key est un index
            assert -self.size_l < key <= self.size_l, "line {} does not exist".format(key)
            item = self.__content[key-1]
        return item

    def __setitem__(self, key, value) -> None:
        if isinstance(key, tuple): # key est un couple ligne/colonne
            key_l, key_c = key
            assert (-self.size_l < key_l <= self.size_l) and (-self.size_c < key_c <= self.size_c), "invalid coordinates {}, {}".format(key_l, key_c)
            self.__content[key_l-1][key_c-1] = value
        else: # key est un index
            assert -self.size_l < key <= self.size_l, "line {} does not exist".format(key)
            self.__content[key-1] = value

    def __str__(self) -> str:
        sl = ['' for _ in range(len(self) + 1)]
        sl[0] = "Matrice {} : ".format(self.name) + sl[0]
        for j in range(1, len(self[0])+1): # per column index
            len_sep = max(map(len, [str(self[i, j]) for i in range(len(self))])) + 2
            for i in range(1, len(self)+1): # per line index
                s_elt = str(self[i, j]) 
                sl[i] += s_elt + ' ' * (len_sep - len(s_elt))
        return '\n'.join(sl)

    def __repr__(self) -> str:
        return f"{self.name}({len(self)}, {len(self[0])})"
    
    def __add__(self, addvalue) -> Matrix:
        assert isinstance(addvalue, self.__class__), "addition : seule l'addition de deux matrices est possible"
        assert len(addvalue) == len(self), "addition : dimension lignes incompatible"
        assert len(addvalue[0]) == len(self[0]), "addition : dimension colonnes incompatible"
        mat_res = [
            [self[i, j] + addvalue[i, j]
                for j in range(1, len(self[0])+1)
            ] 
            for i in range(1, len(self)+1)
        ]
        return self.__conv_res(mat_res, '+{}'.format(addvalue.name), (len(self), len(self[0])))
    
    def __mul__(self, mulvalue) -> Matrix:
        if isinstance(mulvalue, self.__class__): # multiplication matrice/matrice
            assert len(self[0]) == len(mulvalue), "number of columns on the left does not match with number of lines on the right"
            mat_res = [
                [sum([self[i, k] * mulvalue[k, j] for k in range(1, len(self[0])+1)])
                    for j in range(1, len(mulvalue[0])+1)
                ]
                for i in range(1, len(self)+1)
            ]
            size = (len(self), len(mulvalue[0]))
            name = mulvalue.name
        else: # multiplication par un scalaire
            mat_res = [
                [self[i, j] * mulvalue
                    for j in range(1, len(self[0])+1)
                ] 
                for i in range(1, len(self)+1)
            ]
            size = (len(self), len(self[0]))
            name = "*{}".format(mulvalue) if mulvalue >= 1 else "/{}".format(1/mulvalue)
            
        return self.__conv_res(mat_res, name, size)

    def __rmul__(self, mulvalue) -> Matrix:
        return self * mulvalue

    def __sub__(self, subvalue) -> Matrix:
        return self + (subvalue * -1)
    
    def __truediv__(self, divvalue) -> Matrix:
        if isinstance(divvalue, self.__class__): 
            pass # inversion de matrice ? TODO
        else: # division par un scalaire
            return (self * (1/divvalue))

if __name__ == '__main__':
    # inconnues d'exemple
    x = Variable('x', 1)
    y = Variable('y', 1)
    z = Variable('z', 1)
    print("Matrices d'exemple : ")
    # exemple matrice A de taille (2, 3)
    mat_A = Matrix((2, 3), "A")
    mat_A.set_as_mat([
        [2, 3*x, 7],
        [1, 4, 6*z]
    ])
    print(mat_A)
    print(repr(mat_A))
    # exemple matrice B de taille (3,2)
    mat_B = Matrix((3, 2), "B")
    mat_B.set_as_mat([
        [4, 5],
        [0, 1*y],
        [3*x, 2]
    ])
    print(mat_B)
    print(repr(mat_B))
    mat_C = Matrix((3, 3), "C")
    mat_C.set_as_mat([
        [1, 2, -3],
        [2, -1, 4],
        [4, 3, -2]
    ])
    print(mat_C)
    print(repr(mat_C))
    # ---------------------
    # opérateurs 
    print("Utilisation des opérateurs : ")
    # addition :
    addition = mat_A + mat_A
    print(addition)
    # multiplication :
    #   - par une autre matrice (dans les deux sens)
    multi = mat_A * mat_B
    print(multi)
    multi = mat_B * mat_A
    print(multi)
    #   - par un scalaire 3
    multi_sca = 3 * mat_A
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
    
