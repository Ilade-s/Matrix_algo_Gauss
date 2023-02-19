class Variable: pass

class Expression: pass

class Expression:
    """représente une expression formée d'une constante et d'inconnues sous forme de Variable"""
    def __init__(self, constant, variables: list[Variable]) -> None:
        self.constant = constant
        self.vars = variables
    
    @property
    def termes(self) -> list:
        return (self.vars + [self.constant])

    def __len__(self) -> int:
        return len([t for t in self.termes if t])
    
    def __str__(self) -> str:
        return ' + '.join(map(str, [t for t in self.termes if t]))
    
    def __repr__(self) -> str:
        vars_repr = ' ; '.join(map(repr, [v for v in self.vars if v]))
        return '{}(\n\tconst = {},\n\t{})'.format(self.__class__.__name__, self.constant, vars_repr)

    def __add__(self, addvalue) -> Expression:
        if isinstance(addvalue, Variable): 
            n_vars = [*self.vars]
            for i in range(len(n_vars)): # il faut vérifier la présence ou non de cette inconnue dans l'équation
                if n_vars[i].name == addvalue.name and not isinstance(n_vars[i].factor, Variable): 
                    n_vars[i] += addvalue
                    return self.__class__(self.constant, n_vars)
            n_vars.append(addvalue)
            return self.__class__(self.constant, n_vars)
        elif isinstance(addvalue, self.__class__):
            exp_res = self.__class__(self.constant, self.vars) 
            for v in addvalue.termes:
                exp_res += v
            return exp_res
        else:
            return self.__class__(self.constant + addvalue, self.vars)
    
    def __sub__(self, subvalue) -> Expression:
        return self + subvalue * (-1)
    
    def __copy__(self) -> Expression:
        return self.__class__(self.constant, self.vars)

    def __mul__(self, mulvalue) -> Expression: 
        if isinstance(mulvalue, self.__class__): # dévellopement
            n_vars = []
            for t in self.termes:
                for t_mul in mulvalue.termes:
                    n_vars.append(t * t_mul)
        elif isinstance(mulvalue, Variable):
            return Expression(0, [v * mulvalue for v in self.vars if v] + [self.constant * mulvalue])
        else:
            return Expression(self.constant * mulvalue, [v * mulvalue for v in self.vars if v])

class Variable:
    """représente une variable avec son facteur associé dans une matrice"""
    def __init__(self, name: str, factor) -> None:
        self.name = name
        self.factor = factor
    
    @property
    def inverse(self) -> Variable:
        """variable avec son facteur inversé (^-1)"""
        return self.__class__(self.name, 1 / self.factor)

    def __bool__(self) -> bool:
        return self.factor != 0
    
    def __str__(self) -> str:
        return '{}{}'.format(self.factor, self.name)
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.factor!r}, {self.name})"

    def __add__(self, addvalue) -> (Expression | Variable):
        if isinstance(addvalue, self.__class__):
            if addvalue.name == self.name:
                return self.__class__(self.name, self.factor + addvalue.factor)
            else:
                return Expression(0, [self, addvalue])
        elif isinstance(addvalue, Expression):
            return addvalue + self
        else:
            return Expression(addvalue, [self])
    
    def __radd__(self, addvalue) -> (Expression | Variable):
        return self + addvalue

    def __mul__(self, mulvalue) -> (Expression | Variable):
        if isinstance(mulvalue, self.__class__):
            return self.__class__(self.name, mulvalue * self.factor)
        elif isinstance(mulvalue, Expression):
            return Expression(0, [self * v for v in mulvalue.vars if v] + [self * mulvalue.constant])
        else:
            return self.__class__(self.name, self.factor * mulvalue)
    
    def __rmul__(self, mulvalue) -> (Expression | Variable):
        return self * mulvalue

    def __sub__(self, subvalue) -> (Expression | Variable):
        return self + (subvalue * -1)
    
    def __rsub__(self, subvalue) -> (Expression | Variable):
        return -1 * self + subvalue

    def __truediv__(self, divvalue) -> (Expression | Variable):
        if isinstance(divvalue, Variable):
            return self * divvalue.inverse
        else:
            return self.__class__(self.name, self.factor / divvalue)
    
    def __rdiv__(self, divvalue): # uniquement si divvalue est une constante
        pass # TODO : nécessite une changement de structure : attribut "exposant" ? 

if __name__ == '__main__':
    var_1 = Variable('x', 2) # 2x
    var_2 = Variable('y', 3) # 3y
    var_3 = Variable('x', 1) # 1x
    print('Variables : ')
    print(var_1, var_2, var_3)
    exp_1 = 4 - var_1 + var_2 - 5 # -2x + 3y + -1
    print(exp_1)
    print(repr(exp_1))
    exp_1x = exp_1 * var_3
    print(exp_1x)
    print(repr(exp_1x))
    exp_1x += var_3 + var_2 
    print(exp_1x)
    print(repr(exp_1x))
    var_12 = var_1 * var_2 * var_1 # 12yxx
    print(var_12) # human readable
    print(repr(var_12)) # debug

