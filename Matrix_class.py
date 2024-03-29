from Expression_class import Expression, Variable

class Matrix: pass

class Identity: pass

class Elementary: pass

class Matrix:
    """
    Objet qui représente une matrice de taille (p, q) donnée à l'initialisation.
    
    Initialisée à une matrice nulle de la bonne taille.

    Accès/modification : 
    -----------------
        - ligne (élément) : Matrix[<ligne> (, <colonne>)]
        - en accès uniquement : 
            - <ligne> et <colonne> peuvent être soit des entiers, soit des sous-parties (i.e. objet Slice au format <start>:<stop>:<step>)
            - si l'un des deux (ou les deux) sont des sous-parties, alors le résultat de l'accès sera une matrice issue de la matrice originelle (avec un nom automatique).
            - Interprétation des indices (IMPORTANT) :
                - Entiers : un 0 est interprété comme un -1 (i.e. dernière ligne/colonne)
                - Slices :
                    - si <start> est fourni et est positif, la ligne/colonne correspondante ne sera pas incluse (incluse si négatif)
                    - au contraire, si <stop> est fourni, la ligne/colonne correspondante sera bien incluse
                    - si <start> = 0, il sera interprété comme si <start> n'a pas été fourni

    Opérateurs/Actions implémentés : 
    -------------
        - l'addition par une matrice de même taille (respectivement la soustraction)
        - la multiplication : 
                - par un scalaire (support de Variable et Expression) (respectivement la division)
                - par une matrice de taille compatible
        - affichage (méthode __print__ et __repr__ définies)
    
    Opérations élémentaires :
    ------------- 
        Ces opérations utilisent les matrices de transformation définies dans ce fichier, sur les lignes (multiplication à gauche). \n
        (Pour avoir les transformations sur les colonnes, veuillez utiliser les subs-classes indiquées directement.
        Leur initialisation est similaire aux énoncés mathématiques, et elles héritent de toutes les méthodes de Matrix)

        - Transposée : self.transposition (retourne une nouvelle matrice)
        - Permutation : self.permute(j, k) (en place) : Permutation(j, k, size(, name))
        - Dilatation : self.dilate(i, d) (en place) : Dilatation(i, d, size(, name))
        - Transvection : self.transvect(i, j, t) (en place) : Transvection(i, j, t, size(, name))

        Les autres matrices disponibles sont la matrice identité Identity(size(, name)) et la matrice élémentaire Elementary(i, j, size(, name))
    """
    def __init__(self, size: tuple[int, int] | int, name: str) -> None:
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
            for j in range(1, self.size_c+1)
        ]
        t_mat = Matrix((self.size_c, len(self)), '{}t'.format(self.name))
        t_mat.set_as_mat(mat)
        return t_mat

    @property
    def size(self) -> tuple[int, int]:
        return (self.size_l, self.size_c)
    
    def __set_size(self, size: tuple[int, int] | int) -> None:
        if isinstance(size, int):
            self.size_l = size
            self.size_c = size
        else:
            (self.size_l, self.size_c) = size
    
    def set_as_mat(self, mat: list[list] | Matrix, strict=True) -> None:
        """sets the matrix to the contents of mat (supports 2D lists or Matrix objets).
        \nstrict flag, if set, ensures that the size of mat is identical to this matrix, if not, changes the size to match mat (true by default)"""
        if not mat:
            if not strict:
                self.size_l = len(mat)
            return
        mat_is_list = isinstance(mat, list)
        if strict:    
            assert len(mat) == len(self), "dimension lignes incompatible : self = {} ; mat = {}".format(len(self), len(mat))
            if mat_is_list:
                assert len(mat[0]) == self.size_c, "dimension colonnes incompatible : self = {} ; mat = {}".format(self.size_c, len(mat[0]))
            else:
                assert mat.size_c == self.size_c, "dimension colonnes incompatible : self = {} ; mat = {}".format(self.size_c, mat.size_c)
        else:
            if mat_is_list:
                self.__set_size((len(mat), len(mat[0])))
            else:
                self.__set_size(mat.size)
        if mat_is_list:    
            self.__content = mat
        else:
            self.__content = mat.content
    
    def set_zero(self) -> None:
        mat = [
            [
                0 for j in range(self.size_c)
            ] 
            for i in range(self.size_l)
        ]
        self.set_as_mat(mat)
    
    def __conv_res(self, mat: list[list], op: str, size: tuple[int, int]) -> Matrix:
        ret_mat = Matrix(size, "{}{}".format(self.name, op))
        ret_mat.set_as_mat(mat)
        return ret_mat

    def permute(self, j: int, k: int) -> None: # voir pour faire transpostion de la même manière (avec res = self * P)
        """échange les lignes d'indice j et k (en place)"""
        assert 0 < j <= len(self) and 0 < k <= len(self), "transvect : line does not exist"
        res = Permutation(j, k, len(self)) * self
        self.set_as_mat(res)

    def dilate(self, i: int, d: int) -> None:
        """multiplie la ligne i par le facteur d (en place)"""
        assert 0 < i <= len(self), "dilate : line does not exist"
        res = Dilatation(i, d, len(self)) * self
        self.set_as_mat(res)
    
    def transvect(self, i: int, j: int, t: int) -> None:
        """ajoute à la ligne i la ligne j multipliée par le facteur t (en place)"""
        res = Transvection(i, j, t, len(self)) * self
        self.set_as_mat(res)

    def __len__(self) -> int:
        return self.size_l
    
    def __bool__(self) -> bool:
        return bool(len(self))

    def __getitem__(self, key: tuple | int | slice):
        assert isinstance(key, (tuple, int, slice)), "key must be one or two indexes ([<line>] or [<line>, <column>])"
        if isinstance(key, tuple): # key est un couple ligne/colonne
            key_l, key_c = key
            if isinstance(key_l, slice): # suite de lignes
                if isinstance(key_c, slice): # sous matrice
                    item = [[self[i+1, j+1] for j in range(*key_c.indices(self.size_c))] 
                        for i in range(*key_l.indices(len(self)))
                    ]
                    lc = 0
                    if len(item):
                        lc = len(item[0])
                    mat = Matrix((len(item), lc), 
                        "{}({}:{}:{}, {}:{}:{})".format(
                            self.name, *key_l.indices(len(self)), *key_c.indices(self.size_c)))
                    mat.set_as_mat(item)

                else: # plusieurs éléments d'une même colonne key_c
                    item = [self[i+1, key_c] for i in range(*key_l.indices(len(self)))]
                    mat = Matrix((1, len(item)), 'tmp')
                    mat.set_as_mat([item])
                    mat = mat.transposition
                    mat.name = "{}({}:{}:{}, {})".format(
                                    self.name, *key_l.indices(len(self)), key_c)
    
            else: # une seule ligne
                if isinstance(key_c, slice): # plusieurs éléments d'une même ligne key_l
                    item = [self[key_l, j+1] for j in range(*key_c.indices(self.size_c))]
                    mat = Matrix((1, len(item)), 
                        "{}({}, {}:{}:{})".format(
                            self.name, key_l , *key_c.indices(len(self)+1)))
                    mat.set_as_mat([item])
                else: # un seul item à l'index (key_l, key_c)
                    assert (-self.size_l <= key_l <= self.size_l) and (-self.size_c <= key_c <= self.size_c), "item does not exist at coordinates {}, {}".format(key_l, key_c)
                    if key_l >= 0: key_l -= 1
                    if key_c >= 0: key_c -= 1
                    item = self.__content[key_l][key_c]
                    return item
                
        elif isinstance(key, slice): # key est une suite de lignes
            item = [self[i+1].content[0] for i in range(*key.indices(len(self)))]
            print(item)
            mat = Matrix((len(item), self.size_c), 
                "{}({}:{}:{})".format(self.name, *key.indices(len(self))))
            mat.set_as_mat(item)

        else: # key est un index
            assert -self.size_l <= key <= self.size_l, "line {} does not exist".format(key)
            item = self.__content[key-1 if key >= 0 else key]
            mat = Matrix((1, self.size_c), "{}({}, :)".format(self.name, key))
            mat.set_as_mat([item])
        return mat

    def __setitem__(self, key: tuple | int, value) -> None:
        if isinstance(key, tuple): # key est un couple ligne/colonne
            key_l, key_c = key
            assert (-self.size_l <= key_l <= self.size_l) and (-self.size_c <= key_c <= self.size_c), "invalid coordinates {}, {}".format(key_l, key_c)
            if key_l >= 0: key_l -= 1
            if key_c >= 0: key_c -= 1
            self.__content[key_l][key_c] = value
        else: # key est un index
            assert isinstance(value, (list, Matrix)), "value must be either a list or a {} object".format(Matrix.__name__)
            assert -self.size_l <= key <= self.size_l, "line {} does not exist".format(key)
            if key >= 0: key -= 1
            if isinstance(value, list): # value est une liste de coefs
                self.__content[key] = value
            else: # value est une matrice ligne
                assert self.size_c == value.size_c, "la matrice ligne doit avoir le même nombre de colonnes"
                for c in range(1, self.size_c+1):
                    self.__content[key][c-1] = value[1, c]

    def __str__(self) -> str:
        sl = ['' for _ in range(len(self) + 1)]
        sl[0] = "Matrice {} : ".format(self.name) + sl[0]
        for j in range(1, self.size_c+1): # per column index
            len_sep = max(map(len, [str(self[i, j]) for i in range(len(self))])) + 2
            for i in range(1, len(self)+1): # per line index
                s_elt = str(self[i, j]) 
                sl[i] += s_elt + ' ' * (len_sep - len(s_elt))
        return '\n'.join(sl)

    def __repr__(self) -> str:
        return f"{self.name}({len(self)}, {self.size_c})"
    
    def __add__(self, addvalue) -> Matrix:
        assert isinstance(addvalue, Matrix), "addition : seule l'addition de deux matrices est possible"
        assert len(addvalue) == len(self), "addition : dimension lignes incompatible"
        assert addvalue.size_c == self.size_c, "addition : dimension colonnes incompatible"
        mat_res = [
            [self[i, j] + addvalue[i, j]
                for j in range(1, self.size_c+1)
            ] 
            for i in range(1, len(self)+1)
        ]
        return self.__conv_res(mat_res, '+{}'.format(addvalue.name), (len(self), self.size_c))
    
    def __mul__(self, mulvalue) -> Matrix:
        if isinstance(mulvalue, Matrix): # multiplication matrice/matrice
            assert self.size_c == len(mulvalue), "number of columns on the left does not match with number of lines on the right"
            mat_res = [
                [sum([self[i, k] * mulvalue[k, j] for k in range(1, self.size_c+1)])
                    for j in range(1, mulvalue.size_c+1)
                ]
                for i in range(1, len(self)+1)
            ]
            size = (len(self), mulvalue.size_c)
            name = mulvalue.name
        else: # multiplication par un scalaire/Variable/Expression
            mat_res = [
                [self[i, j] * mulvalue
                    for j in range(1, self.size_c+1)
                ] 
                for i in range(1, len(self)+1)
            ]
            size = (len(self), self.size_c)
            name = "*{}".format(mulvalue) if mulvalue >= 1 else "/{}".format(1/mulvalue)
            
        return self.__conv_res(mat_res, name, size)

    def __rmul__(self, mulvalue) -> Matrix:
        return self * mulvalue

    def __sub__(self, subvalue) -> Matrix:
        return self + (subvalue * -1)
    
    def __truediv__(self, divvalue) -> Matrix:
        if isinstance(divvalue, Matrix): 
            pass # inversion de matrice ? TODO
        else: # division par un scalaire
            return (self * (1/divvalue))
    
    def __pow__(self, power) -> Matrix:
        assert len(self) == self.size_c, "la matrice doit être une matrice carrée"
        assert power >= 0, "l'exposant doit être positif ou nul"
        res = Identity(len(self), 'tmp')
        for _ in range(power):
            res *= self
        res.name = self.name + "^{}".format(power) 
        return res

class Elementary(Matrix):
    """Matrice élémentaire E (avec E[i, j] = 1)
    \nSubclass de Matrix"""
    def __init__(self, i: int, j: int, size: tuple[int, int] | int, name = '') -> None:
        if not name:
            name = 'E({}, {})'.format(size, i, j)
        super().__init__(size, name)
        assert 0 < i <= len(self) and 0 < j <= self.size_c, "{} : given coordinates ({}, {}) are out of bounds".format(self.__repr__(), i, j)
        self[i, j] = 1

class Identity(Matrix):
    """Matrice identité I (avec I[i, j] = 1 si i == j, sinon = 0)
    \nSubclass de Matrix"""
    def __init__(self, size: int, name = '') -> None:
        if not name:
            name = 'I{}'.format(size)
        super().__init__(size, name)
        for c in range(size):
            self[c, c] = 1

class Dilatation(Identity):
    """Matrice de dilatation de la ligne i, de facteur d (avec I[n\\\{i}, j] = 1 si n\\\{i} == j et I[i, j] = d) : D{i}({d})
    \nSubclass de Identity"""
    def __init__(self, i: int, d, size: int, name = '') -> None:
        if not name:
            name = 'D{}({})'.format(i, d)
        super().__init__(size, name)
        assert 0 < i <= len(self), "{} : given line {} is out of bounds".format(self.__repr__(), i)
        self[i, i] = d

class Permutation(Identity):
    """Matrice de permutation P des lignes/colonnes j et k : P{j}{k}
    \nSubclass de Identity"""
    def __init__(self, j: int, k: int, size: int, name='') -> None:
        if not name:
            name = 'P({},{})'.format(j, k)
        super().__init__(size, name)
        self[j, j] = 0
        self[k, k] = 0
        self[j, k] = 1
        self[k, j] = 1

class Transvection(Identity):
    """Matrice de transvection de la ligne i par la ligne j facteur t : T{i}{j}({t})
    \nSubclass de Identity"""
    def __init__(self, i: int, j: int, t, size: int, name='') -> None:
        if not name:
            name = "T{}{}({})".format(i, j, t)
        super().__init__(size, name)
        assert i != j, "{} : line i and j are equal (= {})".format(self.__repr__(), i)
        self[i, j] = t

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
    sous_mat_A = mat_A[-2, ::-1] # 1ere ligne avec colonnes inversées
    print(sous_mat_A) # exemple sous matrice
    print(repr(sous_mat_A))
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
    print(mat_C**2)
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
    d = Variable("d", 3); i = 2
    mat_C.dilate(i, d)
    print("D{}({}) :\n".format(i, d), mat_C, sep='')
    mat_C.dilate(i, 1/d) # inverse 
    # transvection
    t = 2; i = 2; j = 1
    mat_C.transvect(i, j, t)
    print("T{}{}({})\n".format(i, j, t), mat_C, sep='')
    mat_C.transvect(i, j, -t) # inverse
    print(mat_C)
    
