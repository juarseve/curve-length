from sympy import symbols, lambdify, diff
from numpy import sum, linspace, ndarray, pi


def crear_funcion(funciones_coordenadas: list) -> lambdify:
    t = symbols("t")
    f = ((diff(funciones_coordenadas[0], t) ** 2) +
         (diff(funciones_coordenadas[1], t) ** 2) +
         (diff(funciones_coordenadas[2], t) ** 2)) ** (1 / 2)

    return lambdify(t, f, "numpy")


def suma_de_riemann(funcion: lambdify, n: int) -> ndarray:
    dtheta = (2 * pi - 0) / n
    intervalos = linspace(0, 2 * pi, num=n)

    if n == 1:
        medio = [0, pi]
    else:
        medio = (intervalos[:-1] + intervalos[1:]) / 2

    return sum(funcion(medio) * dtheta)