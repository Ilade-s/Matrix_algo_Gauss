from typing import Any

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
    
    def non_zero(self, constant_included=False) -> list[Variable]:
        """return the variables that have a non zero factor (plus the constant if constant_included set to True)"""
        res = [v for v in self.vars if v] 
        if constant_included and self.constant:
            res.append(self.constant)
        return res

    def __len__(self) -> int:
        return len(self.non_zero(True))
    
    def __str__(self) -> str:
        return ' + '.join(map(str, self.non_zero(True)))
    
    def __repr__(self) -> str:
        vars_repr = ' ; '.join(map(repr, [v for v in self.vars if v]))
        return '{}(\n\tconst = {},\n\t{})'.format(self.__class__.__name__, self.constant, vars_repr)

    def __add__(self, addvalue) -> Expression:
        if isinstance(addvalue, Variable): 
            n_vars = self.non_zero()
            for i in range(len(n_vars)): 
                if addvalue.is_same_vars(n_vars[i]): # il faut vérifier la présence ou non de cette combinaison (produit) d'inconnues dans l'équation
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
            n_const = 0
            for t in self.non_zero(True):
                for t_mul in mulvalue.termes:
                    nt = t * t_mul
                    if isinstance(nt, Variable):
                        n_vars.append(nt)
                    else:
                        n_const += nt
            res = self.__class__(n_const, [])
            for v in n_vars:
                res += v
            return res
        elif isinstance(mulvalue, Variable):
            return self.__class__(0, [v * mulvalue for v in self.vars if v] + [self.constant * mulvalue])
        else:
            return self.__class__(self.constant * mulvalue, [v * mulvalue for v in self.vars if v])
    
    def __rmul__(self, mulvalue) -> Expression:
        return self * mulvalue
    
    def __div__(self, divvalue) -> Expression: # TODO
        pass
    
    def __pow__(self, power) -> Expression:
        res = 1
        for _ in range(power):
            res *= self
        return res

class Variable:
    """représente une variable avec son facteur associé dans une matrice"""
    def __init__(self, name: str, factor, exponent = 1) -> None:
        self.name = name
        self.factor = factor
        self.exp = exponent
    
    @property
    def inverse(self) -> Variable:
        """variable avec son facteur et son expsant inversé (^-1)"""
        return self.__class__(self.name, 1 / self.factor, -self.exp)

    @property
    def constant_factor(self):
        i_self = self
        while isinstance(i_self, self.__class__): # liste des inconnues de self
            i_self = i_self.factor
        return i_self
    
    def is_same_vars(self, var: Variable) -> bool:
        """return whether self and var have the same variables, at the same exponent, or not"""
        self_names = []
        var_names = []
        i_self = self
        i_var = var
        while isinstance(i_self, self.__class__): # liste des inconnues de self
            self_names.append((i_self.name, i_self.exp))
            i_self = i_self.factor
        while isinstance(i_var, self.__class__): # liste des inconnues de l'autre variable
            var_names.append((i_var.name, i_var.exp))
            i_var = i_var.factor
        # res est vrai uniquement si il y a exactement les mêmes inconnues, au même exposant pour chacune, dans self et var (pas forcément dans le même ordre)
        res = (sorted(self_names, key = lambda x: x[0]) == sorted(var_names, key = lambda x: x[0])) 
        return res 

    def __bool__(self) -> bool:
        return self.constant_factor != 0
    
    def __str__(self) -> str:
        return (str(self.factor) if self.factor != 1 else '') + self.name + ('^{}'.format(self.exp) if self.exp != 1 else '')
    
    def __repr__(self) -> str:
        return "{}({}, {}, {})".format(self.__class__.__name__, repr(self.factor), self.name, self.exp)

    def __add__(self, addvalue) -> (Expression | Variable):
        if isinstance(addvalue, self.__class__):
            if self.is_same_vars(addvalue):
                mul_factor = (self.constant_factor + addvalue.constant_factor) / self.constant_factor
                return self * mul_factor
            else:
                return Expression(0, [self, addvalue])
        elif isinstance(addvalue, Expression):
            return addvalue + self
        else:
            return Expression(addvalue, [self])
    
    def __radd__(self, addvalue) -> (Expression | Variable):
        return self + addvalue

    def __mul__(self, mulvalue) -> (Expression | Variable | Any):
        if isinstance(mulvalue, self.__class__):
            n_var = self.__class__(self.name, self.factor, self.exp)
            i_factor = n_var
            while i_factor.name != mulvalue.name and isinstance(i_factor.factor, self.__class__):
                i_factor = i_factor.factor
            if i_factor.name == mulvalue.name:
                i_factor.factor *= mulvalue.factor
                i_factor.exp += mulvalue.exp
                if i_factor.exp == 0: # inconnue à la puissance 0 -> simplifier en une constante seulement
                    return i_factor.factor
            else:    
                i_factor.factor *= mulvalue
            return n_var
        elif isinstance(mulvalue, Expression):
            return Expression(0, [self * v for v in mulvalue.vars if v] + [self * mulvalue.constant])
        else:
            return self.__class__(self.name, self.factor * mulvalue, self.exp)
    
    def __rmul__(self, mulvalue) -> (Expression | Variable | Any):
        return self * mulvalue

    def __sub__(self, subvalue) -> (Expression | Variable):
        return self + (subvalue * -1)
    
    def __rsub__(self, subvalue) -> (Expression | Variable):
        return -1 * self + subvalue

    def __truediv__(self, divvalue) -> (Expression | Variable | Any):
        if isinstance(divvalue, Variable):
            return self * divvalue.inverse
        else:
            return self.__class__(self.name, self.factor / divvalue, self.exp)
    
    def __rtruediv__(self, divvalue) -> (Expression | Variable | Any):
        return divvalue * self.inverse

    def __pow__(self, power) -> Variable:
        return self.__class__(self.name, self.factor ** power, self.exp * power)

if __name__ == '__main__':
    x = Variable('x', 1)
    y = Variable('y', 1)
    z = Variable('z', 1)
    print('Variables : ')
    print(x, y, z)
    print('Expressions :')
    exp_1 = 4 - 2 * x + 3 * y - 5 
    print("exp_1 =", exp_1) # -2x + 3y + -1
    print(repr(exp_1))
    print("\nexp_1 au carré (exp_1^2) =", exp_1**2) # 4x^2 + -12.0yx + 4.0x + 9y^2 + -6.0y + 1 
    print(repr(exp_1**2))
    x_inv = 2 / (2 * x) # x^-1
    print("\ninverse de x (x^-1) =", x_inv)
    print(repr(x_inv))
    dev = x_inv * exp_1**2
    print("\nx^-1 * exp_1^2 =", dev) # 4.0x + -12.0y + 4.0 + 9.0y^2x^-1 + -6.0yx^-1 + x^-1
    print(repr(dev))
    exp_1x = exp_1 * x 
    print("\nexp_1 * x =", exp_1x) # -2x^2 + 3yx + -1x
    print(repr(exp_1x))
    x2 = (2 * x) * (3 * y) * x 
    print("\nx2 =", x2) # 6yx^2
    print(repr(x2))
    print("\nx2 au carré (x2^2) :", x2**2) # 36y^2x^4
    


