class Variable: pass

class Expression: pass

class Expression:
    """représente une expression formée de valeurs (int...) et d'inconnues sous forme de Variable"""
    def __init__(self, constant, variables: list[Variable]) -> None:
        self.constant = constant
        self.vars = variables
    
    @property
    def termes(self):
        """termes """
        return (self.vars + [self.constant])
    
    def __str__(self):
        return ' + '.join(map(str, [t for t in self.termes if t]))

    def __add__(self, addvalue):
        if isinstance(addvalue, Variable):
            return self.__class__(self.constant, self.vars + [addvalue])
        elif isinstance(addvalue, self.__class__):
            return self.__class__(self.constant + addvalue.constant, self.vars + addvalue.vars)
        else:
            return self.__class__(self.constant + addvalue, self.vars)
    
    def __sub__(self, subvalue):
        return self + subvalue * (-1)

    def __mul__(self, mulvalue): # TODO
        pass

class Variable:
    """représente une variable avec son facteur associé dans une matrice"""
    def __init__(self, name: str, factor) -> None:
        self.name = name
        self.factor = factor
    
    @property
    def inverse(self):
        """variable avec son facteur^-1"""
        return self.__class__(self.name, 1 / self.factor)

    def __bool__(self) -> bool:
        return self.factor != 0
    
    def __str__(self) -> str:
        return '{}{}'.format(self.factor, self.name)

    def __add__(self, addvalue):
        if isinstance(addvalue, self.__class__):
            if addvalue.name == self.name:
                return self.__class__(self.name, self.factor + addvalue.factor)
            else:
                return Expression(0, [self, addvalue])
        elif isinstance(addvalue, Expression):
            return Expression(addvalue.constant, addvalue.vars + [self])
        else:
            return Expression(addvalue, [self])
    
    def __radd__(self, addvalue):
        return self + addvalue

    def __mul__(self, mulvalue):
        if isinstance(mulvalue, self.__class__):
            return self.__class__(self.name, mulvalue * self.factor)
        elif isinstance(mulvalue, Expression):
            return Expression(0, [self * v for v in mulvalue.vars] + [self * mulvalue.constant])
        else:
            return self.__class__(self.name, self.factor * mulvalue)
    
    def __rmul__(self, mulvalue):
        return self * mulvalue

    def __sub__(self, subvalue):
        return self + (subvalue * -1)
    
    def __rsub__(self, subvalue):
        return -1 * self + subvalue

    def __truediv__(self, divvalue):
        if isinstance(divvalue, Variable):
            return self * divvalue.inverse
        else:
            return self.__class__(self.name, self.factor / divvalue)

if __name__ == '__main__':
    var_1 = Variable('x', 2) # 2x
    var_2 = Variable('y', 3) # 3y
    var_3 = Variable('x', 1) # 1x
    print('Variables : ')
    print(var_1, var_2, var_3)
    exp_1 = 4 - var_1 + var_2 - 5 
    print(exp_1)

