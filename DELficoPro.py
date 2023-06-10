## PARA ECUACIONES UTILIZANDO LA LIBRERIA DE XPRESS 

import xpress as xp
import numpy as np


def express_fico():
    # Parámetros para con números que ya están definidos
    N = 10  # Número de posibles ubicaciones
    M = 5  # Número de barras de distribución
    P_max = 100  # Capacidad máxima de cada barra de distribución
    # valores de arreglos de 10x1
    D = np.array([50, 30, 20, 40, 60, 25, 35, 45, 55, 50])  # Potencia demandada por electrolineras
    C = np.array([10000, 8000, 6000, 9000, 7000, 5000, 7500, 6500, 5500, 4000])  # Costo de instalación
    O = np.array([2000, 1500, 1200, 1800, 1400, 1000, 1600, 1300, 1100, 800])  # Costo de operación y mantenimiento
    Mante = np.array([2000, 1500, 1200, 1800, 1400, 1000, 1600, 1300, 1100, 800])  # matt
    C_gasolina = 30000  # Costo de una gasolinera

    # Crear el problema de optimización
    prob = xp.problem()

    # Variables de decisión
    X = [xp.var(vartype=xp.binary, name="X" + str(i + 1)) for i in range(N)]
    P = [[xp.var(lb=0, ub=P_max, name="P" + str(i + 1) + "_" + str(j + 1)) for j in range(M)] for i in range(N)]

    # Agregar variables al problema
    prob.addVariable(X)
    prob.addVariable(P)

    # Función objetivo
    obj = xp.Sum(C[i] * X[i] + O[i] * X[i] for i in range(N))
    prob.setObjective(obj, sense=xp.minimize)

    # Restricciones
    for j in range(M):
        prob.addConstraint(xp.Sum(P[i][j] for i in range(N)) <= P_max)

    for i in range(N):
        prob.addConstraint(xp.Sum(P[i][j] for j in range(M)) >= D[i] * X[i])

    costs_expr = xp.Sum(C[i] * X[i] + O[i] * X[i] for i in range(N))
    prob.addConstraint(costs_expr <= C_gasolina)

    # Resolver el problema
    prob.solve()

    # Imprimir la solución
    print("Estado de la solución:", prob.getProbStatusString())
    print("Valor óptimo de la función objetivo:", prob.getObjVal())

    for i in range(N):
        print("X" + str(i + 1) + ":", prob.getSolution(X[i]))

    for i in range(N):
        for j in range(M):
            print("P" + str(i + 1) + "_" + str(j + 1) + ":", prob.getSolution(P[i][j]))

