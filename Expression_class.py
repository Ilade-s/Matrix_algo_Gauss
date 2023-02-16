class Variable: pass

class Expression: pass

class Expression:
    """représente une expression formée de valeurs (int...) et d'inconnues sous forme de Variable"""
    def __init__(self, constant, variables: list[Variable]) -> None:
        self.constant = constant
        self.vars = variables
    
    @property
    def termes(self):
        return self.values + self.vars
    
    def __str__(self):
        return ' + '.format(*self.termes)

class Variable:
    """représente une variable avec son facteur associé dans une matrice"""
    def __init__(self, name: str, factor) -> None:
        self.name = name
        self.factor = factor
    
    def __str__(self) -> str:
        return '{}{}'.format(self.factor, self.name)

    def __add__(self, addvalue) -> Expression:
        if type(addvalue) == Variable:
            return Expression([], [self, addvalue])
        elif type(addvalue) == Expression:
            return Expression(addvalue.values, addvalue.vars + [self])
        else:
            return Expression([addvalue], [self])

    def __mul__(self, mulvalue) -> Variable:
        if type(mulvalue) == Variable:
            return Variable(self.name, mulvalue * self.factor)
        elif type(mulvalue) == Expression:
            return Expression(0, [self * v for v in mulvalue.vars] + [self * mulvalue.constant])
        else:
            return Variable(self.name, self.factor * mulvalue)
    
    def __sub__(self, subvalue):
        return self + (subvalue * -1)

    def __truediv__(self, divvalue):
        pass

if __name__ == '__main__':
    pass
