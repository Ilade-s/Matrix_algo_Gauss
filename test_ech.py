"""test échellonage"""
from Matrix_class import Matrix, Transvection as T, Identity as I, Dilatation as D, Elementary as E, Permutation as P

class Systeme(Matrix):
    """Représente un système linéaire
    \nSubclass de Matrix"""
    def __init__(self, mat: list[list] | Matrix, name: str) -> None:
        super().__init__(0, name)
        self.set_as_mat(mat, strict=False)
    
    @property
    def equations(self):
        return self[:, :-1]
    
    @property
    def results(self):
        return self[:, -1]

if __name__ == '__main__':
    mat = Matrix((3, 4), "C")
    mat.set_as_mat([
        [1, 2, -3, 6],
        [2, -1, 4, 2],
        [4, 3, -2, 14]
    ])

    sys = Systeme(mat, 'S')

    print(sys)

    print(sys.equations)
    print(sys.results)
