import math

def getfstring(a, b):
    c = math.sqrt(a ** 2 + b ** 2)

    # print(a + '^2 '+ b +'^2 = ' + c + '^2') # says unsupproted operand

    # print(a, '^2 +', b, '^2 = ', c, '^2')
    return f'output is: {a}^2 + {b}^2 = {c}^2'