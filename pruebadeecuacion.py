## FUNCIONA PERO SON SOLO 5 VARIABLES 

from scipy.optimize import linprog
#función objetivo de optimizar
# minimiza z = sum (x(i)*p(i))/P + sum (x(i)(Cins+Cop+Cmtt))
from pulp import LpProblem, LpVariable, lpSum, LpMinimize
problem = LpProblem("Minimization Problem", LpMinimize)
# Ejemplo con 5 variables enteras
x = [LpVariable(f"x{i}", lowBound=0, cat='Integer') for i in range(5)]
# Ejemplo de función objetivo
objective = lpSum([x[i] for i in range(2)])
problem += objective
# Ejemplo de restricciones
problem += lpSum([x[i] for i in range(2)]) >= 10
problem += lpSum([x[i] for i in range(2)]) <= 20
problem.solve()

optimal_value = problem.objective.value()
optimal_solution = [x[i].value() for i in range(2)]
print("Optimal Value:", optimal_value)
print("Optimal Solution:", optimal_solution)
